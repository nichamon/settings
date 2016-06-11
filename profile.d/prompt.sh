parent=`ps -o cmd --no-headers $PPID | awk '{ print $1 }'`
if (( $UID )); then
	# This is regular user
	left='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[01;33m\]@\h\[\033[01;34m\] \w'
else
	# This is root
	left='${debian_chroot:+($debian_chroot)}\[\033[01;31m\]\u\[\033[01;33m\]@\h\[\033[01;34m\] \w'
fi
#right="\\[\\033[01;31m\\][$parent]"
right="\\[\\033[01;31m\\][$parent]"

myprompt() {
	echo -ne "\033]0;${USER}@${HOSTNAME}:$PWD\007"
	PS1=$(printf "\n%*s\r%s\n\\[\\033[01;34m\\]\$\\[\\033[00m\\] " "$((COLUMNS + 15))" "$right" "$left")
}

export -f myprompt
export PROMPT_COMMAND=myprompt
export PYTHONSTARTUP=$HOME/.pyrc
export DISPLAY=:0
alias vim='vim -X'

# use vi mode
set -o vi
