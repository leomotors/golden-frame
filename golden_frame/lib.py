from typing import Dict, List, Tuple, Union
import cv2
import json
import numpy as np
import os
import pkg_resources

ASSET_PATH = pkg_resources.resource_filename("golden_frame", "assets")

if os.environ.get("DEBUG") is not None:
    ASSET_PATH = "./golden_frame/assets"


class CropOptions:
    CROP = 0
    PRESERVE = 1


class PosOptions:
    CENTER = 0
    START = 1
    END = 2


def getPos(x: Union[int, float], dx: Union[int, float], opt) -> Tuple[int, int]:
    opt = int(opt)
    if(opt == PosOptions.START):
        return 0, round(x)
    elif opt == PosOptions.CENTER:
        return round(dx), round(x+dx)
    elif opt == PosOptions.END:
        return round(2*dx), round(2*dx+x)
    else:
        raise Exception("opt is not valid PosOptions")


def resizeImage(
    pic: np.ndarray,
    size: List[int],
    posOption=PosOptions.CENTER
) -> np.ndarray:
    py, px = pic.shape[0:2]

    ratio = max(size[0]/px, size[1]/py)

    resized = cv2.resize(pic, dsize=(
        round(px*ratio), round(py*ratio)))

    ysize, xsize = resized.shape[0:2]

    dx = (xsize - size[0])/2
    dy = (ysize - size[1])/2

    sx, ex = getPos(size[0], dx, posOption)
    sy, ey = getPos(size[1], dy, posOption)

    return resized[sy:ey, sx:ex]


def buildGoldenFrame(
    frame: np.ndarray,
    picture: np.ndarray,
    pos: List[int],
    posOption=PosOptions.CENTER
) -> np.ndarray:
    resized = resizeImage(
        picture, [pos[2]-pos[0], pos[3]-pos[1]], posOption)
    xstart, ystart = pos[0:2]
    ysize, xsize = resized.shape[0:2]

    # Why can't you use same axis system?
    frame[ystart:ystart+ysize, xstart:xstart+xsize] = resized

    return frame


def loadConfig(name: str) -> Dict:
    with open(".".join(name.split(".")[:-1]) + ".json") as f:
        return json.load(f)


def buildFromPreset(frame: str, image: str, out: str, opt=PosOptions.CENTER):
    frame = f"{ASSET_PATH}/{frame}"

    try:
        frameimg = cv2.imread(frame)
        if not frameimg.data:
            raise
    except:
        print(
            f"ERROR: Cannot Read {frame}! Did you execute this script from correct location and frame name is correct?"
        )
        return

    try:
        inputimg = cv2.imread(image)
        if not inputimg.data:
            raise
    except:
        print(f"ERROR: Cannot Read Input Image {image}!")
        return

    cfg = loadConfig(frame)["pos"]
    outim = buildGoldenFrame(frameimg, inputimg,
                             list(int(k) for k in cfg.split(",")), opt)

    try:
        cv2.imwrite(out, outim)
    except:
        print(f"Error writing Image!")


def listFrames() -> str:
    import os
    items = list(filter(lambda x: not x.endswith(
        ".json"), os.listdir(ASSET_PATH)))

    text = f"There are {len(items)} frames available.\n"

    for item in items:
        cfg = loadConfig(f"{ASSET_PATH}/{item}")
        text += f"\n{item} : {cfg['name']}"

    return text
