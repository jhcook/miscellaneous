#!/usr/bin/env bash
#
# This small piece of code creates a string of random alphanumeric characters
# with a frequency of random delimiters separating the string into evenly
# divided fields.
#
# Clearly, this is ideal for creating passwords and tokens. Some applications
# and APIs have limitations such as characters and length. Use the command-line
# options to sort as appropriate.
#
# Usage: `basename $0` <delimiter> <length>
#
# Author: Justin Cook <jhcook@secnix.com>

set -o nounset
set -o errexit

# Set the frequency of chars/-
_fr=`seq 3 6 | sort -R | head -n1`

# Select the random delimiter
if [ $# -gt 0 ]
then
  _dl=$1
else
  _dm='!@#$%^&*-_+='
  _dl="${_dm:$(( RANDOM % ${#_dm} )):1}"
fi

# Get a string of random alphanum chars
if [ $# -gt 1 ]
then
  _ct=$2
else
  _ct=32
fi
_rc="`LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c $_ct`"

# If delimiter is '' then print _rc and exit
if [ "$_dl" = '' ]
then
  echo $_rc
  exit
fi

# Loop and create a delimiter divided string
_pd=""
p='printf %s'
for i in `seq 0 $_fr $(($_ct-$_fr))`
do
  _pd=$_pd`[ -n "$_pd" ] && $p "$_dl" || $p ""``eval $p "\${_rc:$i:$_fr}"`
done

echo $_pd