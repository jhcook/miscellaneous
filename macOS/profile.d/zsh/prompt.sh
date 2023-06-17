BLACK="%F{black}"
DK_RED="%F{red}"
DK_GRN="%F{green}"
DK_YEL="%F{yellow}"
DK_BLU="%F{blue}"
DK_PUR="%F{magenta}"
DK_CYN="%F{cyan}"
LT_GRAY="%F{white}"
DK_GRAY="%F{8}"
LT_RED="%F{9}"
LT_GRN="%F{10}"
LT_YEL="%F{11}"
LT_BLU="%F{12}"
LT_PUR="%F{13}"
LT_CYN="%F{14}"
WHITE="%F{15}"
RESET="%f"

# get the tty
CP_TTY=$(tty)
CP_TTY=${CP_TTY:5}

# see if we are root
if [[ $(id -u) -eq 0 ]]; then
    CP_TEXT=$DK_RED
else
    CP_TEXT=$DK_PUR
fi

#$DK_GRAY($CP_TEXT@%m$DK_GRAY) \
typeset -x PS1="$DK_GRAY>$LT_GRAY>$WHITE> \
$DK_GRAY($CP_TEXT%n$WHITE@$CP_TEXT%m$DK_GRAY) \
$DK_GRAY($CP_TEXT%j$WHITE/$CP_TEXT$CP_TTY$DK_GRAY) \
$DK_GRAY($CP_TEXT%~$DK_GRAY)
$WHITE\$ $RESET"


unset CP_TTY
unset CP_TEXT

