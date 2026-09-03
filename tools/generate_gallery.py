#!/usr/bin/env python3
"""Generate the bundled palette gallery SVG."""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from theme_engine import display_name, load_theme, palette  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--themes-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    names = sorted(path.parent.name for path in args.themes_dir.glob("*/colors.toml"))
    columns, card_w, card_h, gap, margin = 4, 400, 168, 22, 34
    rows = (len(names) + columns - 1) // columns
    width = margin * 2 + columns * card_w + (columns - 1) * gap
    height = 112 + rows * card_h + (rows - 1) * gap + margin
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#0b0f14"/>',
        '<text x="34" y="48" fill="#f0f4f8" font-family="JetBrains Mono,monospace" font-size="25" font-weight="700">KALI OMARCHY — 22 THEMES</text>',
        '<text x="34" y="77" fill="#8a96a3" font-family="JetBrains Mono,monospace" font-size="13">Current Omarchy palettes adapted for Kali Linux Xfce</text>',
    ]
    for index, name in enumerate(names):
        c = load_theme(args.themes_dir, name)
        x = margin + (index % columns) * (card_w + gap)
        y = 112 + (index // columns) * (card_h + gap)
        title = html.escape(display_name(name))
        parts.extend(
            [
                f'<g transform="translate({x} {y})">',
                f'<rect width="{card_w}" height="{card_h}" rx="13" fill="{c["background"]}" stroke="{c["accent"]}" stroke-opacity=".72"/>',
                f'<text x="20" y="35" fill="{c["foreground"]}" font-family="JetBrains Mono,monospace" font-size="17" font-weight="700">{title}</text>',
                f'<text x="20" y="59" fill="{c["dark_foreground"]}" font-family="JetBrains Mono,monospace" font-size="11">{c["mode"].upper()}  {c["background"]}  +  {c["accent"]}</text>',
            ]
        )
        for swatch, color in enumerate(palette(c)[1:7]):
            parts.append(f'<rect x="{20 + swatch * 58}" y="89" width="46" height="46" rx="8" fill="{color}"/>')
        parts.extend([f'<rect x="20" y="146" width="360" height="3" rx="2" fill="{c["accent"]}"/>', '</g>'])
    parts.append("</svg>")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
