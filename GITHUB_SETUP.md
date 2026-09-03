# GitHub publishing guide

## Repository metadata

**Recommended repository name**

```text
Kali-Omarchy-Xfce
```

**Description**

```text
Bring Omarchy's 22 themes and terminal-first workflow to Kali Linux Xfce with Rofi menus, hotkeys, wallpapers, terminal/editor themes, utilities, and safe restore.
```

**Topics**

```text
kali-linux omarchy xfce linux-theme linux-rice desktop-customization rofi dotfiles terminal-theme qterminal neovim tmux bash zsh cybersecurity
```

Leave the website field empty initially. Select **Public**, and do not ask GitHub
to add a README, `.gitignore`, or license because those files already exist.

## First push

Run these commands from the extracted source directory:

```bash
cd ~/Downloads/Kali-Omarchy-Theme

git init
git branch -M main
git config user.name "Ankit Kumar Panda"
git config user.email "YOUR_GITHUB_EMAIL"

git add .
git commit -m "Initial release: Kali Omarchy 2.0.1"
git remote add origin https://github.com/Ankit-ku-panda/Kali-Omarchy-Xfce.git
git push -u origin main
```

Replace `YOUR_GITHUB_EMAIL` with your GitHub email or GitHub no-reply email.

## Release

Open **Releases → Draft a new release** and use:

- Tag: `v2.0.1`
- Target: `main`
- Title: `Kali Omarchy 2.0.1`
- Mark as latest release: enabled

Upload `Kali-Omarchy-Theme.zip` as the release asset. Do not commit the ZIP into
the source repository; `.gitignore` intentionally excludes it.

### Release notes

````markdown
## Kali Omarchy 2.0.1

Bring the current Omarchy visual style and terminal-first workflow to Kali Linux
Xfce without replacing Kali or installing Hyprland.

### Highlights

- 22 current Omarchy color palettes
- 44 original matching SVG wallpapers
- GTK, Xfce, Rofi, QTerminal and Xfce Terminal styling
- btop, Neovim/Vim, tmux and VS Code themes
- Kitty, Foot, Alacritty and Ghostty palette exports
- Unified menu and Omarchy-inspired Xfce hotkeys
- Reminders, screenshots, OCR, QR recognition and desktop toggles
- Automatic backup and complete restore command
- Safe color-only remote theme installation

### Install

```bash
unzip Kali-Omarchy-Theme.zip
cd Kali-Omarchy-Theme
chmod +x install.sh
./install.sh
```

Run the installer as your normal Kali desktop user, not with `sudo`.
````

## Recommended repository settings

- Enable Issues and Discussions.
- Enable private vulnerability reporting under **Settings → Security**.
- Require pull requests and the `Smoke test` check before merging into `main`
  after the repository begins receiving contributions.
- Upload `docs/social-preview.png` as the social preview image.
