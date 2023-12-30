from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

@app.route('/')
def send_request():
    import requests

    # Replace with the actual IP address and port of your ESP8266 server
    server_ip = "192.168.1.156"
    server_port = 80

    url = f"http://{server_ip}:{server_port}/"

    try:
        # Send a request to the ESP8266 server
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
    server_response_with_timestamp = f"{timestamp} - {server_response}"

    # Render the HTML template with the server response
    return render_template('index.html', server_response=server_response_with_timestamp)

if __name__ == "__main__":
    # Run the Flask app on port 5000 with debug mode enabled
    app.run(port=5000, debug=True)
