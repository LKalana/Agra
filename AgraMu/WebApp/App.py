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
        # There is an issue with adding Rain guage data.
        #rain = weather_data['rain']['1h']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        city_ = weather_data['name']
        city_info = f'{city_}' # If you want to show this, Add it to return html_render.
        weather_description = weather_data['weather'][0]['description']
        weather_info = f'Temperature: {temperature}°C, Humidity: {humidity} g.m-3, Description: {weather_description}'
    except Exception as e:
        weather_info = f'Error fetching weather data: {e}'

    try:
        # Send a request to the ESP8266 server
        server_ip = "192.168.1.156"
        server_port = 80
        url = f"http://{server_ip}:{server_port}/"
        response = requests.get(url)
        if response.status_code == 200:
            # If the response is successful, extract the server response
            server_response = response.text
            # Create a new ServerResponse object and add it to the database
            new_response = ServerResponse(response_text=server_response)
            db.session.add(new_response)
            db.session.commit()
        else:
            # If there's an error in the response, display an error message
            server_response = f"Error: {response.status_code} - {response.text}"
    except requests.ConnectionError as e:
        # If there's an error connecting to the server, display the connection error
        server_response = f"Error connecting to the server: {e}"

    # Add a timestamp to the server response
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #server_response_with_timestamp = f"{timestamp} - {server_response}"
    # Render the HTML template with the server response and weather information
    return render_template('index.html', server_response=server_response, time_info = timestamp, weather_info = weather_info, city_info = city_info)

if __name__ == "__main__":
    # Run the Flask app on port 5000 with debug mode enabled
    app.run(port=5000, debug=True)
