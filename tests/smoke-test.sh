#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_ROOT="$(mktemp -d /tmp/kali-omarchy-smoke.XXXXXX)"
trap 'rm -rf -- "$TEST_ROOT"' EXIT

for script in \
  "$PROJECT_DIR/install.sh" \
  "$PROJECT_DIR/bin/kali-omarchy" \
  "$PROJECT_DIR/bin/kali-omarchy-menu" \
  "$PROJECT_DIR/bin/kali-omarchy-launcher" \
  "$PROJECT_DIR/bin/kali-omarchy-reminder-fire" \
  "$PROJECT_DIR/shell/kali-omarchy.bash"; do
  bash -n "$script"
done
if command -v zsh >/dev/null 2>&1; then zsh -n "$PROJECT_DIR/shell/kali-omarchy.zsh"; fi

mapfile -t themes < <(python3 "$PROJECT_DIR/lib/theme_engine.py" --themes-dir "$PROJECT_DIR/themes" validate)
[[ "${#themes[@]}" -eq 22 ]]

for theme in "${themes[@]}"; do
  output="$TEST_ROOT/generated-$theme"
  python3 "$PROJECT_DIR/lib/theme_engine.py" --themes-dir "$PROJECT_DIR/themes" generate --theme "$theme" --output "$output"
  for file in manifest.json gtk-3.0/gtk.css gtk-4.0/gtk.css qterminal.colorscheme rofi.rasi btop.theme kali-omarchy.vim tmux.conf kitty.conf foot.ini alacritty.toml ghostty.conf shell.env vscode-color-theme.json; do
    test -s "$output/$file"
  done
done

[[ "$(find "$PROJECT_DIR/assets/wallpapers" -mindepth 2 -maxdepth 2 -type f -name '*.svg' | wc -l)" -eq 44 ]]
python3 - "$PROJECT_DIR/integrations/vscode/package.json" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
assert len(data["contributes"]["themes"]) == 22
PY

HOME="$TEST_ROOT/home" KALI_OMARCHY_TEST_MODE=1 "$PROJECT_DIR/install.sh" --force --no-packages --no-apply >/dev/null
CLI="$TEST_ROOT/home/.local/bin/kali-omarchy"
HOME="$TEST_ROOT/home" KALI_OMARCHY_TEST_MODE=1 "$CLI" apply nord >/dev/null
[[ "$(<"$TEST_ROOT/home/.config/kali-omarchy/current-theme")" == nord ]]
grep -Fq 'source-file' "$TEST_ROOT/home/.tmux.conf"
test -s "$TEST_ROOT/home/.config/kali-omarchy/generated/manifest.json"

HOME="$TEST_ROOT/home" KALI_OMARCHY_TEST_MODE=1 "$CLI" apply white >/dev/null
[[ "$(<"$TEST_ROOT/home/.config/kali-omarchy/current-theme")" == white ]]
HOME="$TEST_ROOT/home" KALI_OMARCHY_TEST_MODE=1 "$CLI" restore >/dev/null
test ! -e "$TEST_ROOT/home/.config/kali-omarchy"
test ! -e "$TEST_ROOT/home/.tmux.conf"
test ! -e "$TEST_ROOT/home/.zshrc"
test ! -e "$TEST_ROOT/home/.bashrc"

printf 'Smoke tests passed: 22 themes generated; isolated install, switch, and restore succeeded.\n'
