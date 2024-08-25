import os
import platform
import socket
import psutil
import requests

# Function to gather system information
def gather_system_info():
    info = {}

    # Get basic system information
    info['Operating System'] = platform.system()
    info['OS Version'] = platform.version()
    info['Computer Name'] = socket.gethostname()
    info['IP Address'] = socket.gethostbyname(socket.gethostname())
    info['Processor'] = platform.processor()
    info['Architecture'] = platform.machine()

    # Get memory and CPU usage
    info['Total RAM'] = f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB"
    info['Available RAM'] = f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB"
    info['CPU Usage'] = f"{psutil.cpu_percent(interval=1)}%"

    return info

# Function to send the information to a webhook
def send_info_to_webhook(info, webhook_url):
    try:
        response = requests.post(webhook_url, json=info)
        if response.status_code == 200:
            print("Information sent successfully!")
        else:
            print(f"Failed to send information. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function
if __name__ == "__main__":
    # Gather system information
    system_info = gather_system_info()

    # Replace with your webhook URL
    webhook_url = "https://webhook.site/4868fc8d-fedd-49b8-be58-e4f49fa0a4cf"

    # Send the information to your webhook
    send_info_to_webhook(system_info, webhook_url)
