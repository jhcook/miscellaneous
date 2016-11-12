#!/usr/bin/env bash

#
#
#
#

set -o errexit

trap on_exit EXIT
trap on_int INT
trap on_term TERM

on_exit() {
    printf "caught EXIT"
}

on_int() {
    printf "caught INT"
}

on_term() {
    printf "caught TERM"
}

echo "waiting for five"
sleep 5
echo "cya"
exit 0
