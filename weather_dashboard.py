"""
Weather Dashboard - Main Application
Fetches weather data from OpenWeatherMap API and displays it in a modern GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
from datetime import datetime
import json
import os

class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2e")
        
        # API Configuration
        self.API_KEY = "YOUR_API_KEY_HERE"  # Get from https://openweathermap.org/api
        self.BASE_URL = "https://api.openweathermap.org/data/2.5"
        
        # Load config if exists
        self.load_config()
        
        # Variables
        self.weather_data = None
        self.forecast_data = None
        self.is_loading = False
        
        # Create UI
        self.create_ui()
        
        # Load weather for default city
        self.search_city("London")
    
    def load_config(self):
        """Load API key from config file if exists"""
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                    self.API_KEY = config.get("API_KEY", self.API_KEY)
            except:
                pass
    
    def save_config(self):
        """Save API key to config file"""
        config = {"API_KEY": self.API_KEY}
        with open("config.json", "w") as f:
            json.dump(config, f)
    
    def create_ui(self):
        """Create the main UI layout"""
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#16213e", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="🌤️ Weather Dashboard", 
                        font=("Arial", 24, "bold"), fg="#00d4ff", bg="#16213e")
        title.pack(side="left", padx=20, pady=15)
        
        # Search Frame
        search_frame = tk.Frame(header_frame, bg="#16213e")
        search_frame.pack(side="right", padx=20, pady=15)
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30,
                                     bg="#0f3460", fg="#ffffff", 
                                     insertbackground="#00d4ff")
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_city())
        
        search_btn = tk.Button(search_frame, text="Search", command=self.search_city,
                              bg="#00d4ff", fg="#000000", font=("Arial", 10, "bold"),
                              cursor="hand2", relief="flat", padx=20)
        search_btn.pack(side="left", padx=5)
        
        settings_btn = tk.Button(search_frame, text="⚙️ Settings", command=self.open_settings,
                                bg="#e94560", fg="#ffffff", font=("Arial", 10, "bold"),
                                cursor="hand2", relief="flat", padx=15)
        settings_btn.pack(side="left", padx=5)
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg="#1e1e2e")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Current Weather Frame
        current_frame = tk.Frame(content_frame, bg="#0f3460", relief="flat")
        current_frame.pack(fill="x", pady=(0, 20))
        
        self.current_weather_frame = tk.Frame(current_frame, bg="#0f3460")
        self.current_weather_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Main content with weather info and forecast
        main_frame = tk.Frame(content_frame, bg="#1e1e2e")
        main_frame.pack(fill="both", expand=True)
        
        # Left side - Details
        left_frame = tk.Frame(main_frame, bg="#1e1e2e")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.details_frame = tk.Frame(left_frame, bg="#0f3460", relief="flat")
        self.details_frame.pack(fill="both", expand=True)
        
        # Right side - Forecast
        right_frame = tk.Frame(main_frame, bg="#1e1e2e")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        forecast_label = tk.Label(right_frame, text="5-Day Forecast", 
                                 font=("Arial", 14, "bold"), fg="#00d4ff", bg="#1e1e2e")
        forecast_label.pack(anchor="w", pady=(0, 10))
        
        self.forecast_frame = tk.Frame(right_frame, bg="#1e1e2e")
        self.forecast_frame.pack(fill="both", expand=True)
    
    def search_city(self, city=None):
        """Search for weather by city name"""
        if city is None:
            city = self.search_entry.get()
        
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
        
        if not self.API_KEY or self.API_KEY == "YOUR_API_KEY_HERE":
            messagebox.showerror("API Key Error", 
                               "Please set your OpenWeatherMap API key in Settings")
            return
        
        # Fetch data in thread to avoid freezing UI
        thread = threading.Thread(target=self._fetch_weather, args=(city,), daemon=True)
        thread.start()
    
    def _fetch_weather(self, city):
        """Fetch weather data from API"""
        try:
            self.is_loading = True
            
            # Current weather
            weather_url = f"{self.BASE_URL}/weather?q={city}&appid={self.API_KEY}&units=metric"
            weather_response = requests.get(weather_url, timeout=5)
            weather_response.raise_for_status()
            self.weather_data = weather_response.json()
            
            # 5-day forecast
            forecast_url = f"{self.BASE_URL}/forecast?q={city}&appid={self.API_KEY}&units=metric"
            forecast_response = requests.get(forecast_url, timeout=5)
            forecast_response.raise_for_status()
            self.forecast_data = forecast_response.json()
            
            # Update UI in main thread
            self.root.after(0, self.display_weather)
            
        except requests.exceptions.ConnectionError:
            self.root.after(0, lambda: messagebox.showerror("Connection Error", 
                                                            "Could not connect to weather service"))
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                self.root.after(0, lambda: messagebox.showerror("City Not Found", 
                                                                "The city was not found. Please try again."))
            elif e.response.status_code == 401:
                self.root.after(0, lambda: messagebox.showerror("API Error", 
                                                                "Invalid API key. Please check Settings."))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
        finally:
            self.is_loading = False
    
    def display_weather(self):
        """Display current weather"""
        if not self.weather_data:
            return
        
        # Clear previous content
        for widget in self.current_weather_frame.winfo_children():
            widget.destroy()
        
        data = self.weather_data
        
        # City name and country
        city_info = tk.Label(self.current_weather_frame, 
                            text=f"{data['name']}, {data['sys']['country']}", 
                            font=("Arial", 20, "bold"), fg="#00d4ff", bg="#0f3460")
        city_info.pack(anchor="w")
        
        # Container for temp and description
        info_frame = tk.Frame(self.current_weather_frame, bg="#0f3460")
        info_frame.pack(fill="x", pady=10)
        
        # Temperature
        temp = int(data['main']['temp'])
        weather_desc = data['weather'][0]['main']
        weather_icon = data['weather'][0]['icon']
        
        temp_label = tk.Label(info_frame, text=f"{temp}°C", 
                             font=("Arial", 48, "bold"), fg="#ffffff", bg="#0f3460")
        temp_label.pack(side="left")
        
        # Description and icon
        desc_frame = tk.Frame(info_frame, bg="#0f3460")
        desc_frame.pack(side="left", padx=20)
        
        desc_label = tk.Label(desc_frame, text=weather_desc, 
                             font=("Arial", 16), fg="#00d4ff", bg="#0f3460")
        desc_label.pack(anchor="w")
        
        feels_like = int(data['main']['feels_like'])
        feels_label = tk.Label(desc_frame, text=f"Feels like {feels_like}°C", 
                              font=("Arial", 12), fg="#888888", bg="#0f3460")
        feels_label.pack(anchor="w")
        
        # Display weather details
        self.display_weather_details()
        
        # Display forecast
        self.display_forecast()
    
    def display_weather_details(self):
        """Display detailed weather information"""
        if not self.weather_data:
            return
        
        # Clear previous content
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        data = self.weather_data
        
        details_label = tk.Label(self.details_frame, text="Weather Details", 
                                font=("Arial", 14, "bold"), fg="#00d4ff", bg="#0f3460")
        details_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Details grid
        details = [
            ("Humidity", f"{data['main']['humidity']}%", "💧"),
            ("Pressure", f"{data['main']['pressure']} hPa", "🔽"),
            ("Wind Speed", f"{data['wind']['speed']} m/s", "💨"),
            ("UV Index", "N/A", "☀️"),
            ("Visibility", f"{data['visibility']/1000:.1f} km", "👁️"),
            ("Sunrise", datetime.fromtimestamp(data['sys']['sunrise']).strftime("%H:%M"), "🌅"),
            ("Sunset", datetime.fromtimestamp(data['sys']['sunset']).strftime("%H:%M"), "🌇"),
            ("Cloud Coverage", f"{data['clouds']['all']}%", "☁️"),
        ]
        
        for detail, value, icon in details:
            detail_frame = tk.Frame(self.details_frame, bg="#0f3460")
            detail_frame.pack(fill="x", padx=20, pady=5)
            
            label = tk.Label(detail_frame, text=f"{icon} {detail}:", 
                           font=("Arial", 11), fg="#888888", bg="#0f3460", width=15)
            label.pack(side="left")
            
            value_label = tk.Label(detail_frame, text=value, 
                                  font=("Arial", 11, "bold"), fg="#00d4ff", bg="#0f3460")
            value_label.pack(side="left")
    
    def display_forecast(self):
        """Display 5-day forecast"""
        if not self.forecast_data:
            return
        
        # Clear previous content
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()
        
        forecast_list = self.forecast_data['list']
        
        # Group by day (daily forecast at noon)
        daily_forecasts = {}
        for item in forecast_list:
            date = datetime.fromtimestamp(item['dt']).date()
            time = datetime.fromtimestamp(item['dt']).hour
            
            # Get forecast at 12:00 (noon)
            if time == 12 or (date not in daily_forecasts and time > 9):
                daily_forecasts[date] = item
        
        # Display first 5 days
        for i, (date, item) in enumerate(list(daily_forecasts.items())[:5]):
            forecast_day_frame = tk.Frame(self.forecast_frame, bg="#0f3460", relief="flat")
            forecast_day_frame.pack(fill="x", pady=5)
            
            # Date
            date_label = tk.Label(forecast_day_frame, text=date.strftime("%a, %b %d"), 
                                 font=("Arial", 10), fg="#00d4ff", bg="#0f3460", width=12)
            date_label.pack(side="left", padx=10)
            
            # Weather description
            desc = item['weather'][0]['main']
            desc_label = tk.Label(forecast_day_frame, text=desc, 
                                 font=("Arial", 10), fg="#ffffff", bg="#0f3460", width=15)
            desc_label.pack(side="left", padx=5)
            
            # Temperature
            temp_max = int(item['main']['temp_max'])
            temp_min = int(item['main']['temp_min'])
            temp_label = tk.Label(forecast_day_frame, 
                                 text=f"{temp_max}°C / {temp_min}°C", 
                                 font=("Arial", 10, "bold"), fg="#888888", bg="#0f3460")
            temp_label.pack(side="left", padx=5)
            
            # Precipitation chance
            rain_chance = int(item.get('pop', 0) * 100)
            rain_label = tk.Label(forecast_day_frame, text=f"💧 {rain_chance}%", 
                                 font=("Arial", 9), fg="#6ba3ff", bg="#0f3460")
            rain_label.pack(side="right", padx=10)
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x300")
        settings_window.configure(bg="#1e1e2e")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # API Key Frame
        api_frame = tk.Frame(settings_window, bg="#1e1e2e")
        api_frame.pack(fill="x", padx=20, pady=20)
        
        api_label = tk.Label(api_frame, text="OpenWeatherMap API Key:", 
                            font=("Arial", 11, "bold"), fg="#00d4ff", bg="#1e1e2e")
        api_label.pack(anchor="w", pady=(0, 5))
        
        api_entry = tk.Entry(api_frame, font=("Arial", 10), width=50,
                            bg="#0f3460", fg="#ffffff", insertbackground="#00d4ff")
        api_entry.pack(fill="x", pady=(0, 10))
        api_entry.insert(0, self.API_KEY)
        
        info_label = tk.Label(api_frame, 
                             text="Get a free API key from: https://openweathermap.org/api", 
                             font=("Arial", 9), fg="#888888", bg="#1e1e2e")
        info_label.pack(anchor="w", pady=(0, 20))
        
        # Temperature Unit
        unit_frame = tk.Frame(settings_window, bg="#1e1e2e")
        unit_frame.pack(fill="x", padx=20, pady=10)
        
        unit_label = tk.Label(unit_frame, text="Temperature Unit:", 
                             font=("Arial", 11, "bold"), fg="#00d4ff", bg="#1e1e2e")
        unit_label.pack(anchor="w", pady=(0, 5))
        
        unit_var = tk.StringVar(value="celsius")
        tk.Radiobutton(unit_frame, text="Celsius (°C)", variable=unit_var, value="celsius",
                      bg="#1e1e2e", fg="#ffffff", activebackground="#0f3460",
                      activeforeground="#00d4ff", selectcolor="#0f3460").pack(anchor="w")
        tk.Radiobutton(unit_frame, text="Fahrenheit (°F)", variable=unit_var, value="fahrenheit",
                      bg="#1e1e2e", fg="#ffffff", activebackground="#0f3460",
                      activeforeground="#00d4ff", selectcolor="#0f3460").pack(anchor="w")
        
        # Buttons
        button_frame = tk.Frame(settings_window, bg="#1e1e2e")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        save_btn = tk.Button(button_frame, text="Save", 
                            command=lambda: self.save_settings(api_entry.get(), settings_window),
                            bg="#00d4ff", fg="#000000", font=("Arial", 10, "bold"),
                            cursor="hand2", relief="flat", padx=30)
        save_btn.pack(side="left", padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=settings_window.destroy,
                              bg="#555555", fg="#ffffff", font=("Arial", 10, "bold"),
                              cursor="hand2", relief="flat", padx=30)
        cancel_btn.pack(side="left", padx=5)
    
    def save_settings(self, api_key, window):
        """Save settings"""
        if not api_key:
            messagebox.showwarning("Input Error", "Please enter an API key")
            return
        
        self.API_KEY = api_key
        self.save_config()
        messagebox.showinfo("Success", "Settings saved successfully!")
        window.destroy()

def main():
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
