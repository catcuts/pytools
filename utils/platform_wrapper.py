# -*- coding:utf-8 -*-

import subprocess
import platform

# 分离功能的原则：有单独调用的需求


def platform_name():  # 如果命名为 platform 则覆盖上面 import 的 platform
    recognizable_pf = ["windows", "raspbian", "debian", "ubuntu", "centos"]
    cur_pf = "unknown"
    for pf in recognizable_pf:
        if platform_is(pf):
            cur_pf = pf
            break
    return cur_pf


def platform_is(pf):
    cur_pf = platform.platform().lower()
    if pf in cur_pf:
        return True
    elif is_raspbian() and pf == "raspbian":
        return True
    else:
        return False


def is_raspbian():
    s = subprocess.Popen("head -n 1 /etc/issue", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return "raspbian" in s.communicate()[0].decode().lower()
