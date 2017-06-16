myprompt() {
	if test -z "$parent"; then
		parent=`ps -o cmd --no-headers $PPID | awk '{ print $1 }'`
	fi
	if test -z "$left"; then
		if (( $UID )); then
			# This is regular user
			left='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[01;33m\]@\h\[\033[01;34m\] \w'
		else
			# This is root
			left='${debian_chroot:+($debian_chroot)}\[\033[01;31m\]\u\[\033[01;33m\]@\h\[\033[01;34m\] \w'
		fi
	fi

	_branch="$(git symbolic-ref HEAD --short 2>/dev/null || echo '--')"
	_git_sym_ref="\\033[0;32m(git-branch: $_branch)"

	right="\\[\\033[01;31m\\][$parent]"
	echo -ne "\033]0;${USER}@${HOSTNAME}:$PWD\007"
	PS1=$(printf "\n%*s\r%s\n%*s\n\\[\\033[01;34m\\]\$\\[\\033[00m\\] " "$((COLUMNS + 15))" "$right" "$left" "$((COLUMNS + 10))" "$_git_sym_ref")
}

export -f myprompt
export PROMPT_COMMAND=myprompt
