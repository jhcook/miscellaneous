alias brewski='brew update && brew upgrade ; brew cleanup; brew doctor'
alias smashmp='for node in $(multipass list --format json | jq -r ".list[].name") ; do multipass delete $node --purge ; done'
alias janitor='export PATH="/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin" ; . ~/.bash_profile'
