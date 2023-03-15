#!/bin/bash

# enable color support of ls and also add color aliases
ls_colors=""
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    ls_colors="--color=auto"
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi


# Standard aliases
alias ls='ls ${ls_colors} -ahF'
alias la='ls ${ls_colors} -AahF'
alias ll='ls ${ls_colors} -lahF'
alias l='ll'
alias 'cd..'='cd ..'
alias '..'='cd ..'
alias emacs='TERM=xterm-direct emacs -nw'
alias emasc='TERM=xterm-direct emacs -nw'
alias eamcs='TERM=xterm-direct emacs -nw'
alias emcas='TERM=xterm-direct emacs -nw'
alias emcsa='TERM=xterm-direct emacs -nw'
alias 'sudoemacs'='sudo TERM=xterm-direct emacs -nw'
alias 'ipscan'='sudo arp-scan --interface=eth0 --localnet'
alias pip=pip3

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

