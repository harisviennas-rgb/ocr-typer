# OCR Typer 📝

A portable Windows application that automatically reads text from a selected screen area and types it for you.

## ✨ Features

- **Drag & Drop Window** - Draggable GUI that stays on top
- **Select Area** - Click and drag to choose what to read
- **Auto-Read** - Every 2 seconds, reads text in selected area
- **Auto-Type** - Automatically types detected text
- **Always Working** - Continues even when you switch windows
- **Portable** - Single EXE file (except Tesseract dependency)
- **Visual Feedback** - Green overlay shows monitored area

## 🚀 Quick Start

### Download & Run (Easiest)
1. Download `OCRTyper.exe` from the releases
2. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
3. Run `OCRTyper.exe`

### Build from Source
```bash
git clone https://github.com/harisviennas-rgb/ocr-typer.git
cd ocr-typer
pip install -r requirements.txt
python build_exe.py
```

## 📖 How to Use

1. **Click START** - Begin selecting mode
2. **Drag to Select** - Choose the area with text you want to read
3. **Click in Input Field** - Where you want text typed
4. **It Works!** - Every 2 seconds, new text is detected and typed
5. **Click STOP** - To stop monitoring

## 📋 Requirements

- Windows 7 or later (64-bit)
- Tesseract OCR installed
- No internet needed

## 📦 What's Included

- `ocr_typer_gui.py` - Main application
- `build_exe.py` - Script to build EXE
- `requirements.txt` - Python dependencies
- `SETUP_INSTRUCTIONS.md` - Detailed setup guide
- `dist/OCRTyper.exe` - Ready-to-use executable

## 🛠️ Technologies

- Python 3.8+
- Tesseract OCR
- PyAutoGUI
- PIL/Pillow
- PyInstaller

## 📝 Use Cases

- Extract text from video streams
- Read live chat messages and auto-respond
- Capture text from screenshots/images
- Automate data entry from visual sources
- Read OCR results and type into forms

## ⚙️ Advanced

### Change Check Interval
Edit `ocr_typer_gui.py`:
```python
time.sleep(2)  # Change to your desired seconds
```

### Customize Window
```python
self.root.geometry("200x100")  # width x height
```

## 🐛 Troubleshooting

**"TesseractNotFoundError"**
- Install Tesseract OCR from official source
- Default path: `C:\Program Files\Tesseract-OCR`

**Text not recognized**
- Select a clearer area
- Improve screen contrast/lighting

**Text not typing**
- Click in input field before starting
- Check if field is focused

## 📄 License

MIT License - Free to use and modify

## 🔗 Links

- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- [PyAutoGUI Docs](https://pyautogui.readthedocs.io/)
- [GitHub Repository](https://github.com/harisviennas-rgb/ocr-typer)

## ❓ FAQ

**Q: Does it need internet?**  
A: No, everything runs locally.

**Q: Is it safe?**  
A: Yes, open source and runs on your machine only.

**Q: Can I stop it anytime?**  
A: Yes, click the STOP button or close the window.

**Q: Does it keep working if I minimize it?**  
A: Yes, it continues in the background.

**Q: Can I move the window?**  
A: Yes, drag by the title bar - it stays on top.

---

Made with ❤️ for automation and productivity
