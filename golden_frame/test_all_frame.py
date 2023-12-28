#!/usr/bin/python3

import os
os.environ["DEV"] = "1"

if True:
    from golden_frame.lib import build_from_preset

os.makedirs("out", exist_ok=True)

frames = list(filter(lambda x: not x.endswith(
    ".json") and not x.startswith("."), os.listdir("golden_frame/assets")))

input_image = input("Input Image: ")

for frame in frames:
    output_name = ".".join(frame.split(".")[:-1]) + ".png"
    build_from_preset(frame, input_image, f"out/{output_name}", 0)
