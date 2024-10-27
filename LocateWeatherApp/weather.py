import customtkinter  # type: ignore
from PIL import ImageTk, Image  # type: ignore
import requests  # type: ignore
import configparser
from datetime import datetime
import geopy.geocoders  # type: ignore
from geopy.geocoders import Nominatim

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')
api_key = "#Add Api Key Here"
url_current = 'http://api.openweathermap.org/data/2.5/weather'
url_forecast = 'http://api.openweathermap.org/data/2.5/forecast'
iconUrl = 'http://openweathermap.org/img/wn/{}@2x.png'

# App UI
app = customtkinter.CTk()
app.geometry('350x600')
app.title('Weather App')

# Toggle for Celsius/Fahrenheit
is_celsius = True
is_on = False
search_history = []

def getweather(city):
    try:
        params = {'q': city, 'appid': api_key, 'units': 'metric' if is_celsius else 'imperial', 'lang': 'en'}
        data = requests.get(url_current, params=params).json()
        
        if data.get("cod") != 200:
            locationLabel.configure(text=f"City '{city}' not found.")
            return None

        weather_details = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon'],
            'condition': data['weather'][0]['description'],
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
        }
        return weather_details

    except Exception as e:
        print(f"Error retrieving data: {e}")
        locationLabel.configure(text="Error retrieving data.")
        return None

def get_forecast(city):
    try:
        params = {'q': city, 'appid': api_key, 'units': 'metric' if is_celsius else 'imperial'}
        data = requests.get(url_forecast, params=params).json()
        if data.get("cod") != "200":
            return None
        
        forecast = [
            {
                'temp': item['main']['temp'],
                'condition': item['weather'][0]['description'],
                'time': item['dt_txt'],
                'icon': item['weather'][0]['icon']
            }
            for item in data['list'][0:5]
        ]
        return forecast

    except Exception as e:
        print(f"Error retrieving forecast: {e}")
        return None

def toggle_temp_unit():
    global is_celsius
    is_celsius = not is_celsius
    temp_unit_button.configure(text="°C" if is_celsius else "°F")
    if cityEntry.get():
        main()

def detect_location():
    geolocator = Nominatim(user_agent="weatherApp")
    location = geolocator.geocode("Tanzania")
    if location:
        getweather(location.address)

def main():
    city = cityEntry.get()
    if city:
        search_history.append(city)
        weather = getweather(city)
        forecast = get_forecast(city)

        if weather:
            locationLabel.configure(text=f"{weather['city']}, {weather['country']}")
            tempLabel.configure(text=f"{weather['temp']}°{'C' if is_celsius else 'F'}")
            conditionLabel.configure(text=weather['condition'].capitalize())
            humidityLabel.configure(text=f"Humidity: {weather['humidity']}%")
            windLabel.configure(text=f"Wind: {weather['wind_speed']} km/h")
            sunriseLabel.configure(text=f"Sunrise: {weather['sunrise']}")
            sunsetLabel.configure(text=f"Sunset: {weather['sunset']}")

            icon = customtkinter.CTkImage(Image.open(requests.get(iconUrl.format(weather['icon']), stream=True).raw), size=(100, 100))
            iconLabel.configure(image=icon)
            iconLabel.image = icon

            # Display 5-day forecast
            forecastLabel.configure(text="5-Day Forecast:")
            forecast_data = ""
            for day in forecast:
                forecast_data += f"{day['time'][:10]} - {day['temp']}°{ 'C' if is_celsius else 'F' }, {day['condition']}\n"
            forecastText.configure(text=forecast_data)

def toggle_theme():
    global is_on
    is_on = not is_on
    button.configure(text="Light Mode" if is_on else "Dark Mode")
    customtkinter.set_appearance_mode("light" if is_on else "dark")

# Interface
cityEntry = customtkinter.CTkEntry(app, justify='center', placeholder_text="Enter City Name")
cityEntry.pack(fill=customtkinter.BOTH, ipady=10, padx=18, pady=5)
cityEntry.focus()

cityEntry.bind('<Return>', lambda event: main())
searchButton = customtkinter.CTkButton(app, text='Search', font=('Arial', 15), command=main)
searchButton.pack(fill=customtkinter.BOTH, ipady=10, padx=20)

# Location detection
locationButton = customtkinter.CTkButton(app, text="Use My Location", font=('Arial', 10), command=detect_location)
locationButton.pack(ipady=5, padx=18, pady=5)

# Theme Toggle Button
button = customtkinter.CTkButton(app, text="Dark Mode", command=toggle_theme)
button.pack(ipady=10, padx=18, pady=5)

# Temperature Unit Toggle
temp_unit_button = customtkinter.CTkButton(app, text="°C", command=toggle_temp_unit)
temp_unit_button.pack(ipady=5, padx=18, pady=5)

# Weather Info Labels
iconLabel = customtkinter.CTkLabel(app, text="", width=80, height=80)
iconLabel.pack()
locationLabel = customtkinter.CTkLabel(app, font=('Arial', 30), text="")
locationLabel.pack()
tempLabel = customtkinter.CTkLabel(app, font=('Arial', 15, 'bold'), text="")
tempLabel.pack()
conditionLabel = customtkinter.CTkLabel(app, font=('Arial', 20), text="")
conditionLabel.pack()
humidityLabel = customtkinter.CTkLabel(app, font=('Arial', 12), text="")
humidityLabel.pack()
windLabel = customtkinter.CTkLabel(app, font=('Arial', 12), text="")
windLabel.pack()
sunriseLabel = customtkinter.CTkLabel(app, font=('Arial', 12), text="")
sunriseLabel.pack()
sunsetLabel = customtkinter.CTkLabel(app, font=('Arial', 12), text="")
sunsetLabel.pack()

# Forecast Labels
forecastLabel = customtkinter.CTkLabel(app, font=('Arial', 15), text="5-Day Forecast:")
forecastLabel.pack(pady=10)
forecastText = customtkinter.CTkLabel(app, font=('Arial', 10), text="", wraplength=300)
forecastText.pack()

app.mainloop()
