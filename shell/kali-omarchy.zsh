# Kali Omarchy prompt for Zsh. Loaded from ~/.zshrc by the installer.
[[ -o interactive ]] || return

_ko_app="${KALI_OMARCHY_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/kali-omarchy}"
[[ -r "$_ko_app/shell/kali-omarchy-common.sh" ]] && source "$_ko_app/shell/kali-omarchy-common.sh"
[[ -r "${XDG_CONFIG_HOME:-$HOME/.config}/kali-omarchy/generated/shell.env" ]] && source "${XDG_CONFIG_HOME:-$HOME/.config}/kali-omarchy/generated/shell.env"

autoload -Uz colors vcs_info add-zsh-hook
colors

zstyle ':vcs_info:git:*' formats '%F{141}  git:%b%f'
zstyle ':vcs_info:git:*' actionformats '%F{141}  git:%b|%a%f'
zstyle ':vcs_info:*' enable git

_kali_omarchy_precmd() { vcs_info }
add-zsh-hook precmd _kali_omarchy_precmd

if [[ "$EUID" -eq 0 ]]; then
  _ko_user_color="${KO_RED:-#f7768e}"
  _ko_prompt_symbol='#'
else
  _ko_user_color="${KO_ACCENT:-#7aa2f7}"
  _ko_prompt_symbol='❯'
fi

_ko_accent_color="${KO_ACCENT:-#7aa2f7}"
_ko_muted_color="${KO_MUTED:-#565f89}"
_ko_foreground_color="${KO_FOREGROUND:-#c0caf5}"
_ko_red_color="${KO_RED:-#f7768e}"

setopt prompt_subst
PROMPT='%F{${_ko_muted_color}}╭─%f%F{${_ko_user_color}}%n%f%F{${_ko_muted_color}}@%f%F{${_ko_accent_color}}%m%f  %F{${_ko_foreground_color}}%~%f${vcs_info_msg_0_}
%F{${_ko_muted_color}}╰─%f%F{${_ko_accent_color}}'"$_ko_prompt_symbol"'%f '
RPROMPT='%(?..%F{${_ko_red_color}}exit %?%f)'

HISTFILE="${ZDOTDIR:-$HOME}/.zsh_history"
HISTSIZE=10000
SAVEHIST=10000
setopt HIST_IGNORE_DUPS SHARE_HISTORY AUTO_CD INTERACTIVE_COMMENTS

for plugin in \
  /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh \
  /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh; do
  [[ -r "$plugin" ]] && source "$plugin" && break
done

for plugin in \
  /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh \
  /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh; do
  [[ -r "$plugin" ]] && source "$plugin" && break
done
