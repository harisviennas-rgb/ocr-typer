import tkinter as tk
from tkinter import messagebox
import threading
import pyautogui
import time
from PIL import Image, ImageDraw, ImageTk
import pytesseract
import os
from pynput import mouse, keyboard
from datetime import datetime

class OCRTyperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Typer - Draggable GUI")
        self.root.geometry("200x100")
        self.root.attributes('-topmost', True)
        self.root.resizable(False, False)
        
        # Set window to stay on top
        self.root.attributes('-type', 'splash')
        
        # Variables
        self.is_running = False
        self.crop_area = None
        self.monitoring_thread = None
        self.start_x = 0
        self.start_y = 0
        self.cropping = False
        self.last_ocr_result = ""
        self.overlay = None
        self.mouse_listener = None
        self.keyboard_listener = None
        
        # Create GUI elements
        self.label = tk.Label(root, text="OCR Typer", font=("Arial", 12, "bold"))
        self.label.pack()
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.start_btn = tk.Button(button_frame, text="START", command=self.start_crop, 
                                    bg="green", fg="white", font=("Arial", 10, "bold"), width=10)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="STOP", command=self.stop_ocr, 
                                   bg="red", fg="white", font=("Arial", 10, "bold"), width=10, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        # Make window draggable
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        
        # Status label
        self.status_label = tk.Label(root, text="Ready", font=("Arial", 8))
        self.status_label.pack()
        
    def start_move(self, event):
        self.root.x = event.x_root - self.root.winfo_x()
        self.root.y = event.y_root - self.root.winfo_y()
    
    def do_move(self, event):
        x = event.x_root - self.root.x
        y = event.y_root - self.root.y
        self.root.geometry(f"+{x}+{y}")
    
    def start_crop(self):
        """Start cropping mode"""
        self.status_label.config(text="Select area...")
        self.start_btn.config(state="disabled")
        
        # Create overlay window
        self.create_overlay()
        
        # Set up mouse listener for cropping
        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click
        )
        self.mouse_listener.start()
    
    def create_overlay(self):
        """Create transparent overlay for selection"""
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes('-alpha', 0.3)
        self.overlay.attributes('-topmost', True)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.overlay.geometry(f"{screen_width}x{screen_height}+0+0")
        self.overlay.configure(bg='blue')
        
        # Create canvas for drawing
        self.canvas = tk.Canvas(self.overlay, bg='blue', cursor="crosshair", 
                               highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_overlay_click)
        self.canvas.bind("<Button1-Motion>", self.on_overlay_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_overlay_release)
        
        self.rect = None
        self.start_x = 0
        self.start_y = 0
    
    def on_mouse_move(self, x, y):
        """Track mouse movement (optional visual feedback)"""
        pass
    
    def on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click for cropping"""
        if not pressed and button == mouse.Button.left:
            return False
    
    def on_overlay_click(self, event):
        """Start selection on overlay"""
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
    
    def on_overlay_drag(self, event):
        """Draw selection rectangle while dragging"""
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline="red", width=2
        )
    
    def on_overlay_release(self, event):
        """Finish selection"""
        end_x = event.x
        end_y = event.y
        
        # Normalize coordinates
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        
        self.crop_area = (x1, y1, x2, y2)
        
        # Close overlay
        self.overlay.destroy()
        self.overlay = None
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        
        # Show selected area with semi-transparent box
        self.show_crop_selection()
        
        # Start OCR monitoring
        self.is_running = True
        self.stop_btn.config(state="normal")
        self.status_label.config(text="Running OCR...")
        self.monitoring_thread = threading.Thread(target=self.monitor_ocr, daemon=True)
        self.monitoring_thread.start()
    
    def show_crop_selection(self):
        """Show the selected crop area with overlay"""
        if not self.crop_area:
            return
        
        x1, y1, x2, y2 = self.crop_area
        
        # Create a window showing the crop area
        selection_window = tk.Toplevel(self.root)
        selection_window.attributes('-alpha', 0.2)
        selection_window.attributes('-topmost', True)
        selection_window.configure(bg='green')
        selection_window.geometry(f"{x2-x1}x{y2-y1}+{x1}+{y1}")
        
        # Keep reference to prevent garbage collection
        self.selection_window = selection_window
    
    def monitor_ocr(self):
        """Monitor the crop area for text every 2 seconds"""
        while self.is_running:
            try:
                time.sleep(2)  # Wait 2 seconds before checking again
                
                if not self.is_running:
                    break
                
                # Capture screenshot of crop area
                if self.crop_area:
                    x1, y1, x2, y2 = self.crop_area
                    screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
                    
                    # Perform OCR
                    text = pytesseract.image_to_string(screenshot)
                    text = text.strip()
                    
                    # If new text found and different from last, type it
                    if text and text != self.last_ocr_result:
                        self.last_ocr_result = text
                        self.type_text(text)
                        self.update_status(f"Typed: {text[:30]}...")
            
            except Exception as e:
                print(f"OCR Error: {e}")
    
    def type_text(self, text):
        """Type the extracted text"""
        try:
            # Small delay to ensure focus
            time.sleep(0.1)
            pyautogui.typewrite(text, interval=0.05)
        except Exception as e:
            print(f"Typing error: {e}")
    
    def stop_ocr(self):
        """Stop the OCR monitoring"""
        self.is_running = False
        self.stop_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.status_label.config(text="Stopped")
        
        # Close selection window
        if self.selection_window:
            try:
                self.selection_window.destroy()
            except:
                pass
        
        self.last_ocr_result = ""
    
    def update_status(self, message):
        """Update status label safely from thread"""
        try:
            self.status_label.config(text=message)
            self.root.update_idletasks()
        except:
            pass

def main():
    root = tk.Tk()
    app = OCRTyperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
