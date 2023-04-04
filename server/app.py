from datetime import datetime

import cv2
from flask import Flask, request, jsonify
from blink_detector import BlinkDetector
import numpy as np


# Initialize Flask app
app = Flask(__name__)

# Initialize blink detector
blink_detector = BlinkDetector()
blinks = {}
frames = {}

@app.route("/process_frame", methods=["POST"])
def process_frame():
    # Decode frame from request
    dt = datetime.now()
    frame_encoded = np.frombuffer(request.data, np.uint8)
    frame = cv2.imdecode(frame_encoded, cv2.IMREAD_COLOR)

    # Detect blinks in the frame and return blink rate as JSON response
    blinks[(dt.hour, (dt.minute % 15) * 15)] = blinks.get((dt.hour, (dt.minute % 15) * 15), 0)
    frames[(dt.hour, (dt.minute % 15) * 15)] = blinks.get((dt.hour, (dt.minute % 15) * 15), 0)

    if blink_detector.detect_blinks(frame):
        blinks[(dt.hour, (dt.minute % 15) * 15)] = blinks.get((dt.hour, (dt.minute % 15) * 15), 0) + 1

    frames[(dt.hour, (dt.minute % 15) * 15)] = frames.get((dt.hour, (dt.minute % 15) * 15), 0) + 1

    return jsonify({"success": True})

@app.route('/blink_rate')
def blink_rate_report():
    return jsonify({'blinks': blinks, 'frames': frames})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
