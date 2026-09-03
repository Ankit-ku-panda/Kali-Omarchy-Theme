# Command reference

## Themes and appearance

```bash
kali-omarchy theme                    # graphical picker, or list outside a GUI
kali-omarchy theme list
kali-omarchy theme set kanagawa
kali-omarchy theme next
kali-omarchy theme previous
kali-omarchy theme install <git-url>  # colors and images only
kali-omarchy theme remove <name>      # custom themes only

kali-omarchy background
kali-omarchy background list
kali-omarchy background set /path/to/image.png
kali-omarchy background next
kali-omarchy background add /path/to/image.png

kali-omarchy font list
kali-omarchy font set "JetBrains Mono"
```

## Menus, apps, windows, and workspaces

```bash
kali-omarchy menu
kali-omarchy menu style
kali-omarchy menu system
kali-omarchy launcher
kali-omarchy launch terminal|tmux|browser|files|editor|activity|settings
kali-omarchy window close|fullscreen
kali-omarchy workspace switch 2
kali-omarchy workspace move 3
kali-omarchy workspace next|previous
```

## Desktop utilities

```bash
kali-omarchy toggle dnd|nightlight|idle|panel|compositor
kali-omarchy capture screenshot [region|window|full]
kali-omarchy capture ocr|qr|record
kali-omarchy reminder add 10m "Check the scan"
kali-omarchy reminder list|clear|prompt
kali-omarchy notice datetime|battery|weather|about
kali-omarchy hotkeys [--window]
```

## Maintenance

```bash
kali-omarchy apply [theme]
kali-omarchy status
kali-omarchy doctor
kali-omarchy restore
kali-omarchy uninstall
```

`restore` returns every tracked file and Xfce setting to its pre-theme state.
Run it from a graphical Xfce terminal so Xfconf is available.
