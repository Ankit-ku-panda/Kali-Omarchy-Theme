# Shared interactive shell helpers for Kali Omarchy.

export PATH="$HOME/.local/bin:$PATH"
export EDITOR="${EDITOR:-nano}"
export PAGER="${PAGER:-less}"

alias grep='grep --color=auto'
alias omarchy='kali-omarchy menu'
alias ko='kali-omarchy'

if command -v eza >/dev/null 2>&1; then
  alias ls='eza --icons=auto --group-directories-first'
  alias ll='eza -lah --icons=auto --group-directories-first --git'
  alias la='eza -a --icons=auto --group-directories-first'
else
  alias ll='ls -lah --color=auto'
  alias la='ls -A --color=auto'
fi

command -v batcat >/dev/null 2>&1 && alias bat='batcat'
command -v fdfind >/dev/null 2>&1 && alias fd='fdfind'
command -v fastfetch >/dev/null 2>&1 && alias ff='fastfetch'

mkcd() { mkdir -p -- "$1" && cd -- "$1"; }
extract() {
  [[ -f "$1" ]] || { printf 'Not a file: %s\n' "$1" >&2; return 1; }
  case "$1" in
    *.tar.bz2|*.tbz2) tar xjf "$1" ;; *.tar.gz|*.tgz) tar xzf "$1" ;;
    *.tar.xz|*.txz) tar xJf "$1" ;; *.tar.zst) tar --zstd -xf "$1" ;;
    *.zip) unzip "$1" ;; *.7z) 7z x "$1" ;; *.rar) unrar x "$1" ;;
    *.gz) gunzip "$1" ;; *.bz2) bunzip2 "$1" ;; *.xz) unxz "$1" ;;
    *) printf 'Unknown archive type: %s\n' "$1" >&2; return 2 ;;
  esac
}
kohere() { kali-omarchy launch terminal; }
