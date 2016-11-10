# 161030 Simplistic code inspired by pass
# Quick and dirty fix bug in VM setting
# Source in .bashrc script

function mypass() {
    local sleep_argv0="password store sleep"
    pkill -f "^$sleep_argv0" 2>/dev/null && sleep 0.5

    # Copy 1st line of passwd to clipboard
    # Remove trailing cr

    pass $1 | head -n1 |  tr -d '\n'| xsel -b -i
    ( ( exec -a "$sleep_argv0" sleep 45 )
        # clear the clipboard brutally
        /usr/bin/xsel -b -c
    ) 2>/dev/null & disown
}
