from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)

# Configure the SQLite database URI. You can replace this with the URI for your preferred database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///responses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create an instance of the SQLAlchemy class without attaching it to the app
db = SQLAlchemy()

# Initialize the app with the db instance
db.init_app(app)

# Define a model for the ServerResponse table
class ServerResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    response_text = db.Column(db.String(255))

# Notify Flask to create all the tables
with app.app_context():
    db.create_all()

global city  
city = 'Colombo' # Desired city of location.
# Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
OPENWEATHERMAP_API_KEY = '6d589d7482d994ee8dfcca1280624de7'
CITY_NAME = city  # Replace with the name of the city you want weather data for

@app.route('/')
def send_request():
    # Get weather data from OpenWeatherMap API
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    weather_response = requests.get(weather_url)
    # To read the JSON of Openwethermap, use below link.
    # https://openweathermap.org/current
    try:
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        city_ = weather_data['name']
        weather_main = weather_data['weather'][0]['main']
        weather_description = weather_data['weather'][0]['description']
        city_info = f'{city_}' # If you want to show this, Add it to return html_render.
        weather_info = f'Temperature: {temperature}°C, Humidity: {humidity} g.m-3, Main Weather: {weather_main}, Description: {weather_description}'
    except Exception as e:
        weather_info = f'Error fetching weather data: {e}'
    
    # Extract rain information
    rain_info_1h = weather_data.get("rain", {}).get("1h", "No rain gauge data")
    rain_info_main = weather_data['weather'][0]['main']
    rain_info_description = weather_data['weather'][0]['description']
    
    # Add a timestamp to the server response
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a placeholder server response
    server_response = "Field Network Fail"  # You can customize this message
    
    # Render the HTML template with the server response and weather information
    return render_template('index.html', server_response=server_response, time_info=timestamp, weather_info=weather_info, city_info=city_info, rain_info_1h=rain_info_1h, rain_info_main=rain_info_main, rain_info_description=rain_info_description)

if __name__ == "__main__":
    # Run the Flask app on port 5000 with debug mode enabled
    app.run(port=5000, debug=True)
