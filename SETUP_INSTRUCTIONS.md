# OCR Typer - Setup & Build Instructions

## What is OCR Typer?

A portable Windows application that:
- Allows you to select a screen area by dragging
- Shows a green overlay over the selected area
- Every 2 seconds, reads any text in that area using OCR
- Automatically types the detected text at your cursor
- Continues working even if you switch tabs/windows
- Can be stopped at any time with the STOP button

## System Requirements

- Windows 7 or later (64-bit recommended)
- Python 3.8+ (if running from source)
- Tesseract OCR installed
- ~50MB disk space

## Installation Steps

### Option A: Use Pre-built EXE (Easiest)

1. **Download OCRTyper.exe** from the `dist/` folder
2. **Install Tesseract OCR:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download: `tesseract-ocr-w64-setup-v5.x.x.exe`
   - Run installer (default path: `C:\Program Files\Tesseract-OCR`)
3. **Run OCRTyper.exe**

### Option B: Build EXE from Source

1. **Install Python 3.8+** from https://www.python.org
2. **Install Tesseract OCR:**
   - https://github.com/UB-Mannheim/tesseract/wiki
   - Install to `C:\Program Files\Tesseract-OCR`

3. **Clone or download this repository:**
   ```bash
   git clone https://github.com/harisviennas-rgb/ocr-typer.git
   cd ocr-typer
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Build the EXE:**
   ```bash
   python build_exe.py
   ```

6. **Find your EXE:**
   - `dist/OCRTyper.exe` - Ready to use!
   - `OCRTyper_Portable.zip` - Share with others

## How to Use

### Step 1: Start
Click the **"START"** button on the main window

### Step 2: Select Area
- Click and drag to select the area where text appears
- You'll see a green overlay marking your selection
- Release to confirm

### Step 3: Position Your Cursor
- Click in any text input field (email, message, document, etc.)
- Keep the window visible (but you can minimize other windows)

### Step 4: It Will Start Working Automatically
- Every 2 seconds, it checks for text in the selected area
- When new text is detected, it types it automatically
- The green area stays visible so you know what's being read

### Step 5: Stop When Done
Click the **"STOP"** button to stop monitoring

## Features

✓ **Draggable Window** - Drag by the title bar to move around  
✓ **Always on Top** - Stays above other windows  
✓ **Persistent Selection** - Green overlay shows the monitored area  
✓ **Background Monitoring** - Works even when window is not focused  
✓ **2-Second Interval** - Checks for new text every 2 seconds  
✓ **Portable** - Single EXE file, no installation needed (except Tesseract)  

## Troubleshooting

### Error: "pytesseract.TesseractNotFoundError"
**Problem:** Tesseract OCR not found  
**Solution:**
1. Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Make sure it's installed to: `C:\Program Files\Tesseract-OCR`
3. Restart OCRTyper

### Text is not being recognized
**Solution:**
1. Make sure the selected area is visible and clear
2. Good lighting/contrast improves OCR accuracy
3. Try selecting a larger area

### Text is not being typed
**Solution:**
1. Click in the target text field BEFORE starting
2. Make sure the field is focused (cursor visible)
3. Check that OCRTyper shows "Running OCR..."

### App crashes on startup
**Solution:**
1. Make sure Python 3.8+ is installed (if running from source)
2. Verify all dependencies: `pip install -r requirements.txt`
3. Check Tesseract installation path

## File Structure

```
ocr-typer/
├── ocr_typer_gui.py          # Main application code
├── build_exe.py              # Build script for EXE
├── requirements.txt          # Python dependencies
├── SETUP_INSTRUCTIONS.md     # This file
└── dist/
    └── OCRTyper.exe          # Ready-to-use executable
```

## Advanced: Customization

### Change OCR Interval
Edit `ocr_typer_gui.py`, line ~150:
```python
time.sleep(2)  # Change 2 to your desired seconds
```

### Change Window Size
Edit `ocr_typer_gui.py`, line ~19:
```python
self.root.geometry("200x100")  # width x height
```

### Tesseract Custom Path
If Tesseract is installed elsewhere, set environment variable:
```bash
set PYTESSERACT_PATH=C:\YourPath\tesseract.exe
```

## Performance Notes

- CPU usage: ~5-10% while monitoring
- Memory usage: ~50-100MB
- Tesseract processing: ~1-2 seconds per image
- Best results with 100x100 pixel or larger selection area

## Security & Privacy

- This application runs locally on your computer
- No data is sent to any server
- No internet connection required
- Source code is open and available

## Uninstall

1. Delete `OCRTyper.exe`
2. (Optional) Uninstall Tesseract OCR from Control Panel

## Support & Issues

Report issues at: https://github.com/harisviennas-rgb/ocr-typer/issues

## License

MIT License - Free to use and modify

## Credits

Built with:
- Tesseract OCR (text recognition)
- PyAutoGUI (screen automation)
- PIL (image processing)
- PyInstaller (executable builder)
