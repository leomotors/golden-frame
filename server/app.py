# pylint: disable=no-member

import io
import os
import cv2
import numpy as np
from golden_frame.lib import buildGoldenFrame, listFrames, ASSET_PATH, loadConfig, PosOptions

from flask import Flask, request, Response

from dotenv import load_dotenv

load_dotenv()

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


def build_golden_frame(frame_name: str, input_img: np.ndarray):
    frame_path = f"{ASSET_PATH}/{frame_name}"
    frameimg = cv2.imread(frame_path)
    cfg = loadConfig(frame_path)["pos"]

    out_image = buildGoldenFrame(frame=frameimg, picture=input_img, pos=list(
        int(k) for k in cfg.split(",")), posOption=PosOptions.CENTER)

    return out_image


def listFramesJson():
    frames = listFrames()
    items = list(map(line_to_json, filter(
        lambda x: len(x), frames.split("\n")[1:])))

    return items


@app.route("/", methods=["GET"])
def get_frames():
    return listFramesJson(), 200


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

    if not any(map(lambda x: x['name'] == frame_name, listFramesJson())):
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


app.run(host="0.0.0.0", port=3131, debug=True)
