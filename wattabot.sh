#!/bin/bash
## wattabot.sh
if pgrep -x "pigpiod"
then
    echo "pigpiod is running"
else
    echo "starting pigpiod"
    pigpiod
fi
sudo -u hedi python3 /home/hedi/wattabot/wattabot.py