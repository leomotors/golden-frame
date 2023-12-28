# pylint: disable=no-member

from waitress import serve
from flask import Flask, request, Response
from datetime import datetime
import io
import os

import cv2
import numpy as np

import os
os.environ["USELOCAL"] = "1"

if True:
    from lib import ASSET_PATH, build_frame, get_target_resolution, list_frames,  load_config

app = Flask(__name__)

PASSWORD = os.getenv("PASSWORD")

if PASSWORD is None or len(PASSWORD) < 6:
    raise Exception("PASSWORD environment variable is not set or too weak!")


def build_golden_frame(frame_name: str, input_image: np.ndarray, res: int, crop: bool):
    frame_path = os.path.join(ASSET_PATH, frame_name)
    frame_image = cv2.imread(frame_path)
    cfg = load_config(frame_path)

    target_resolution = get_target_resolution(res, cfg, frame_image)

    out_image = build_frame(
        source_image=input_image,
        frame_image=frame_image,
        frame_marks=load_config(frame_path)["pos"],
        target_resolution=target_resolution,
        crop=crop,
    )

    return out_image


def line_to_json(line: str):
    tokens = line.split(":")
    name = ":".join(tokens[:2]).strip()
    name_tokens = name.split(" ")
    description = tokens[2].strip()

    return {
        "name": name_tokens[0].strip(),
        "description": description,
        "ratio": float(name_tokens[1].strip()[1:].split(":")[0])
    }


def list_frame_json():
    frames = list_frames()
    items = list(map(line_to_json, filter(
        lambda x: len(x), frames.split("\n")[1:])))

    return items


@app.route("/", methods=["GET"])
def get_frames():
    return list_frame_json(), 200


@app.route("/health", methods=["GET"])
def get_health():
    return "OK", 200


ALLOWED_FILE_TYPES = set(
    ["image/jpeg", "image/png", "image/webp", "image/avif"])


@app.route("/", methods=["POST"])
def handle_post():
    if PASSWORD is None or len(PASSWORD) < 6:
        return "Internal Server Error (Magic)", 500

    # * Get password and confirm access
    password = request.headers.get("Authorization")
    if password != PASSWORD:
        return "Unauthorized", 401

    # * Get files
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    if not file or file.filename == "":
        return "No file selected", 400

    filetype = file.content_type
    if filetype not in ALLOWED_FILE_TYPES:
        return "Invalid file type", 400

    # * Get frame name
    frame_name = request.form.get("frame_name")

    if frame_name is None:
        return "No frame name selected", 400

    if not any(map(lambda x: x["name"] == frame_name, list_frame_json())):
        return "Invalid frame name", 400

    # * Get resolution option
    resolution = request.form.get("resolution") or 0
    try:
        res_int = int(resolution)
    except ValueError:
        return "Invalid resolution", 400

    if res_int < -5:
        return "Resolution multipler too big, must not exceed x5", 400

    if 0 < res_int < 360:
        return "Resolution too small, must be at least 360", 400

    if res_int > 4000:
        return "Resolution too big, must not exceed 4000", 400

    # * Get No Crop options
    nocrop = request.form.get("nocrop")
    crop = nocrop is None or len(nocrop) < 1

    # Read the image file as bytes
    image_bytes = file.read()

    # Convert the image bytes to a NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the NumPy array into an OpenCV image
    input_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if input_image is None:
        return "Unable to parse input image", 400

    # Run the command
    out_image = build_golden_frame(frame_name, input_image, res_int, crop)

    # Create a response stream
    response_stream = io.BytesIO()

    ret, encoded_img = cv2.imencode(".png", out_image)
    response_stream.write(encoded_img.tobytes())

    # Set the appropriate headers for the response
    headers = {
        "Content-Disposition": f"attachment; filename=${file.filename}.out.png",
        "Content-Type": "image/png"
    }

    # Return the response with the image stream
    return Response(response_stream.getvalue(), headers=headers)


def getIP():
    return request.headers.get("cf-connecting-ip") or request.headers.get(
        "x-real-ip") or request.remote_addr


@app.after_request
def log_response(response):
    if request.path == "/health" and request.headers.get("Authorization") == PASSWORD:
        return response

    now = datetime.now()
    print(f"[{now.strftime('%d/%m/%Y %H:%M:%S')}] {getIP()} -> {request.method} {request.path} {response.status_code}")
    return response


PORT = 3131

if os.getenv("DEV"):
    app.run(host="0.0.0.0", port=PORT, debug=True)
else:
    print(f"Starting server on port {PORT}")
    serve(app, host="0.0.0.0", port=PORT)
