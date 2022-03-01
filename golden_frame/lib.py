from typing import List, Tuple, Union
import cv2
import numpy as np
import json


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
    px, py = pic.shape[0:2]

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


def loadConfig(name: str) -> str:
    with open(".".join(name.split(".")[:-1]) + ".json") as f:
        return json.load(f)["pos"]


def buildFromPreset(frame: str, image: str, out: str, opt=PosOptions.CENTER):
    cfg = loadConfig(frame)
    outim = buildGoldenFrame(cv2.imread(frame), cv2.imread(image),
                             list(int(k) for k in cfg.split(",")), opt)

    cv2.imwrite(out, outim)
