import psutil
import time
import requests
import platform
import socket
import json

# Configuration
WEBHOOK_URL = "	https://webhook.site/4868fc8d-fedd-49b8-be58-e4f49fa0a4cf"  # Replace with your server URL

# Function to gather system activities
def gather_activities():
    activities = {
        'CPU Usage': f"{psutil.cpu_percent(interval=1)}%",
        'Memory Usage': f"{psutil.virtual_memory().percent}%",
        'Disk Usage': f"{psutil.disk_usage('/').percent}%",
        'Active Processes': [p.info for p in psutil.process_iter(['pid', 'name'])],
        'System Info': {
            'OS': platform.system(),
            'OS Version': platform.version(),
            'Hostname': socket.gethostname(),
            'IP Address': socket.gethostbyname(socket.gethostname()),
        }
    }
    return activities

# Function to send data to the server
def send_data_to_server(data):
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main loop
if __name__ == "__main__":
    while True:
        activities = gather_activities()
        send_data_to_server(activities)
        time.sleep(60)  # Send data every 60 seconds
