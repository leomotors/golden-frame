#!/usr/bin/env python3

import typer
import os

if os.environ.get("DEBUG") is None:
    from golden_frame.lib import PosOptions, buildFromPreset, listFrames
else:
    print("[DEBUG] Only use this mode for local development")
    from lib import PosOptions, buildFromPreset, listFrames

app = typer.Typer()


@app.command()
def build(frame_name: str, input: str, output="output.png", pos=PosOptions.CENTER):
    """Build the Golden Frame

    Args:

        frame_name (str): Name of Template Frame

        input (str): Location of your Image

        output (str, optional): Output Location. Defaults to "output.png".

        pos (0 | 1 | 2, optional): Position Type CENTER = 0, START = 1, END = 2. Defaults to CENTER.
    """
    buildFromPreset(frame_name, input, output, pos)


@app.command()
def list():
    """Print List of Available Frames
    """
    print(listFrames())


def main():
    app()


if __name__ == "__main__":
    main()
