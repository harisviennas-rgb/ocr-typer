"""
Build script to create standalone Weather Dashboard EXE using PyInstaller
Run: python build_weather_exe.py
"""

import os
import shutil
import subprocess
import sys

def build_exe():
    """Build the Weather Dashboard EXE using PyInstaller"""
    
    print("=" * 60)
    print("Weather Dashboard - EXE Builder")
    print("=" * 60)
    
    # Clean previous builds
    print("\n[1/5] Cleaning previous builds...")
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    print("[2/5] Checking dependencies...")
    # Verify required packages
    required_packages = ['requests', 'pillow', 'pyinstaller']
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
        '--name=WeatherDashboard',  # Executable name
        'weather_dashboard.py'  # Main script
    ]
    
    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print("✓ PyInstaller build completed")
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller failed: {e}")
        return False
    
    print("\n[4/5] Creating distribution zip...")
    
    # Create zip with EXE and instructions
    zip_name = 'WeatherDashboard_Portable'
    
    # Create temporary folder
    if os.path.exists(zip_name):
        shutil.rmtree(zip_name)
    os.makedirs(zip_name)
    
    # Copy EXE
    exe_path = 'dist/WeatherDashboard.exe'
    if os.path.exists(exe_path):
        shutil.copy(exe_path, f'{zip_name}/WeatherDashboard.exe')
        print(f"✓ Copied EXE to {zip_name}/")
    else:
        print(f"✗ EXE not found at {exe_path}")
        return False
    
    # Create README
    readme_content = """WEATHER DASHBOARD - PORTABLE VERSION
=====================================

FEATURES:
✓ Real-time weather data from OpenWeatherMap API
✓ Current weather conditions with temperature
✓ 5-day forecast
✓ Detailed weather information (humidity, wind, sunrise/sunset, etc.)
✓ Search any city worldwide
✓ Beautiful modern dashboard UI

INSTALLATION:

1. Run WeatherDashboard.exe

SETUP:

1. Click "⚙️ Settings" button
2. Get a FREE API key:
   - Go to: https://openweathermap.org/api
   - Sign up for free account
   - Create an API key
3. Paste API key into the Settings dialog
4. Click "Save"

HOW TO USE:

1. Enter a city name in the search box
2. Press Enter or click "Search"
3. View current weather and 5-day forecast
4. Click "⚙️ Settings" to change API key or preferences

WHAT YOU'LL SEE:

Current Weather Section:
- City name and country
- Current temperature
- Weather description (Sunny, Rainy, etc.)
- Feels like temperature

Weather Details:
- Humidity percentage
- Atmospheric pressure
- Wind speed
- Visibility distance
- Sunrise and sunset times
- Cloud coverage percentage

5-Day Forecast:
- Daily high and low temperatures
- Weather conditions
- Precipitation chance
- Day and date

TROUBLESHOOTING:

If you see "API Key Error":
- You haven't set up an API key yet
- Click Settings and enter your key
- Make sure the key is valid

If weather doesn't load:
- Check internet connection
- Verify the city name is spelled correctly
- Make sure your API key is active (check openweathermap.org)

If the app crashes:
- Reinstall the application
- Make sure Windows 7 or later is installed

GETTING AN API KEY:

1. Go to: https://openweathermap.org/api
2. Click "Sign Up" 
3. Create free account
4. Go to "API Keys" section
5. Copy your key (starts with letters/numbers)
6. Paste into Settings dialog in the app

FREE API includes:
- Unlimited calls
- 5-day forecast
- Current weather for all cities
- Minute by minute accuracy

For more info, visit: https://github.com/harisviennas-rgb/ocr-typer
"""
    
    with open(f'{zip_name}/README.txt', 'w') as f:
        f.write(readme_content)
    
    # Create quick start guide
    quickstart_content = """QUICK START GUIDE
=================

STEP 1: Get API Key (2 minutes)
==============================
1. Open browser: https://openweathermap.org/api
2. Click "Sign Up" 
3. Fill in email, password, username
4. Check email and verify account
5. Login to your account
6. Click "API Keys" in left menu
7. Copy the key (Default key is shown)

STEP 2: Set API Key in App (1 minute)
=====================================
1. Run WeatherDashboard.exe
2. Click "⚙️ Settings" button (top right)
3. Paste your API key into the text field
4. Click "Save"

STEP 3: Use the Dashboard (now!)
================================
1. Type a city name (e.g., "New York", "London", "Tokyo")
2. Press Enter or click "Search"
3. See current weather and 5-day forecast

SEARCHING FOR CITIES:

- Use city name: "London"
- Use city and country: "London, UK"
- Works for ANY city worldwide
- Auto-completes major cities

WEATHER INFORMATION:

Current Weather Shows:
- Temperature in Celsius/Fahrenheit
- Weather condition (Clear, Rainy, Cloudy, etc.)
- "Feels like" temperature
- Humidity
- Wind speed
- Visibility
- Sunrise/Sunset times
- Cloud coverage

Forecast Shows:
- High and low temperatures
- Weather conditions
- Rain probability
- For 5 days ahead

TIPS:

- Refresh: Search the city again for latest data
- Change units: Go to Settings to switch Celsius/Fahrenheit
- Favorites: Browser history remembers your searches
- Offline: App needs internet to fetch weather data

NO COST:
Free API with no credit card required!

ENJOY YOUR WEATHER DASHBOARD! 🌤️
"""
    
    with open(f'{zip_name}/QUICK_START.txt', 'w') as f:
        f.write(quickstart_content)
    
    # Zip the folder
    print(f"Creating {zip_name}.zip...")
    shutil.make_archive(zip_name, 'zip', '.', zip_name)
    print(f"✓ Created {zip_name}.zip")
    
    print("\n[5/5] Finalizing...")
    
    # Create summary file
    summary = f"""BUILD COMPLETE!
===============

Generated Files:
✓ dist/WeatherDashboard.exe - Main executable (ready to use!)
✓ {zip_name}.zip - Portable version with documentation

To use:
1. Run WeatherDashboard.exe
2. Click Settings and add your OpenWeatherMap API key
3. Search for any city to see weather!

Get FREE API Key:
https://openweathermap.org/api (2 minute signup)

FEATURES:
✓ Current weather conditions
✓ 5-day forecast
✓ Search any city worldwide
✓ Beautiful modern UI
✓ Detailed weather metrics
✓ No cost, free API

Next steps:
1. Get free API key from openweathermap.org
2. Run WeatherDashboard.exe
3. Add API key in Settings
4. Search for cities and view weather!

Enjoy! 🌤️
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
