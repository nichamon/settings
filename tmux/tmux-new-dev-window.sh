#!/bin/bash

tmux new-window

tmux split-window -t 0 -h -l 80
tmux split-window -t 0 -h -l 80
tmux split-window -t 2 -v
tmux split-window -t 1 -v
tmux select-pane -t 0
