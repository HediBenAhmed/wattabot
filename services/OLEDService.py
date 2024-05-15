from drivers.OLED import OLED
from services.Service import Service
import subprocess


class OLEDService(Service):

    def __init__(self):
        self.OLED = OLED()

    def displaySystemInfo(self):
        cmd = "hostname -I | cut -d' ' -f1"
        IP = subprocess.check_output(cmd, shell=True)
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True)
        cmd = "/usr/bin/vcgencmd measure_temp"
        CPUT = subprocess.check_output(cmd, shell=True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True)
        cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%dGB %s", $3,$2,$5}\''
        Disk = subprocess.check_output(cmd, shell=True)

        self.OLED.displayTexts(
            ["IP: " + str(IP), str(CPU), str(CPUT), str(MemUsage), str(Disk)]
        )


OLED_SERVICE = OLEDService()
