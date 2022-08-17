#!/usr/bin/env python3

# pylint: disable=import-error

import os
import typer

if os.environ.get("DEBUG") is None:
    from golden_frame.lib import PosOptions, buildFromPreset, listFrames
else:
    print("[DEBUG] Only use this mode for local development")
    from lib import PosOptions, buildFromPreset, listFrames

app = typer.Typer()


@app.command()
def build(frame_name: str, input: str, output="output.png",
          pos=PosOptions.CENTER, res=720):
    """Build the Golden Frame

    Args:

        frame_name (str): Name of Template Frame

        input (str): Location of your Image

        output (str, optional): Output Location. Defaults to "output.png".

        pos (0 | 1 | 2, optional): Position Type CENTER = 0, START = 1, END = 2. Defaults to CENTER.

        res (int, optional): Minimum size of image
    """
    buildFromPreset(frame_name, input, output, int(pos), int(res))


@app.command()
def list():
    """Print List of Available Frames
    """
    print(listFrames())


def main():
    app()


if __name__ == "__main__":
    main()
