#!/bin/bash

_prepend() {
	local L=$1
	local E=$2
	[[ *:${!L}:* == *:${E}:* ]] || eval export ${L}="${E}:${!L}"
}

_append() {
	local L=$1
	local E=$2
	[[ *:${!L}:* == *:${E}:* ]] || eval export ${L}="${!L}:${E}"
}

_prepend PATH $HOME/.local/bin
