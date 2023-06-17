# Check to see if the watcher is running. If not, start it.
if ! pgrep -qf "${HOME}/profile.d/bin/ipwatcher.py"
then
    "${HOME}/profile.d/bin/ipwatcher.py" &
fi

# The following trap for USR1 is used to source the environment after an IP
# address change.
# https://superuser.com/questions/1042748/periodically-source-shell-profile
trap "source ~/.zshrc" USR1
