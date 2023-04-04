import cv2
import numpy as np
import requests
import time

from dotenv import dotenv_values

config = {
    **dotenv_values("../.env.prod"),  # load shared development variables
    **dotenv_values("../.env.secret"),  # load sensitive variables
}

# Define constants
FPS = int(config.get('FPS', 30))
SERVER_URL = f"http://{config.get('SERVER_IP','hh.home')}:{config.get('SERVER_PORT',8008)}/process_frame"

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame from camera
    ret, frame = cap.read()

    # If frame capture was successful, send frame to server
    if ret:
        # Resize frame to reduce network traffic
        frame_resized = cv2.resize(frame, (640, 480))

        # Encode frame as JPEG
        _, frame_encoded = cv2.imencode(".jpg", frame_resized)

        # Send frame to server for processing
        response = requests.post(SERVER_URL, data=frame_encoded.tobytes())

        # If server returns a response, print blink rate to console
        if response.status_code == 200:
            blink_rate = float(response.content.decode("utf-8"))
            print(f"Blink rate: {blink_rate:.2f} blinks per minute")

    # Wait for next frame
    time.sleep(1 / FPS)

# Release camera
cap.release()
