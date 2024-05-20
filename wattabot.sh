#!/bin/bash
## wattabot.sh
if pgrep -x "pigpiod"
then
    echo "pigpiod is running"
else
    echo "starting pigpiod"
    pigpiod
fi
python3 /home/hedi/wattabot/wattabot.py