from typing import Dict, List
import json
import os

import cv2
import numpy as np


ASSET_PATH = os.path.join("golden_frame", "assets")

if os.environ.get("DEBUG") is not None:
    ASSET_PATH = "./golden_frame/assets"


def build_frame(
    source_image: np.ndarray,
    frame_image: np.ndarray,
    frame_marks: List[List[int]],
    res=720
) -> np.ndarray:

    # Scale Frame to match size requirements
    #   - Scale to match height
    #   - Calculate change of x point and y point to shift position mark on frame
    og_height, og_width = frame_image.shape[0:2]
    frame_image = cv2.resize(
        frame_image, (frame_image.shape[1]*res//frame_image.shape[0], res))

    # Calculate change of x point and y point to shift position mark on frame
    for mark in frame_marks:
        mark[0] = mark[0]*frame_image.shape[1]//og_width
        mark[1] = mark[1]*frame_image.shape[0]//og_height

    # Calculate width and height of the destination frame & Resize Source Image
    # Convert frame_marks to np.float32
    frame_marks_f32: np.ndarray = np.float32(frame_marks)  # type: ignore
    width = int(max(np.linalg.norm(
        frame_marks_f32[0] - frame_marks_f32[1]), np.linalg.norm(frame_marks_f32[2] - frame_marks_f32[3])))
    height = int(max(np.linalg.norm(
        frame_marks_f32[0] - frame_marks_f32[3]), np.linalg.norm(frame_marks_f32[1] - frame_marks_f32[2])))
    source_image = cv2.resize(source_image, (width, height))

    # Perform Perspective Transformation
    #   - Define source points
    #   - Calculate the perspective transformation matrix
    #   - Apply the perspective transformation
    src_pts: np.ndarray = np.float32(
        [[0, 0], [width, 0], [width, height], [0, height]])  # type: ignore
    M = cv2.getPerspectiveTransform(src_pts, frame_marks_f32)
    warped = cv2.warpPerspective(
        source_image, M, (frame_image.shape[1], frame_image.shape[0]))

    # Create a mask and inverse mask of the warped image
    mask = cv2.warpPerspective(np.ones_like(
        source_image) * 255, M, (frame_image.shape[1], frame_image.shape[0]))
    inv_mask = cv2.bitwise_not(mask)

    # Blend the images
    result = cv2.bitwise_and(frame_image, inv_mask)
    result = cv2.add(result, warped)

    return result


def build_from_preset(
        frame: str, image: str, out: str, res=720):
    frame = f"{ASSET_PATH}/{frame}"

    try:
        frame_image = cv2.imread(frame)
        if not frame_image.data:
            raise
    except:
        print(
            f"ERROR: Cannot Read {frame}! Did you execute this script from correct location and frame name is correct?"
        )
        return

    try:
        input_image = cv2.imread(image)
        if not input_image.data:
            raise
    except:
        print(f"ERROR: Cannot Read Input Image {image}!")
        return

    cfg = load_config(frame)["pos"]
    outim = build_frame(input_image, frame_image, cfg, res)
    try:
        cv2.imwrite(out, outim)
    except:
        print(f"Error writing Image!")


def list_frames() -> str:
    import os
    items = list(filter(lambda x: not x.endswith(
        ".json"), os.listdir(ASSET_PATH)))

    text = f"There are {len(items)} frames available.\n"

    for item in items:
        cfg = load_config(f"{ASSET_PATH}/{item}")
        text += f"\n{item} : {cfg['name']}"

    return text


def load_config(name: str) -> Dict:
    with open(".".join(name.split(".")[:-1]) + ".json") as f:
        return json.load(f)
