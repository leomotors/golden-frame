#!/usr/bin/env python3

import typer

from golden_frame.lib import PosOptions, buildFromPreset

app = typer.Typer()


@app.command()
def build(frame_name: str, input: str, output="output.png", pos=PosOptions.CENTER):
    buildFromPreset(frame_name, input, output, pos)


def main():
    app()


if __name__ == "__main__":
    main()
