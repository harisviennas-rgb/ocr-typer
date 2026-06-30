"""
Build script to create standalone EXE using PyInstaller
Run: python build_exe.py
"""

import os
import shutil
import subprocess
import sys

def build_exe():
    """Build the EXE using PyInstaller"""
    
    print("=" * 60)
    print("OCR Typer - EXE Builder")
    print("=" * 60)
    
    # Clean previous builds
    print("\n[1/5] Cleaning previous builds...")
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    print("[2/5] Checking dependencies...")
    # Verify required packages
    required_packages = ['pytesseract', 'pillow', 'pyautogui', 'pynput', 'pyinstaller']
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} NOT FOUND")
            print(f"\nInstalling {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("\n[3/5] Building EXE with PyInstaller...")
    
    # PyInstaller command
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',  # Create single EXE file
        '--windowed',  # No console window
        '--icon=NONE',  # No icon (optional)
        '--name=OCRTyper',  # Executable name
        '--add-data=ocr_typer_gui.py:.',  # Include main script
        'ocr_typer_gui.py'  # Main script
    ]
    
    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print("✓ PyInstaller build completed")
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller failed: {e}")
        return False
    
    print("\n[4/5] Creating distribution zip...")
    
    # Create zip with EXE and instructions
    zip_name = 'OCRTyper_Portable'
    
    # Create temporary folder
    if os.path.exists(zip_name):
        shutil.rmtree(zip_name)
    os.makedirs(zip_name)
    
    # Copy EXE
    exe_path = 'dist/OCRTyper.exe'
    if os.path.exists(exe_path):
        shutil.copy(exe_path, f'{zip_name}/OCRTyper.exe')
        print(f"✓ Copied EXE to {zip_name}/")
    else:
        print(f"✗ EXE not found at {exe_path}")
        return False
    
    # Create README
    readme_content = """OCR TYPER - PORTABLE VERSION
============================

REQUIREMENTS:
- Windows 7 or later (64-bit recommended)
- Tesseract OCR installed on your system

INSTALLATION STEPS:

1. Install Tesseract OCR:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Run the installer (tesseract-ocr-w64-setup-v5.x.x.exe)
   - Install to: C:\\Program Files\\Tesseract-OCR
   - Remember the installation path

2. Run OCRTyper.exe

HOW TO USE:

1. Click "START" button
2. Click and drag to select the area where text appears (the area you want to read)
3. The selected area will be highlighted in green
4. Every 2 seconds, the app will:
   - Take a screenshot of the selected area
   - Use Tesseract to read any text
   - Type the text automatically at your cursor position
5. Click "STOP" to stop monitoring
   - The green highlight stays visible until you click START again

FEATURES:
- Draggable GUI window (drag by the title)
- Stays on top of other windows
- Continues working even if you switch tabs/windows
- Automatic typing on detected text changes
- Every 2-second interval check for new text

TIPS:
- Make sure your cursor is in the text input field before clicking START
- Select a clear area with good contrast for better OCR accuracy
- The first detection may take a few seconds

TROUBLESHOOTING:

If you get "pytesseract.TesseractNotFoundError":
- Tesseract OCR is not installed
- Install it from: https://github.com/UB-Mannheim/tesseract/wiki
- Make sure to install to C:\\Program Files\\Tesseract-OCR

If text is not being typed:
- Check that your input field is focused
- Try selecting a different area with clearer text
- Increase the selected crop area size

For more info, visit: https://github.com/harisviennas-rgb/ocr-typer
"""
    
    with open(f'{zip_name}/README.txt', 'w') as f:
        f.write(readme_content)
    
    # Create config file for Tesseract path
    config_content = """# OCRTyper Configuration
# If Tesseract is installed in a non-standard location, update this:

TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe
"""
    
    with open(f'{zip_name}/config.ini', 'w') as f:
        f.write(config_content)
    
    # Create setup script
    setup_script = """@echo off
echo Installing Tesseract OCR requirement...
echo Please download and run the Tesseract installer:
echo https://github.com/UB-Mannheim/tesseract/wiki
pause
"""
    
    with open(f'{zip_name}/INSTALL_TESSERACT.bat', 'w') as f:
        f.write(setup_script)
    
    # Zip the folder
    print(f"Creating {zip_name}.zip...")
    shutil.make_archive(zip_name, 'zip', '.', zip_name)
    print(f"✓ Created {zip_name}.zip")
    
    print("\n[5/5] Finalizing...")
    
    # Create summary file
    summary = f"""BUILD COMPLETE!
===============

Generated Files:
✓ dist/OCRTyper.exe - Main executable
✓ {zip_name}.zip - Portable version with documentation

To distribute or use:
1. Use OCRTyper.exe directly, OR
2. Share {zip_name}.zip with others

Total size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB (EXE only)

Next steps:
1. Install Tesseract OCR
2. Run OCRTyper.exe
3. Enjoy!
"""
    
    print(summary)
    
    with open('BUILD_SUMMARY.txt', 'w') as f:
        f.write(summary)
    
    print("\n" + "=" * 60)
    print("Build successful! Check dist/ folder and .zip file")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
