#!/usr/bin/env python3
"""Generate the 1280×640 GitHub social preview image."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from theme_engine import load_theme  # noqa: E402


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--themes-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    width, height = 1280, 640
    top, bottom = rgb("#10121c"), rgb("#1a1b2c")
    image = Image.new("RGB", (width, height), top)
    pixels = image.load()
    for y in range(height):
        ratio = y / (height - 1)
        line = tuple(round(top[i] * (1 - ratio) + bottom[i] * ratio) for i in range(3))
        for x in range(width):
            pixels[x, y] = line
    draw = ImageDraw.Draw(image, "RGBA")
    for x in range(0, width, 48):
        draw.line((x, 0, x, height), fill=(192, 202, 245, 10), width=1)
    for y in range(0, height, 48):
        draw.line((0, y, width, y), fill=(192, 202, 245, 10), width=1)
    for radius, alpha in ((280, 14), (205, 22), (125, 30)):
        draw.ellipse((1000 - radius, 70 - radius, 1000 + radius, 70 + radius), fill=(122, 162, 247, alpha))
    draw.rounded_rectangle((72, 70, 119, 76), radius=3, fill="#7aa2f7")
    draw.text((72, 104), "KALI // OMARCHY", font=font(60, True), fill="#c0caf5")
    draw.text((75, 183), "OMARCHY-INSPIRED THEME SUITE FOR KALI LINUX XFCE", font=font(20), fill="#7aa2f7")
    draw.text((75, 250), "22 THEMES", font=font(38, True), fill="#f7768e")
    draw.text((75, 308), "Terminal-first workflow. Unified menus. Safe restore.", font=font(25), fill="#a9b1d6")
    names = sorted(path.parent.name for path in args.themes_dir.glob("*/colors.toml"))
    for index, name in enumerate(names):
        colors = load_theme(args.themes_dir, name)
        row, column = divmod(index, 11)
        x, y = 76 + column * 100, 420 + row * 70
        draw.rounded_rectangle((x, y, x + 76, y + 44), radius=11, fill=colors["background"], outline=colors["accent"], width=3)
        draw.ellipse((x + 29, y + 13, x + 47, y + 31), fill=colors["accent"])
    draw.text((75, 585), "GTK • ROFI • QTERMINAL • NEOVIM • TMUX • VSCODE", font=font(16, True), fill="#565f89")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output, "PNG", optimize=True)


if __name__ == "__main__":
    main()
