from flask import Flask, render_template
import requests
from datetime import datetime  # Import the datetime module

app = Flask(__name__)

@app.route('/')
def send_request():
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
