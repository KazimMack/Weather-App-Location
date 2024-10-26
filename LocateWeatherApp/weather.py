import customtkinter  # type: ignore
from PIL import ImageTk, Image  # type: ignore
import requests  # type: ignore

# API Key and URL setup
api_key = '#Add Api Key Here'
url = 'http://api.openweathermap.org/data/2.5/weather'
iconUrl = 'http://openweathermap.org/img/wn/{}@2x.png'

# Initialize the customtkinter app
app = customtkinter.CTk()
app.geometry('300x450')
app.title('Weather App')

# Function to retrieve weather information for a city
def getweather(city):
    try:
        params = {'q': city, 'appid': api_key, 'lang': 'en'}
        data = requests.get(url, params=params).json()
        if data and data.get('cod') == 200:
            city = str(data['name']).title()
            country = data['sys']['country']
            temp = int(data['main']['temp'] - 273.15)  # Convert from Kelvin to Celsius
            icon = data['weather'][0]['icon']
            condition = data['weather'][0]['description']
            return (city, country, temp, icon, condition)
        else:
            print(f"No data available for '{city}'.")
    except requests.RequestException as e:
        print("Error retrieving data:", e)
    except KeyError:
        print("Unexpected response format.")
    return None

# Function to update the UI with the weather data
def main():
    city = cityEntry.get()
    weather = getweather(city)
    if weather:
        locationLabel.configure(text=f"{weather[0]}, {weather[1]}")
        tempLabel.configure(text=f"{weather[2]}°C")
        conditionLabel.configure(text=weather[4])
        icon = customtkinter.CTkImage(
            Image.open(requests.get(iconUrl.format(weather[3]), stream=True).raw), size=(100, 100)
        )
        iconLabel.configure(image=icon)
        iconLabel.image = icon

# Dark & Light Mode Button function
is_on = False
def toggle():
    global is_on
    is_on = not is_on
    if is_on:
        button.configure(text="Dark Mode")
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")
    else:
        button.configure(text="Light Mode")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

# UI components
cityEntry = customtkinter.CTkEntry(app, justify='center', placeholder_text="Enter City Name")
cityEntry.pack(fill=customtkinter.BOTH, ipady=10, padx=18, pady=5)
cityEntry.focus()
cityEntry.bind('<Return>', lambda event: main())  # Add enter key event

searchButton = customtkinter.CTkButton(app, text='Search', font=('Arial', 15), command=main)
searchButton.pack(fill=customtkinter.BOTH, ipady=10, padx=20)

button = customtkinter.CTkButton(app, text="Dark Mode", command=toggle)
button.pack(ipady=10, padx=18, pady=5)

iconLabel = customtkinter.CTkLabel(app, text="", width=80, height=80)
iconLabel.pack()

locationLabel = customtkinter.CTkLabel(app, font=('Arial', 30), text="")
locationLabel.pack()

tempLabel = customtkinter.CTkLabel(app, font=('Arial', 15, 'bold'), text="")
tempLabel.pack()

conditionLabel = customtkinter.CTkLabel(app, font=('Arial', 20), text="")
conditionLabel.pack()

app.mainloop()
