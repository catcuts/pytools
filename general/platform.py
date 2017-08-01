# -*- coding:utf-8 -*-

import subprocess
import platform

def getPlatform(self):
    def isRaspbian(self):
        """
        @attention: check if the platform of the system is raspbian
        """  
        s = subprocess.Popen("head -n 1 /etc/issue", shell=True, stdout=subprocess.PIPE)
        return "raspbian" in s.communicate()[0].decode().lower()

    try:
        platForm = platform.platform().lower()
        if "ubuntu" in platForm:
            currentPlatForm = "ubuntu"
        elif "centos" in platForm:
            currentPlatForm = "centos"
        elif isRaspbian():
            currentPlatForm = "raspbian"
        elif "debian" in platForm:
            currentPlatForm = "debian"
        elif "windows" in platform:
            currentPlatForm = "windows"
        else:
            currentPlatForm = "unsupported"
    except:
        currentPlatForm = "unknown"

    return currentPlatForm
    