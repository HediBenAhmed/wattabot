#!/bin/bash
## wattabot.sh
if pgrep -x "pigpiod"
then
    echo "pigpiod is running"
else
    echo "starting pigpiod"
    pigpiod
fi
/home/hedi/.pyenv/versions/3.8.19/bin/python /home/hedi/wattabot/WebControl.py