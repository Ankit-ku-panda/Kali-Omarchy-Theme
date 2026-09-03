# Changelog

All notable changes to Kali Omarchy are documented here. The project follows
[Semantic Versioning](https://semver.org/).

## [2.0.1] - 2026-09-03

### Added

- All 22 current Omarchy palettes adapted for Kali Linux Xfce.
- Two original 1920×1080 SVG wallpapers for every theme.
- GTK 3/4, Rofi, QTerminal, Xfce Terminal, btop, Vim/Neovim, tmux,
  VS Code/VSCodium, Kitty, Foot, Alacritty, and Ghostty integrations.
- Unified menu, Xfce hotkeys, workspace controls, reminders, notices, captures,
  OCR, QR recognition, desktop toggles, and shell helpers.
- Automatic first-apply backup and full restore command.
- Color-and-image-only remote theme importer.
- Isolated installation, theme generation, switching, restore, and path-safety tests.

### Fixed

- Replaced obsolete Kali package `network-manager-gnome` with
  `network-manager-applet` and `nm-connection-editor`.
- Package detection now requires an actual APT candidate and safely skips
  obsolete metadata-only packages.

[2.0.1]: https://github.com/Ankit-ku-panda/Kali-Omarchy-Xfce/releases/tag/v2.0.1
