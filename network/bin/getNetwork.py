# -*- coding:utf-8 -*-


import os
import re
import subprocess

from network.var import path, regexp, cmd

def get_network_conf(dev):

    def decode_netmask(code):  # eg: "24" -> "255.255.255.0"
        code = code.replace("/", "")
        code = "1"*int(code) + "0"*(32 - len(code))
        netmask = ""
        if code:
            for i in range(0, 4):
                netmask = netmask + str(int(code[i*8:i*8+8], 2)) + "."
        netmask = netmask[:-1]
        return netmask

    fp = path.dhcpcd_conf_rpi

    # 命令行
    c_ip_nm_conf = cmd.ip_nm_conf_r_rpi
    c_gw_conf = cmd.gw_conf_r_rpi

    s_ip_nm_conf = subprocess.Popen(c_ip_nm_conf, shell=True, stdout=subprocess.PIPE)
    ip_nm_conf = s_ip_nm_conf.communicate()[0].decode().split("\n")

    c_gw_conf = subprocess.Popen(c_ip_nm_conf, shell=True, stdout=subprocess.PIPE)
    gw_conf = c_gw_conf.communicate()[0].decode().split("\n")

    #  匹配
    r_ip_nm_conf = re.compile(regexp.ip_nm_conf_r_rpi(dev))  # ip netmask
    r_gw_conf = re.compile(regexp.gw_conf_r_rpi(dev))  # gateway
    r_dns_conf = re.compile(regexp.dns_conf_r_rpi)  # dns

    #  初始化
    netconf = {"dev": {"ip": "", "nm": "", "gw": "", "dns_prefer": "", "dns_alter": ""}} 

    #  生成网络配置字典
    m_ip_nm_conf = re.search(r_ip_nm_conf, c_ip_nm_conf)
    m_gw_conf = re.search(r_gw_conf, c_gw_conf)
    with open(fp, "r") as f:
        c_dns_conf = f.read()
        m_dns_conf = re.search(r_dns_conf, c_dns_conf)

    if m_ip_nm_conf:
        netconf["dev"] = m_ip_nm_conf.group(1)
        netconf["ip"] = m_ip_nm_conf.group(2)
        netconf["nm"] = decode_netmask(m_ip_nm_conf.group(3))
    
    if m_gw_conf:
        netconf["gw"] = m_gw_conf.group(1)
    
    if m_dns_conf:
        netconf["dns_prefer"] = m_dns_conf.group(1)
        netconf["dns_alter"] = m_dns_conf.group(2) if len(m_dns_conf.groups()) == 3 else ""

    #  返回网络设置字典
    return netconf

if __name__ == "__main__":
    pass