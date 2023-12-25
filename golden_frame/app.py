# pylint: disable=no-member

import io
import os
import cv2
import numpy as np
from lib import build_frame, list_frames, ASSET_PATH, load_config
from datetime import datetime

from flask import Flask, request, Response
from waitress import serve

app = Flask(__name__)

PASSWORD = os.getenv("PASSWORD")

if PASSWORD is None or len(PASSWORD) < 1:
    print("WARN: Password is not set")


def line_to_json(line: str):
    tokens = line.split(":")

    return {
        "name": tokens[0].strip(),
        "description": tokens[1].strip()
    }


def build_golden_frame(frame_name: str, input_image: np.ndarray):
    frame_path = os.path.join(ASSET_PATH, frame_name)
    frame_image = cv2.imread(frame_path)

    out_image = build_frame(
        source_image=input_image,
        frame_image=frame_image,
        frame_marks=load_config(frame_name)["pos"]
    )
    return out_image


def list_frame_json():
    frames = list_frames()
    items = list(map(line_to_json, filter(
        lambda x: len(x), frames.split("\n")[1:])))

    return items


@app.route("/", methods=["GET"])
def get_frames():
    return list_frame_json(), 200


@app.route("/", methods=["POST"])
def build_frame():
    if PASSWORD:
        password = request.headers.get("Authorization")
        if password != PASSWORD:
            return "Unauthorized", 401

    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    if not file or file.filename == '':
        return 'No file selected', 400

    frame_name = request.form.get('frame_name')

    if frame_name is None:
        return 'No frame name selected', 400

    if not any(map(lambda x: x['name'] == frame_name, list_frame_json())):
        return 'Invalid frame name', 400

    # Read the image file as bytes
    image_bytes = file.read()

    # Convert the image bytes to a NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the NumPy array into an OpenCV image
    input_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if input_image is None:
        return 'Not an image', 400

    # Run the command
    out_image = build_golden_frame(frame_name, input_image)

    # Create a response stream
    response_stream = io.BytesIO()

    ret, encoded_img = cv2.imencode('.png', out_image)
    response_stream.write(encoded_img.tobytes())

    # Set the appropriate headers for the response
    headers = {
        'Content-Disposition': f'attachment; filename=${file.filename}.out.png',
        'Content-Type': 'image/png'
    }

    # Return the response with the image stream
    return Response(response_stream.getvalue(), headers=headers)


def getIP():
    return request.headers.get("cf-connecting-ip") or request.headers.get(
        "x-real-ip") or request.remote_addr


@app.after_request
def log_response(response):
    now = datetime.now()
    print(f"[{now.strftime('%d/%m/%Y %H:%M:%S')}] {getIP()} -> {request.method} {request.path} {response.status_code}")
    return response


PORT = 3131

if os.getenv("DEV"):
    app.run(host="0.0.0.0", port=PORT, debug=True)
else:
    print(f"Starting server on port {PORT}")
    serve(app, host="0.0.0.0", port=PORT)
