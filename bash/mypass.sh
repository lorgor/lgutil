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

# 161205 Quick & dirty fn to call yubioath

function yubi() {
    killall gpg-agent
    /usr/local/bin/yubioath gui
}

# 190401 Quick & dirty fn to set 4K mode for Samsung U28E590 4K monitor

function set4k() {
    xrandr --newmode "3840x2160" 553.01 3840 3890 3940 3990  2160 2210 2260 2310 -hsync +vsync && \
    xrandr --addmode Virtual1 3840x2160 && \
    xrandr --output Virtual1 --mode 3840x2160 | xrandr -s 2560x1600
}
