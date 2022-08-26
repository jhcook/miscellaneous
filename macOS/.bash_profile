for _file_ in ${HOME}/profile.d/*.sh
do
  source "${_file_}"
done

test -e "${HOME}/bin/ssh-agent-start.sh" && eval `${HOME}/bin/ssh-agent-start.sh`

test -e "${HOME}/.iterm2_shell_integration.bash" && source "${HOME}/.iterm2_shell_integration.bash"

MKUBE=`which minikube`
if [ -z "${MKUBE}" ]
then
  MKUBEIP=`minikube ip`
  NO_PROXY="${NO_PROXY},${MKUBEIP}/32"
  no_proxy="${no_proxy},${MKUBEIP}/32"
  export NO_PROXY
  export no_proxy
fi

