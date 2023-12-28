#!/usr/bin/env python3

import typer
from golden_frame.lib import build_from_preset, list_frames

app = typer.Typer()


@app.command()
def build(
    frame_name: str,
    input: str,
    output: str = "output.png",
    res: int = 720,
    crop: bool = True
):
    """
    Build the Golden Frame

    Args:
        frame_name (str): Name of Template Frame
        input (str): Location of your Image
        output (str, optional): Output Location. Defaults to "output.png".
        res (int, optional): Minimum size of image. Defaults to 720.
        crop (bool, optional): Crop image instead of stretching. Defaults to True.
    """
    build_from_preset(frame_name, input, output, res, crop)


@app.command()
def list():
    """Print List of Available Frames"""
    print(list_frames())


@app.command()
def version():
    from importlib.metadata import version
    print(version("golden_frame"))


def main():
    app()


if __name__ == "__main__":
    main()
