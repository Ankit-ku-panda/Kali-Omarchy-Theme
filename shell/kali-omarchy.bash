# Kali Omarchy prompt for Bash. Loaded from ~/.bashrc by the installer.
[[ $- == *i* ]] || return

_ko_app="${KALI_OMARCHY_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/kali-omarchy}"
[[ -r "$_ko_app/shell/kali-omarchy-common.sh" ]] && source "$_ko_app/shell/kali-omarchy-common.sh"
[[ -r "${XDG_CONFIG_HOME:-$HOME/.config}/kali-omarchy/generated/shell.env" ]] && source "${XDG_CONFIG_HOME:-$HOME/.config}/kali-omarchy/generated/shell.env"

_ko_git_branch() {
  local branch
  branch="$(command git symbolic-ref --quiet --short HEAD 2>/dev/null)" || return
  printf '  git:%s' "$branch"
}

_ko_rgb() {
  local color="${1#\#}"
  printf '%d;%d;%d' "$((16#${color:0:2}))" "$((16#${color:2:2}))" "$((16#${color:4:2}))"
}
_ko_accent_rgb="$(_ko_rgb "${KO_ACCENT:-#7aa2f7}")"
_ko_muted_rgb="$(_ko_rgb "${KO_MUTED:-#565f89}")"
_ko_foreground_rgb="$(_ko_rgb "${KO_FOREGROUND:-#c0caf5}")"
_ko_red_rgb="$(_ko_rgb "${KO_RED:-#f7768e}")"

if [[ "$EUID" -eq 0 ]]; then
  _ko_user='\[\e[38;2;'"$_ko_red_rgb"'m\]\u'
  _ko_symbol='#'
else
  _ko_user='\[\e[38;2;'"$_ko_accent_rgb"'m\]\u'
  _ko_symbol='❯'
fi

PS1='\[\e[38;2;'"$_ko_muted_rgb"'m\]╭─\[\e[0m\]'"$_ko_user"'\[\e[38;2;'"$_ko_muted_rgb"'m\]@\[\e[38;2;'"$_ko_accent_rgb"'m\]\h\[\e[0m\]  \[\e[38;2;'"$_ko_foreground_rgb"'m\]\w\[\e[0m\]$(_ko_git_branch)\n\[\e[38;2;'"$_ko_muted_rgb"'m\]╰─\[\e[38;2;'"$_ko_accent_rgb"'m\]'"$_ko_symbol"'\[\e[0m\] '
