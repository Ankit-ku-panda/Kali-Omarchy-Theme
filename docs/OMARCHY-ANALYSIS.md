# Omarchy-to-Kali analysis

This project was checked against the current Omarchy manual and the `quattro`
repository at commit `f99d33a8ddee7b36509a71a6d20d5d23355ce8b1` (2026-09-02). The goal is
functional and visual parity where Xfce offers an equivalent, without turning Kali
into Arch Linux or installing Hyprland over the user's desktop.

Official references:

- <https://omarchy.org/manual/>
- <https://omarchy.org/manual/themes/>
- <https://omarchy.org/manual/hotkeys/>
- <https://omarchy.org/manual/making-your-own-theme/>
- <https://omarchy.org/manual/omarchy-cli/>
- <https://github.com/basecamp/omarchy>

## The 22 current palettes

The color values come from the current official `colors.toml` files. The visual
character and suggested use are this project's concise interpretation of the
palettes and previews, not official marketing descriptions.

| Theme | Mode | Background / accent | Visual character | Works especially well for |
|---|---|---|---|---|
| Catppuccin | Dark | `#1e1e2e` / `#89b4fa` | Soft blue and pastel accents | Long coding sessions |
| Catppuccin Latte | Light | `#eff1f5` / `#1e66f5` | Calm pastel daylight palette | Bright rooms and laptops |
| Ethereal | Dark | `#060B1E` / `#7d82d9` | Deep navy with indigo glow | Focused night work |
| Everforest | Dark | `#2d353b` / `#7fbbb3` | Muted forest greens | Low-contrast comfort |
| Flexoki Light | Light | `#FFFCF0` / `#205EA6` | Warm paper with ink blue | Reading and writing |
| Gruvbox | Dark | `#282828` / `#7daea3` | Warm retro earth tones | Terminal-heavy workflows |
| Hackerman | Dark | `#0B0C16` / `#82FB9C` | Neon green cyber aesthetic | Pentest demos and labs |
| Kanagawa | Dark | `#1f1f28` / `#dcd7ba` | Ink, parchment, muted blue | Distraction-free editing |
| Last Horizon | Dark | `#0c0b0c` / `#b59790` | Near-black with dusty rose | OLED and late-night use |
| Lumon | Dark | `#16242d` / `#8bc9eb` | Steel blue, crisp and cool | Dashboards and monitoring |
| Lupine | Light | `#fafafa` / `#3264eb` | Clean white with electric blue | High-clarity daytime use |
| Matte Black | Dark | `#121212` / `#e68e0d` | Black with amber and red | High-contrast operations |
| Miasma | Dark | `#222222` / `#78824b` | Earthy olive and brown | A subdued vintage look |
| Nord | Dark | `#2e3440` / `#81a1c1` | Arctic gray-blue | Balanced daily use |
| Osaka Jade | Dark | `#111c18` / `#509475` | Deep green with jade accents | Security-tool workspaces |
| Retro 82 | Dark | `#05182e` / `#faa968` | Navy, orange, and teal synth | A colorful retro desktop |
| Ristretto | Dark | `#2c2525` / `#f38d70` | Coffee brown with coral | Warm low-light work |
| Rose Pine | Light | `#faf4ed` / `#56949f` | Blush paper and soft teal | Design and documentation |
| Solitude | Dark | `#101315` / `#798186` | Neutral graphite monochrome | Minimal visual noise |
| Tokyo Night | Dark | `#1a1b26` / `#7aa2f7` | Indigo, blue, and violet | General-purpose default |
| Vantablack | Dark | `#000000` / `#8d8d8d` | Pure black monochrome | OLED screens |
| White | Light | `#ffffff` / `#6e6e6e` | Pure white monochrome | Maximum daylight simplicity |

Each palette generates GTK 3/4, Rofi, QTerminal, Xfce Terminal, btop,
Vim/Neovim, tmux, VS Code, Kitty, Foot, Alacritty, Ghostty, shell variables,
and two original 1920×1080 SVG backgrounds.

## Manual feature coverage

| Omarchy manual area | Kali/Xfce implementation | Coverage |
|---|---|---|
| Themes and theme cycling | 22 palettes, picker, next/previous, live generated configs | Native adaptation |
| Theme backgrounds | Two bundled backgrounds per theme; picker, cycle, and add | Native adaptation |
| Remote theme install | Imports only `colors.toml` and image files from a Git repository | Safer adaptation |
| Top-bar menu | Rofi command center with apps, style, system, capture, toggles, reminders | Xfce equivalent |
| App launcher | Rofi `drun` with icons and fuzzy filtering | Native adaptation |
| Terminal | QTerminal and Xfce Terminal configured; exports for four other terminals | Native adaptation |
| Shell and functions | Themed Bash/Zsh prompt, Git branch, aliases, archive and directory helpers | Native adaptation |
| Tmux | `Ctrl+Space` prefix, splits, pane movement, zoom, mouse, themed status | Native adaptation |
| Neovim | Generated Vim-compatible colorscheme, loaded without replacing user config | Native adaptation |
| Coding tools | One local VS Code/VSCodium extension containing all 22 themes | Native adaptation |
| btop / activity | Generated btop theme and activity launcher | Native adaptation |
| Hotkeys | Xfce shortcuts for menu, apps, theme, background, terminal, lock, capture, toggles, workspaces | Xfce mapping |
| Clipboard | `Super+Ctrl+V` opens Xfce Clipman when installed | Xfce equivalent |
| Reminders | User `systemd-run` timers with desktop notification and list/clear commands | Native adaptation |
| Notices | Date/time, battery, weather, and system/about notices | Native adaptation |
| Screenshots | Region, window, or full-screen capture | Native adaptation |
| OCR and QR | Region capture, local recognition, copy result to clipboard | Native adaptation |
| Screen recording | Opens OBS or SimpleScreenRecorder if installed | App handoff |
| Toggles | Do-not-disturb, night light, stay-awake, panel, compositor | Xfce mapping |
| Fonts | Monospace font listing and live selection | Native adaptation |
| Hooks | Executable user hooks beneath `~/.config/kali-omarchy/hooks/<event>.d/` | Native adaptation |
| Restore | First-apply file and Xfconf snapshot, reversible with one command | Kali-specific safety |

## Intentional boundaries

Xfce does not have Hyprland's tiling tree, window grouping, scratchpad, or
Quickshell widgets. The package therefore does not pretend those operations are
identical. Standard Xfce workspaces, fullscreen, close-window, and panel controls
are mapped instead.

The package deliberately does not touch disk encryption, partitions, GRUB,
Plymouth, login managers, kernel parameters, system snapshots, firewall policy,
Docker groups, or Kali's update mechanism. Those are operating-system decisions,
not theme settings. It also does not bulk-install Omarchy's preferred GUI apps;
Kali's existing tools remain intact.

## Theme format and trust model

A compatible theme needs a root `colors.toml` with the current Omarchy color
keys. A `backgrounds/` directory is optional. `kali-omarchy theme install URL`
clones the repository into a temporary directory, validates the palette, and
copies only that TOML file plus PNG, JPEG, WebP, or SVG images. Executable hooks,
scripts, and application configs from remote repositories are never imported.
