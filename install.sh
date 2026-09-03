#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/kali-omarchy"
BIN_DIR="$HOME/.local/bin"
INSTALL_PACKAGES=1
PACKAGE_MODE=full
APPLY_THEME=1
FORCE_OS=0

blue='\033[38;2;122;162;247m'; green='\033[38;2;158;206;106m'
yellow='\033[38;2;224;175;104m'; red='\033[38;2;247;118;142m'; reset='\033[0m'
info() { printf '%b\n' "${blue}::${reset} $*"; }
ok() { printf '%b\n' "${green}::${reset} $*"; }
warn() { printf '%b\n' "${yellow}:: warning:${reset} $*" >&2; }
die() { printf '%b\n' "${red}:: error:${reset} $*" >&2; exit 1; }

usage() {
  cat <<'EOF'
Kali Omarchy installer

Usage: ./install.sh [options]

  --minimal      Install only the core desktop packages
  --no-packages  Do not install APT packages
  --no-apply     Copy files without changing the current desktop
  --force        Allow another Debian-based Xfce distribution
  -h, --help     Show this help

Run this script as your normal desktop user, not with sudo.
EOF
}

while (($#)); do
  case "$1" in
    --minimal) PACKAGE_MODE=minimal ;;
    --no-packages) INSTALL_PACKAGES=0 ;;
    --no-apply) APPLY_THEME=0 ;;
    --force) FORCE_OS=1 ;;
    -h|--help) usage; exit 0 ;;
    *) die "Unknown option: $1" ;;
  esac
  shift
done

if ((EUID == 0)) && [[ "${KALI_OMARCHY_TEST_MODE:-0}" != 1 ]]; then
  die "Do not run this installer as root. Type 'exit', then run it as your Kali desktop user."
fi

if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  . /etc/os-release
  distro="${ID:-unknown} ${ID_LIKE:-}"
  if [[ "$distro" != *kali* && "$FORCE_OS" -ne 1 ]]; then
    die "This installer targets Kali Linux. Use --force only on another Debian-based Xfce system."
  fi
fi

install_packages() {
  command -v apt-get >/dev/null 2>&1 || { warn "APT was not found; skipping packages."; return; }
  local -a core=(python3 zsh rofi papirus-icon-theme fonts-jetbrains-mono zsh-autosuggestions zsh-syntax-highlighting)
  local -a extras=(btop fastfetch tmux neovim fzf ripgrep eza bat fd-find zoxide jq curl git unzip wmctrl xclip redshift flameshot tesseract-ocr zbar-tools xfce4-screenshooter xfce4-clipman pavucontrol network-manager-applet nm-connection-editor yad)
  local -a requested=("${core[@]}") available=()
  [[ "$PACKAGE_MODE" == full ]] && requested+=("${extras[@]}")
  info "Refreshing Kali package information"
  sudo apt-get update
  local package candidate
  for package in "${requested[@]}"; do
    candidate="$(apt-cache policy "$package" 2>/dev/null | sed -n 's/^[[:space:]]*Candidate:[[:space:]]*//p' | head -n1)"
    if [[ -n "$candidate" && "$candidate" != '(none)' ]]; then
      available+=("$package")
    else
      warn "Package '$package' has no installable candidate and will be skipped."
    fi
  done
  if ((${#available[@]})); then
    info "Installing ${#available[@]} available desktop and terminal components"
    sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y "${available[@]}"
  fi
}

if ((INSTALL_PACKAGES)); then install_packages
else warn "Package installation skipped; optional actions may be unavailable."
fi

info "Installing Kali Omarchy 2.0.1"
mkdir -p "$APP_DIR" "$BIN_DIR"
for directory in assets bin config docs integrations lib rofi shell theme themes; do
  [[ -d "$PROJECT_DIR/$directory" ]] || continue
  mkdir -p "$APP_DIR/$directory"
  cp -a "$PROJECT_DIR/$directory/." "$APP_DIR/$directory/"
done
install -m644 "$PROJECT_DIR/LICENSE" "$APP_DIR/LICENSE"
install -m644 "$PROJECT_DIR/README.md" "$APP_DIR/README.md"
install -m644 "$PROJECT_DIR/THIRD_PARTY_NOTICES.md" "$APP_DIR/THIRD_PARTY_NOTICES.md"
chmod 755 "$APP_DIR/bin/kali-omarchy" "$APP_DIR/bin/kali-omarchy-menu" "$APP_DIR/bin/kali-omarchy-launcher" "$APP_DIR/bin/kali-omarchy-reminder-fire" "$APP_DIR/lib/theme_engine.py"

for command in kali-omarchy kali-omarchy-menu kali-omarchy-launcher; do
  ln -sfn "$APP_DIR/bin/$command" "$BIN_DIR/$command"
done

if ((APPLY_THEME)); then "$APP_DIR/bin/kali-omarchy" apply
else ok "Files installed. Apply later with: $BIN_DIR/kali-omarchy apply"
fi

cat <<'EOF'

Kali Omarchy is installed.

Close and reopen the terminal. Log out and in once if Xfce does not refresh.
Press Super+Space for the unified menu and Super+K for the hotkey guide.

Useful commands:
  kali-omarchy theme
  kali-omarchy background
  kali-omarchy doctor
  kali-omarchy restore
EOF
