# Script Author: Adrian Infante
# Date: November 23, 2023
# Description: This script will take a screenshot from the stream 1 using a Roughneck Vicon camera

import requests
from requests.auth import HTTPDigestAuth  
from PIL import Image
from io import BytesIO
import time
import os

interval = 600 

# ANSI escape codes for colors
GREEN = "\033[92m"
ORANGE = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def save_snapshot(image_data, folder_path, filename):
    image = Image.open(BytesIO(image_data))
    image.save(os.path.join(folder_path, filename))

def capture_snapshot(camera_ip, folder_path, username, password):
    while True:
        try:
            response = requests.get(f"http://{camera_ip}/cgi-bin/snapshot.cgi", auth=HTTPDigestAuth(username, password))
            
            if response.status_code == 200:
                # Save the snapshot to a local folder
                timestamp = time.strftime("%Y%m%d%H%M%S")
                filename = f"ManchesterCentral_{timestamp}.jpg"
                save_snapshot(response.content, folder_path, filename)
                print(f"{GREEN}Snapshot saved: {filename}{RESET}")
                print(f"{ORANGE}Waiting {interval} seconds{RESET}")
            else:
                print(f"{RED}Error: Unable to capture snapshot. Status code: {response.status_code}{RESET}")
        except Exception as e:
            print(f"{RED}Error: {str(e)}{RESET}")

        # Wait for X seconds before sending the next request
        time.sleep(interval)

if __name__ == "__main__":
    # Set the folder name
    folder_name = "Screenshots"

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the local folder if it doesn't exist
    folder_path = os.path.join(script_dir, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Camera info
    camera_ip = "10.253.1.214"
    username = "ADMIN"  #Default camera password
    password = "1234"  #Default camera password

    print(" Script Author: Adrian Infante \n Date: November 23, 2023 \n Description: This script will take a screenshot from the stream 1 using a Roughneck Vicon camera")

    # Start capturing 
    capture_snapshot(camera_ip, folder_path, username, password)
