BLACK="\[\033[0;30m\]"
DK_RED="\[\033[0;31m\]"
DK_GRN="\[\033[0;32m\]"
DK_YEL="\[\033[0;33m\]"
DK_BLU="\[\033[0;34m\]"
DK_PUR="\[\033[0;35m\]"
DK_CYN="\[\033[0;36m\]"
LT_GRAY="\[\033[0;37m\]"
DK_GRAY="\[\033[1;30m\]"
LT_RED="\[\033[1;31m\]"
LT_GRN="\[\033[1;32m\]"
LT_YEL="\[\033[1;33m\]"
LT_BLU="\[\033[1;34m\]"
LT_PUR="\[\033[1;35m\]"
LT_CYN="\[\033[1;36m\]"
WHITE="\[\033[1;37m\]"
RESET="\[\033[0m\]"

# get the tty
CP_TTY=$(tty)
CP_TTY=${CP_TTY:5}

# see if we are root
if [ `/usr/bin/id -u` -eq 0 ]; then
        CP_TEXT=$DK_RED
else
        CP_TEXT=$DK_PUR
fi


export PS1="$DK_GRAY>$LT_GRAY>$WHITE> \
$DK_GRAY($CP_TEXT\\@$DK_GRAY) \
$DK_GRAY($CP_TEXT\\u$WHITE@$CP_TEXT\\h$DK_GRAY) \
$DK_GRAY($CP_TEXT\\j$WHITE/$CP_TEXT$CP_TTY$DK_GRAY) \
$DK_GRAY($CP_TEXT\\w$DK_GRAY)\\n$DK_GRAY\\$ $RESET"

unset CP_TTY
unset CP_TEXT
