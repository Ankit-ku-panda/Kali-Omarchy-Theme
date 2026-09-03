#!/usr/bin/env python3
"""Build two original SVG wallpapers for every bundled palette."""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from theme_engine import display_name, load_theme  # noqa: E402


def waves(name: str, c: dict[str, str]) -> str:
    title = html.escape(display_name(name).upper())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{c['darker_background']}"/><stop offset="1" stop-color="{c['background']}"/></linearGradient>
 <radialGradient id="glow" cx="75%" cy="18%" r="70%"><stop stop-color="{c['accent']}" stop-opacity=".32"/><stop offset="1" stop-color="{c['background']}" stop-opacity="0"/></radialGradient>
 <pattern id="grid" width="64" height="64" patternUnits="userSpaceOnUse"><path d="M64 0H0V64" fill="none" stroke="{c['foreground']}" stroke-opacity=".035"/></pattern>
</defs>
<rect width="1920" height="1080" fill="url(#bg)"/><rect width="1920" height="1080" fill="url(#glow)"/><rect width="1920" height="1080" fill="url(#grid)"/>
<path d="M-100 820C300 650 500 1010 850 755s590-250 1170-65" fill="none" stroke="{c['accent']}" stroke-opacity=".17" stroke-width="90"/>
<path d="M-120 820C300 640 500 995 850 745s610-245 1190-60" fill="none" stroke="{c['bright_foreground']}" stroke-opacity=".55" stroke-width="2"/>
<path d="M-80 870C320 700 520 1040 870 795s600-230 1140-40" fill="none" stroke="{c['magenta']}" stroke-opacity=".24"/>
<g transform="translate(120 900)"><rect width="42" height="2" rx="1" fill="{c['accent']}"/><text y="36" fill="{c['foreground']}" font-family="JetBrains Mono,monospace" font-size="18" letter-spacing="5">KALI // OMARCHY</text><text y="66" fill="{c['dark_foreground']}" font-family="JetBrains Mono,monospace" font-size="11" letter-spacing="3">{title}</text></g>
</svg>'''


def orbit(name: str, c: dict[str, str]) -> str:
    title = html.escape(display_name(name).upper())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
<defs>
 <linearGradient id="bg" x1="0" y1="1" x2="1" y2="0"><stop stop-color="{c['dark_background']}"/><stop offset="1" stop-color="{c['background']}"/></linearGradient>
 <radialGradient id="orb"><stop stop-color="{c['accent']}" stop-opacity=".72"/><stop offset=".45" stop-color="{c['blue']}" stop-opacity=".18"/><stop offset="1" stop-color="{c['background']}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1920" height="1080" fill="url(#bg)"/><circle cx="1450" cy="320" r="430" fill="url(#orb)"/>
<g fill="none" stroke="{c['foreground']}" stroke-opacity=".10"><ellipse cx="1420" cy="340" rx="560" ry="205" transform="rotate(-18 1420 340)"/><ellipse cx="1420" cy="340" rx="420" ry="145" transform="rotate(-18 1420 340)"/><ellipse cx="1420" cy="340" rx="270" ry="90" transform="rotate(-18 1420 340)"/></g>
<circle cx="1045" cy="486" r="7" fill="{c['bright_foreground']}"/><circle cx="1630" cy="194" r="4" fill="{c['magenta']}"/>
<g transform="translate(120 900)"><rect width="42" height="2" rx="1" fill="{c['accent']}"/><text y="36" fill="{c['foreground']}" font-family="JetBrains Mono,monospace" font-size="18" letter-spacing="5">KALI // OMARCHY</text><text y="66" fill="{c['dark_foreground']}" font-family="JetBrains Mono,monospace" font-size="11" letter-spacing="3">{title} / ORBIT</text></g>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--themes-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    for path in sorted(args.themes_dir.glob("*/colors.toml")):
        name = path.parent.name
        colors = load_theme(args.themes_dir, name)
        target = args.output / name
        target.mkdir(parents=True, exist_ok=True)
        (target / "01-waves.svg").write_text(waves(name, colors), encoding="utf-8")
        (target / "02-orbit.svg").write_text(orbit(name, colors), encoding="utf-8")


if __name__ == "__main__":
    main()

