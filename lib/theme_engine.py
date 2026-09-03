#!/usr/bin/env python3
"""Generate Kali/Xfce application configs from Omarchy colors.toml palettes."""

from __future__ import annotations

import argparse
import colorsys
import json
import re
import shutil
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - fallback for older Python
    tomllib = None


REQUIRED = (
    "mode",
    "accent",
    "selection",
    "muted",
    "background",
    "dark_background",
    "darker_background",
    "lighter_background",
    "foreground",
    "dark_foreground",
    "light_foreground",
    "bright_foreground",
    "red",
    "yellow",
    "green",
    "cyan",
    "blue",
    "magenta",
    "bright_red",
    "bright_yellow",
    "bright_green",
    "bright_cyan",
    "bright_blue",
    "bright_magenta",
)


def parse_simple_toml(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def load_theme(themes_dir: Path, name: str) -> dict[str, str]:
    if not re.fullmatch(r"[a-z0-9][a-z0-9._+-]*", name):
        raise ValueError(f"unsafe theme name: {name!r}")
    path = themes_dir / name / "colors.toml"
    if not path.is_file():
        raise FileNotFoundError(f"theme not found: {name}")
    if tomllib:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    else:
        data = parse_simple_toml(path)
    missing = [key for key in REQUIRED if key not in data]
    if missing:
        raise ValueError(f"{name}: missing {', '.join(missing)}")
    if data["mode"] not in {"dark", "light"}:
        raise ValueError(f"{name}: mode must be dark or light")
    for key, value in data.items():
        if key == "mode" or key.startswith("hyprland_") or key in {"active_border_color", "active_tab_background"}:
            continue
        if isinstance(value, str) and not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            raise ValueError(f"{name}: invalid color {key}={value!r}")
    return {key: str(value) for key, value in data.items()}


def rgb(color: str) -> tuple[int, int, int]:
    value = color.lstrip("#")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def rgba(color: str, alpha: str = "ff") -> str:
    return f"{color}{alpha}"


def palette(c: dict[str, str]) -> list[str]:
    return [
        c["darker_background"],
        c["red"],
        c["green"],
        c["yellow"],
        c["blue"],
        c["magenta"],
        c["cyan"],
        c["light_foreground"],
        c["muted"],
        c["bright_red"],
        c["bright_green"],
        c["bright_yellow"],
        c["bright_blue"],
        c["bright_magenta"],
        c["bright_cyan"],
        c["bright_foreground"],
    ]


def put(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def gtk_css(c: dict[str, str]) -> str:
    builtin = "gtk-contained-dark.css" if c["mode"] == "dark" else "gtk-contained.css"
    return f'''@import url("resource:///org/gtk/libgtk/theme/Adwaita/{builtin}");

@define-color theme_bg_color {c["background"]};
@define-color theme_base_color {c["dark_background"]};
@define-color theme_fg_color {c["foreground"]};
@define-color theme_text_color {c["foreground"]};
@define-color theme_selected_bg_color {c["accent"]};
@define-color theme_selected_fg_color {c["darker_background"]};
@define-color borders {c["muted"]};
@define-color accent_color {c["accent"]};

window, .background {{ color: {c["foreground"]}; background-color: {c["background"]}; }}
headerbar, titlebar, .titlebar {{
  min-height: 38px; color: {c["foreground"]}; background: {c["dark_background"]};
  border-bottom: 1px solid {c["muted"]}; box-shadow: none;
}}
button, entry, spinbutton, combobox button {{ border-radius: 7px; }}
button {{ color: {c["foreground"]}; background: {c["dark_background"]}; border-color: {c["muted"]}; }}
button:hover {{ color: {c["bright_foreground"]}; background: {c["lighter_background"]}; border-color: {c["accent"]}; }}
button:checked, button:active, .suggested-action {{ color: {c["darker_background"]}; background: {c["accent"]}; border-color: {c["accent"]}; }}
entry, textview, treeview.view, iconview.view {{ color: {c["foreground"]}; background: {c["dark_background"]}; border-color: {c["muted"]}; }}
selection, *:selected {{ color: {c["darker_background"]}; background-color: {c["accent"]}; }}
menu, .menu, popover, .context-menu {{ color: {c["foreground"]}; background: {c["dark_background"]}; border: 1px solid {c["muted"]}; border-radius: 8px; }}
tooltip {{ color: {c["foreground"]}; background: {c["lighter_background"]}; border: 1px solid {c["muted"]}; border-radius: 6px; }}
.xfce4-panel.background {{ color: {c["foreground"]}; background-color: alpha({c["background"]}, 0.96); border-bottom: 1px solid {c["muted"]}; }}
.xfce4-panel button {{ margin: 3px 2px; padding: 2px 7px; color: {c["light_foreground"]}; background: transparent; border: 0; border-radius: 7px; box-shadow: none; }}
.xfce4-panel button:hover, .xfce4-panel button:checked {{ color: {c["bright_foreground"]}; background: {c["lighter_background"]}; }}
scrollbar slider {{ min-width: 6px; min-height: 6px; border-radius: 8px; background: {c["muted"]}; }}
'''


def qterminal(c: dict[str, str], display: str) -> str:
    lines: list[str] = []
    names = [f"Color{i}" for i in range(8)] + [f"Color{i}Intense" for i in range(8)]
    for section, color in zip(names, palette(c)):
        lines.extend([f"[{section}]", f"Color={','.join(map(str, rgb(color)))}", ""])
    lines.extend(
        [
            "[Background]",
            f"Color={','.join(map(str, rgb(c['background'])))}",
            "",
            "[BackgroundIntense]",
            f"Color={','.join(map(str, rgb(c['dark_background'])))}",
            "",
            "[Foreground]",
            f"Color={','.join(map(str, rgb(c['foreground'])))}",
            "",
            "[ForegroundIntense]",
            f"Color={','.join(map(str, rgb(c['bright_foreground'])))}",
            "",
            "[General]",
            f"Description=Kali Omarchy — {display}",
            "Opacity=1",
        ]
    )
    return "\n".join(lines)


def rofi(c: dict[str, str]) -> str:
    return f'''configuration {{
  modi: "drun,run,window"; show-icons: true; display-drun: " Apps";
  display-run: " Run"; display-window: " Windows"; drun-display-format: "{{name}}";
  font: "JetBrainsMono Nerd Font 12";
}}
* {{
  bg: {rgba(c["background"], "f2")}; bg-alt: {rgba(c["dark_background"])};
  surface: {rgba(c["lighter_background"])}; border: {rgba(c["muted"])};
  fg: {rgba(c["foreground"])}; muted-fg: {rgba(c["dark_foreground"])};
  accent: {rgba(c["accent"])}; urgent: {rgba(c["red"])}; transparent: #00000000;
}}
window {{ width: 700px; border: 2px; border-color: @border; border-radius: 14px; background-color: @bg; padding: 18px; }}
mainbox {{ spacing: 14px; background-color: @transparent; }}
inputbar {{ spacing: 10px; padding: 12px 14px; border: 1px; border-color: @border; border-radius: 10px; background-color: @bg-alt; children: [ prompt, entry ]; }}
prompt {{ text-color: @accent; background-color: @transparent; }}
entry {{ placeholder: "Search…"; placeholder-color: @muted-fg; text-color: @fg; background-color: @transparent; }}
listview {{ lines: 10; columns: 1; fixed-height: false; scrollbar: false; spacing: 4px; background-color: @transparent; }}
element {{ padding: 10px 12px; spacing: 12px; border-radius: 9px; background-color: @transparent; text-color: @fg; }}
element selected {{ background-color: @surface; text-color: @accent; }}
element-icon {{ size: 28px; background-color: @transparent; }}
element-text {{ vertical-align: 0.5; background-color: @transparent; text-color: inherit; }}
'''


def btop(c: dict[str, str]) -> str:
    return f'''# Kali Omarchy generated btop theme
theme[main_bg]="{c['background']}"
theme[main_fg]="{c['foreground']}"
theme[title]="{c['bright_foreground']}"
theme[hi_fg]="{c['accent']}"
theme[selected_bg]="{c['selection']}"
theme[selected_fg]="{c['bright_foreground']}"
theme[inactive_fg]="{c['dark_foreground']}"
theme[graph_text]="{c['light_foreground']}"
theme[meter_bg]="{c['lighter_background']}"
theme[proc_misc]="{c['magenta']}"
theme[cpu_box]="{c['accent']}"
theme[mem_box]="{c['green']}"
theme[net_box]="{c['cyan']}"
theme[proc_box]="{c['magenta']}"
theme[div_line]="{c['muted']}"
theme[temp_start]="{c['green']}"
theme[temp_mid]="{c['yellow']}"
theme[temp_end]="{c['red']}"
theme[cpu_start]="{c['cyan']}"
theme[cpu_mid]="{c['blue']}"
theme[cpu_end]="{c['magenta']}"
theme[free_start]="{c['green']}"
theme[free_mid]="{c['cyan']}"
theme[free_end]="{c['blue']}"
theme[cached_start]="{c['blue']}"
theme[cached_mid]="{c['magenta']}"
theme[cached_end]="{c['red']}"
theme[available_start]="{c['yellow']}"
theme[available_mid]="{c['green']}"
theme[available_end]="{c['cyan']}"
theme[used_start]="{c['green']}"
theme[used_mid]="{c['yellow']}"
theme[used_end]="{c['red']}"
theme[download_start]="{c['cyan']}"
theme[download_mid]="{c['blue']}"
theme[download_end]="{c['magenta']}"
theme[upload_start]="{c['green']}"
theme[upload_mid]="{c['yellow']}"
theme[upload_end]="{c['red']}"
'''


def nvim(c: dict[str, str]) -> str:
    return f'''" Kali Omarchy generated Vim/Neovim colorscheme
hi clear
if exists("syntax_on") | syntax reset | endif
let g:colors_name = "kali-omarchy"
set background={c['mode']}
hi Normal guifg={c['foreground']} guibg={c['background']}
hi NormalFloat guifg={c['foreground']} guibg={c['dark_background']}
hi CursorLine guibg={c['lighter_background']}
hi CursorLineNr guifg={c['accent']} guibg={c['lighter_background']} gui=bold
hi LineNr guifg={c['dark_foreground']} guibg={c['background']}
hi Visual guibg={c['selection']}
hi Search guifg={c['darker_background']} guibg={c['yellow']}
hi IncSearch guifg={c['darker_background']} guibg={c['accent']}
hi Comment guifg={c['dark_foreground']} gui=italic
hi Constant guifg={c['orange'] if 'orange' in c else c['yellow']}
hi String guifg={c['green']}
hi Identifier guifg={c['cyan']}
hi Function guifg={c['blue']}
hi Statement guifg={c['magenta']} gui=bold
hi PreProc guifg={c['yellow']}
hi Type guifg={c['cyan']}
hi Special guifg={c['accent']}
hi Error guifg={c['bright_foreground']} guibg={c['red']}
hi Todo guifg={c['darker_background']} guibg={c['yellow']} gui=bold
hi StatusLine guifg={c['foreground']} guibg={c['lighter_background']}
hi StatusLineNC guifg={c['dark_foreground']} guibg={c['dark_background']}
hi Pmenu guifg={c['foreground']} guibg={c['dark_background']}
hi PmenuSel guifg={c['darker_background']} guibg={c['accent']}
hi DiffAdd guifg={c['green']} guibg={c['dark_background']}
hi DiffChange guifg={c['yellow']} guibg={c['dark_background']}
hi DiffDelete guifg={c['red']} guibg={c['dark_background']}
hi DiagnosticError guifg={c['red']}
hi DiagnosticWarn guifg={c['yellow']}
hi DiagnosticInfo guifg={c['cyan']}
hi DiagnosticHint guifg={c['green']}
'''


def tmux(c: dict[str, str]) -> str:
    return f'''# Kali Omarchy generated tmux colors
set -g status-style "fg={c['foreground']},bg={c['dark_background']}"
set -g status-left-style "fg={c['darker_background']},bg={c['accent']},bold"
set -g status-right-style "fg={c['light_foreground']},bg={c['dark_background']}"
set -g window-status-style "fg={c['dark_foreground']},bg={c['dark_background']}"
set -g window-status-current-style "fg={c['bright_foreground']},bg={c['lighter_background']},bold"
set -g pane-border-style "fg={c['muted']}"
set -g pane-active-border-style "fg={c['accent']}"
set -g message-style "fg={c['bright_foreground']},bg={c['selection']}"
'''


def terminals(c: dict[str, str]) -> dict[str, str]:
    p = palette(c)
    kitty_lines = [
        f"background {c['background']}",
        f"foreground {c['foreground']}",
        f"selection_background {c['selection']}",
        f"cursor {c['accent']}",
    ] + [f"color{i} {color}" for i, color in enumerate(p)]
    foot_lines = [
        "[colors]",
        f"background={c['background'].lstrip('#')}",
        f"foreground={c['foreground'].lstrip('#')}",
        f"selection-background={c['selection'].lstrip('#')}",
    ] + [f"regular{i}={p[i].lstrip('#')}" for i in range(8)] + [f"bright{i}={p[i+8].lstrip('#')}" for i in range(8)]
    alacritty = {
        "colors": {
            "primary": {"background": c["background"], "foreground": c["foreground"]},
            "cursor": {"text": c["background"], "cursor": c["accent"]},
            "selection": {"text": c["foreground"], "background": c["selection"]},
            "normal": dict(zip(("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"), p[:8])),
            "bright": dict(zip(("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"), p[8:])),
        }
    }
    alacritty_lines = ["# Kali Omarchy generated Alacritty palette", "[colors.primary]", f'background = "{c["background"]}"', f'foreground = "{c["foreground"]}"', "", "[colors.cursor]", f'text = "{c["background"]}"', f'cursor = "{c["accent"]}"', "", "[colors.selection]", f'text = "{c["foreground"]}"', f'background = "{c["selection"]}"']
    for group, colors in (("normal", alacritty["colors"]["normal"]), ("bright", alacritty["colors"]["bright"])):
        alacritty_lines.extend(["", f"[colors.{group}]"] + [f'{key} = "{value}"' for key, value in colors.items()])
    ghostty_lines = [
        f"background = {c['background']}", f"foreground = {c['foreground']}",
        f"cursor-color = {c['accent']}", f"selection-background = {c['selection']}",
    ] + [f"palette = {i}={color}" for i, color in enumerate(p)]
    return {
        "kitty.conf": "\n".join(kitty_lines),
        "foot.ini": "\n".join(foot_lines),
        "alacritty.toml": "\n".join(alacritty_lines),
        "ghostty.conf": "\n".join(ghostty_lines),
    }


def vscode(c: dict[str, str], name: str) -> dict:
    display = display_name(name)
    return {
        "$schema": "vscode://schemas/color-theme",
        "name": f"Kali Omarchy — {display}",
        "type": c["mode"],
        "colors": {
            "focusBorder": c["accent"],
            "foreground": c["foreground"],
            "descriptionForeground": c["dark_foreground"],
            "errorForeground": c["red"],
            "editor.background": c["background"],
            "editor.foreground": c["foreground"],
            "editor.selectionBackground": c["selection"],
            "editor.lineHighlightBackground": c["lighter_background"],
            "editorCursor.foreground": c["accent"],
            "editorLineNumber.foreground": c["dark_foreground"],
            "editorLineNumber.activeForeground": c["accent"],
            "sideBar.background": c["dark_background"],
            "sideBar.foreground": c["light_foreground"],
            "activityBar.background": c["darker_background"],
            "activityBar.foreground": c["accent"],
            "titleBar.activeBackground": c["dark_background"],
            "titleBar.activeForeground": c["foreground"],
            "statusBar.background": c["dark_background"],
            "statusBar.foreground": c["foreground"],
            "statusBar.debuggingBackground": c["orange"] if "orange" in c else c["yellow"],
            "panel.background": c["dark_background"],
            "panel.border": c["muted"],
            "terminal.ansiBlack": palette(c)[0],
            "terminal.ansiRed": palette(c)[1],
            "terminal.ansiGreen": palette(c)[2],
            "terminal.ansiYellow": palette(c)[3],
            "terminal.ansiBlue": palette(c)[4],
            "terminal.ansiMagenta": palette(c)[5],
            "terminal.ansiCyan": palette(c)[6],
            "terminal.ansiWhite": palette(c)[7],
            "terminal.ansiBrightBlack": palette(c)[8],
            "terminal.ansiBrightRed": palette(c)[9],
            "terminal.ansiBrightGreen": palette(c)[10],
            "terminal.ansiBrightYellow": palette(c)[11],
            "terminal.ansiBrightBlue": palette(c)[12],
            "terminal.ansiBrightMagenta": palette(c)[13],
            "terminal.ansiBrightCyan": palette(c)[14],
            "terminal.ansiBrightWhite": palette(c)[15],
        },
        "tokenColors": [
            {"scope": ["comment", "punctuation.definition.comment"], "settings": {"foreground": c["dark_foreground"], "fontStyle": "italic"}},
            {"scope": ["string"], "settings": {"foreground": c["green"]}},
            {"scope": ["constant.numeric", "constant.language"], "settings": {"foreground": c["orange"] if "orange" in c else c["yellow"]}},
            {"scope": ["keyword", "storage"], "settings": {"foreground": c["magenta"]}},
            {"scope": ["entity.name.function", "support.function"], "settings": {"foreground": c["blue"]}},
            {"scope": ["entity.name.type", "support.type"], "settings": {"foreground": c["cyan"]}},
            {"scope": ["variable", "identifier"], "settings": {"foreground": c["foreground"]}},
            {"scope": ["invalid"], "settings": {"foreground": c["bright_foreground"], "background": c["red"]}},
        ],
    }


def display_name(name: str) -> str:
    return " ".join(part.upper() if part in {"82"} else part.capitalize() for part in name.split("-"))


def generate(themes_dir: Path, name: str, output: Path) -> None:
    c = load_theme(themes_dir, name)
    display = display_name(name)
    p = palette(c)
    put(output / "gtk-3.0" / "gtk.css", gtk_css(c))
    put(output / "gtk-4.0" / "gtk.css", gtk_css(c))
    put(output / "qterminal.colorscheme", qterminal(c, display))
    put(output / "rofi.rasi", rofi(c))
    put(output / "btop.theme", btop(c))
    put(output / "kali-omarchy.vim", nvim(c))
    put(output / "tmux.conf", tmux(c))
    for filename, content in terminals(c).items():
        put(output / filename, content)
    env_lines = [
        f"KO_THEME='{name}'",
        f"KO_THEME_DISPLAY='{display}'",
        f"KO_MODE='{c['mode']}'",
        f"KO_ACCENT='{c['accent']}'",
        f"KO_BACKGROUND='{c['background']}'",
        f"KO_FOREGROUND='{c['foreground']}'",
        f"KO_MUTED='{c['muted']}'",
        f"KO_RED='{c['red']}'",
        f"KO_GREEN='{c['green']}'",
        f"KO_BLUE='{c['blue']}'",
        f"KO_MAGENTA='{c['magenta']}'",
        f"KO_TERMINAL_PALETTE='{';'.join(p)}'",
    ]
    put(output / "shell.env", "\n".join(env_lines))
    put(
        output / "manifest.json",
        json.dumps({"theme": name, "display_name": display, "mode": c["mode"], "colors": c, "terminal_palette": p}, indent=2),
    )
    put(output / "vscode-color-theme.json", json.dumps(vscode(c, name), indent=2))


def validate_all(themes_dir: Path) -> list[str]:
    names = sorted(path.parent.name for path in themes_dir.glob("*/colors.toml"))
    if not names:
        raise ValueError(f"no themes found in {themes_dir}")
    for name in names:
        load_theme(themes_dir, name)
    return names


def build_vscode(themes_dir: Path, output: Path) -> None:
    names = validate_all(themes_dir)
    themes = []
    for name in names:
        c = load_theme(themes_dir, name)
        filename = f"{name}.json"
        put(output / "themes" / filename, json.dumps(vscode(c, name), indent=2))
        themes.append(
            {
                "label": f"Kali Omarchy — {display_name(name)}",
                "uiTheme": "vs-dark" if c["mode"] == "dark" else "vs",
                "path": f"./themes/{filename}",
            }
        )
    package = {
        "name": "kali-omarchy-themes",
        "displayName": "Kali Omarchy Themes",
        "description": "The 22 Omarchy palettes adapted for Kali Linux.",
        "version": "2.0.0",
        "publisher": "ankit-kumar-panda",
        "engines": {"vscode": "^1.75.0"},
        "categories": ["Themes"],
        "contributes": {"themes": themes},
    }
    put(output / "package.json", json.dumps(package, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--themes-dir", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("generate")
    make.add_argument("--theme", required=True)
    make.add_argument("--output", type=Path, required=True)
    sub.add_parser("validate")
    vs = sub.add_parser("build-vscode")
    vs.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "generate":
            generate(args.themes_dir, args.theme, args.output)
        elif args.command == "validate":
            print("\n".join(validate_all(args.themes_dir)))
        elif args.command == "build-vscode":
            build_vscode(args.themes_dir, args.output)
    except (OSError, ValueError) as exc:
        print(f"theme-engine: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

