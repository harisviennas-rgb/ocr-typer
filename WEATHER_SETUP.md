# Weather Dashboard - Quick Start Guide

## 🌤️ What is Weather Dashboard?

A beautiful, modern application that shows:
- **Current Weather** - Temperature, conditions, feels like
- **Weather Details** - Humidity, wind speed, sunrise/sunset, visibility, pressure
- **5-Day Forecast** - Temperature trends and rain probability
- **Search Worldwide** - Find weather for any city on Earth

## 🚀 Quick Start (2 minutes)

### Step 1: Get Your API Key
1. Go to: https://openweathermap.org/api
2. Sign up (FREE - no credit card needed)
3. Go to "API Keys" section
4. Copy your default key

### Step 2: Run the App
1. Run `WeatherDashboard.exe`
2. Click "⚙️ Settings" button (top right)
3. Paste your API key
4. Click "Save"

### Step 3: Search Weather
1. Type a city name (e.g., "New York", "London", "Tokyo")
2. Press Enter or click "Search"
3. See current weather and 5-day forecast!

## 📦 Build EXE from Source

```bash
# 1. Install dependencies
pip install -r requirements_weather.txt

# 2. Build the EXE
python build_weather_exe.py

# 3. Find your EXE in dist/ folder
# dist/WeatherDashboard.exe
```

## 🎯 Features

✅ Real-time weather data from OpenWeatherMap  
✅ Current conditions (temp, description, feels like)  
✅ Detailed metrics (humidity, wind, visibility, pressure)  
✅ 5-day forecast with precipitation chances  
✅ Search any city worldwide  
✅ Beautiful modern dashboard UI  
✅ Settings panel for API key management  
✅ Portable single EXE file  

## 📋 What You'll See

### Current Weather Section:
- City name and country
- Large temperature display
- Weather description (Sunny, Cloudy, Rainy, etc.)
- "Feels like" temperature

### Weather Details:
- 💧 Humidity (percentage)
- 🔽 Pressure (hPa)
- 💨 Wind Speed (m/s)
- 👁️ Visibility (km)
- 🌅 Sunrise time
- 🌇 Sunset time
- ☁️ Cloud coverage (percentage)

### 5-Day Forecast:
- Daily high and low temperatures
- Weather conditions
- Rain probability (💧)
- Day and date

## 🔑 Getting an API Key (Free!)

### Simple Steps:
1. Visit: https://openweathermap.org/api
2. Click "Sign Up"
3. Create account with email
4. Verify your email
5. Login and go to "API Keys" tab
6. Copy the "Default" key shown
7. Paste into app Settings

### Why Free?
- Unlimited API calls on free tier
- Current weather for all cities
- 5-day forecasts
- No credit card required
- No expiration date

## 💡 Usage Tips

### Searching Cities:
- Just city: `"London"`
- City & country: `"London, UK"`
- Works for ANY city worldwide
- Type partial names for suggestions

### Weather Info:
- **Temperature** - Shown in Celsius (°C)
- **Wind Speed** - Meters per second (m/s)
- **Visibility** - Kilometers (km)
- **Pressure** - Hectopascals (hPa)

### Troubleshooting:

**"API Key Error"**
- You haven't set your API key yet
- Click Settings and add your key

**"City Not Found"**
- Check spelling of city name
- Try different city name format

**Weather not loading**
- Check internet connection
- Verify API key is valid
- Try a different city

**App not opening**
- Make sure Windows 7+ is installed
- Try running as Administrator
- Reinstall the application

## 📱 System Requirements

- Windows 7 or later
- Internet connection (for weather data)
- ~100MB disk space
- 512MB RAM minimum

## 📖 File Structure

```
ocr-typer/
├── weather_dashboard.py       # Main application
├── build_weather_exe.py       # EXE builder
├── requirements_weather.txt   # Dependencies
├── WEATHER_SETUP.md          # This file
└── dist/
    └── WeatherDashboard.exe   # Ready to use!
```

## 🔗 Links

- **OpenWeatherMap API**: https://openweathermap.org/api
- **GitHub Repo**: https://github.com/harisviennas-rgb/ocr-typer
- **Weather Data**: Real-time from OpenWeatherMap
- **Free API**: No payment required

## ❓ FAQ

**Q: Is it really free?**  
A: Yes! OpenWeatherMap's free tier includes unlimited API calls.

**Q: Do I need an account?**  
A: Yes, but it's free and takes 2 minutes to create.

**Q: Can I use it offline?**  
A: No, weather data requires internet connection.

**Q: How often is data updated?**  
A: Current weather updates within 10 minutes of request.

**Q: Can I change the temperature to Fahrenheit?**  
A: Go to Settings to switch units.

**Q: Does it work worldwide?**  
A: Yes! Search any city on Earth.

## 🎨 UI Features

- **Dark theme** - Easy on the eyes
- **Blue accent colors** - Modern look
- **Real-time search** - Instant results
- **Responsive design** - Works on any screen size
- **Emoji indicators** - Visual weather info

## 🛠️ Advanced

### Custom API Key Path:
If you want to change the API key location, edit line in settings:
```python
self.save_config()  # Saves to config.json
```

### Running from Source:
```bash
python weather_dashboard.py
```

## 📝 Notes

- Weather data refreshes when you search
- 5-day forecast data included
- Sunrise/sunset times are local to the searched city
- Wind speed shown in meters per second
- Cloud coverage as percentage

---

**Enjoy your weather dashboard! 🌤️**

For issues or questions: https://github.com/harisviennas-rgb/ocr-typer
