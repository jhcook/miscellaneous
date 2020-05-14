for _file_ in ${HOME}/profile.d/*.sh
do
  source "${_file_}"
done

test -e "${HOME}/bin/ssh-agent-start.sh" && eval `${HOME}/bin/ssh-agent-start.sh`

test -e "${HOME}/.iterm2_shell_integration.bash" && source "${HOME}/.iterm2_shell_integration.bash"
