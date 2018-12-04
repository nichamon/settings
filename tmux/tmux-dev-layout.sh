#!/bin/bash

P=$(tmux list-panes | wc -l)

if [[ $P != 1 ]]; then
	echo "This script must be used on a tmux window with one pane"
	exit -1
fi

tmux split-window -t 0 -h -l 80
tmux split-window -t 0 -h -l 80
tmux split-window -t 2 -v
tmux split-window -t 1 -v
tmux select-pane -t 0
