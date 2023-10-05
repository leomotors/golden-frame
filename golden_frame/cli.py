#!/usr/bin/env python3


import os
import typer
from golden_frame.lib import build_from_preset, listFrames

app = typer.Typer()

@app.command()
def build(
    frame_name: str,
    input: str,
    output: str = "output.png",
    res: int = 720
):
    """
    Build the Golden Frame

    Args:
        frame_name (str): Name of Template Frame
        input (str): Location of your Image
        output (str, optional): Output Location. Defaults to "output.png".
        res (int, optional): Minimum size of image. Defaults to 720.
    """
    build_from_preset(frame_name, input, output, res)


@app.command()
def list():
    """Print List of Available Frames"""
    print(listFrames())


def main():
    app()


if __name__ == "__main__":
    main()
