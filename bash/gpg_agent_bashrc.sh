#
# gpg-agent initialization script for .bashrc
#
# cf  http://manpages.ubuntu.com/manpages/xenial/man1/gpg-agent.1.html
#     https://www.gnupg.org/documentation/manuals/gnupg/Agent-Examples.html#Agent-Examples
#     https://wiki.archlinux.org/index.php/GnuPG#gpg-agent

# Start the gpg-agent if not already running
if ! pgrep -x -u "${USER}" gpg-agent >/dev/null 2>&1; then
   gpg-connect-agent /bye >/dev/null 2>&1
fi

# Tell gpg which terminal to use
export GPG_TTY=$(tty)

# Enable ssh support
unset SSH_AGENT_PID
if [ "${gnupg_SSH_AUTH_SOCK_by:-0}" -ne $$ ]; then
    export SSH_AUTH_SOCK="${HOME}/.gnupg/S.gpg-agent.ssh"
fi