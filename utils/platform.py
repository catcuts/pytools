# -*- coding:utf-8 -*-


import subprocess
import platform

# 分离功能的原则：有单独调用的需求

def platform(self):
    recognizable_pf = ["windows", "raspbian", "debian", "ubuntu", "centos"]
    for pf in recognizable_pf:
        if platformIs(pf): return pf
    return "unknown"


def platformIs(pf):
    cur_pf = platform.platform().lower()
    if pf in curpf:
        return True
    elif isRaspbian():
        return False


def isRaspbian(self):
    s = subprocess.Popen("head -n 1 /etc/issue", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return "raspbian" in s.communicate()[0].decode().lower()