from dataclasses import dataclass
from typing import Dict, List
import json
import os

import cv2
import numpy as np


from pkg_resources import get_distribution, DistributionNotFound

ASSET_PATH = "golden_frame/assets"

if os.getenv("USELOCAL") is None:
    try:
        location = get_distribution("golden-frame").location
        ASSET_PATH = os.path.join(location, "golden_frame/assets")
    except DistributionNotFound:
        pass


def crop_to_ratio(source_image: np.ndarray, ratio: float) -> np.ndarray:
    # From Copilot

    height, width = source_image.shape[:2]
    target_ratio = width / height

    if target_ratio > ratio:
        new_width = int(height * ratio)
        start_x = (width - new_width) // 2
        end_x = start_x + new_width
        cropped_image = source_image[:, start_x:end_x]
    else:
        new_height = int(width / ratio)
        start_y = (height - new_height) // 2
        end_y = start_y + new_height
        cropped_image = source_image[start_y:end_y, :]

    return cropped_image


def build_frame(
    source_image: np.ndarray,
    frame_image: np.ndarray,
    frame_marks: List[List[int]],
    target_resolution=720,
    crop=True,
) -> np.ndarray:
    if crop:
        ratio = calc_aspect_ratio(frame_marks)
        source_image = crop_to_ratio(source_image, ratio)

    # Scale Frame to match size requirements
    #   - Scale to match height
    #   - Calculate change of x point and y point to shift position mark on frame
    og_height, og_width = frame_image.shape[0:2]
    target_frame_dim = (og_width * target_resolution // og_height,
                        target_resolution) if og_width > og_height else (target_resolution, og_height * target_resolution // og_width)
    frame_image = cv2.resize(
        frame_image, target_frame_dim)

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


def get_target_resolution(res: int, config: Dict, frame_image: np.ndarray) -> int:
    if res >= 0 and res < 360:
        res = min(
            frame_image.shape[0], frame_image.shape[1]) * config.get("defaultMultiplier", 1)
    if res < 0:
        res = min(
            frame_image.shape[0], frame_image.shape[1]) * -res

    return res


def build_from_preset(
        frame: str, image: str, out: str, res=0, crop=True):
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

    cfg = load_config(frame)

    res = get_target_resolution(res, cfg, frame_image)

    outim = build_frame(input_image, frame_image, cfg["pos"], res, crop)
    try:
        cv2.imwrite(out, outim)
    except:
        print(f"Error writing Image!")


def calc_aspect_ratio(pos: List[List[int]]) -> float:
    # From Copilot

    return np.linalg.norm(
        np.array(pos[0]) - np.array(pos[1])) / np.linalg.norm(
            np.array(pos[0]) - np.array(pos[3]))  # type: ignore


@dataclass
class FrameInfo:
    name: str
    description: str
    ratio: float
    default_multiplier: int = 1


def load_config(name: str) -> Dict:
    with open(".".join(name.split(".")[:-1]) + ".json") as f:
        return json.load(f)


def import_frame(path: str) -> FrameInfo:
    cfg = load_config(path)
    return FrameInfo(
        path.split("/")[-1],
        cfg["name"],
        calc_aspect_ratio(cfg['pos']),
        cfg.get('defaultMultiplier', None)
    )


def list_frames() -> List[FrameInfo]:
    items = list(filter(lambda x: not x.endswith(
        ".json") and not x.startswith("."), os.listdir(ASSET_PATH)))

    return list(map(lambda item: import_frame(f"{ASSET_PATH}/{item}"), items))


def list_frames_str() -> str:
    items = list_frames()

    text = f"There are {len(items)} frames available.\n"

    for item in items:
        text += f"\n{item.name} ({item.ratio:.3f}:1, {item.default_multiplier or 1}x) : {item.description}"

    return text
