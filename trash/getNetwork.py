# -*- coding:utf-8 -*-

import os
import re

fp = os.path.join(os.getcwd(), "test.conf")

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

    #  整区匹配 \n[^#]*\s*interface\s(eth0)\s*\n\s*static\sip_address\s*=([^/]*)/(.*)\n\s*static\srouters\s*=(.*)\n\s*(static\sdomain_name_servers\s*=(.*))?\n*
    r_netconf = re.compile("\n[^#]*interface\\s(" + dev + ")\\s*\\n\\s*static\\sip_address\\s*=(.*)/(.*)\\n\\s*static\\srouters\\s*=(.*)\\n\\s*(static\\sdomain_name_servers\\s*=(.*))?\\n*")

    #  分段匹配
    # r_head = re.compile("[^#]interface\\s*(" + dev + ")\\s*")  #  网卡设备
    # r_ip = re.compile("[^#]\\s*(static\\sip_address=.*)")  # ip地址/子网掩码
    # r_gateway = re.compile("[^#]\\s*(static\srouters=.*)")  # 路由器/网关地址
    # r_dns = re.compile("[^#]\\s*(static\\sdomain_name_servers=.*)")  # dns地址

    #  初始化
    netconf = {"dev": {"ip": "", "nm": "", "gw": ""}} 

    #  生成网络配置字典
    with open(fp, "r") as f:
        fc = f.read()
        m_netconf = re.search(r_netconf, fc)
        if m_netconf:
            netconf["dev"] = m_netconf.group(1)
            netconf["ip"] = m_netconf.group(2)
            netconf["nm"] = decode_netmask(m_netconf.group(3))
            netconf["gw"] = m_netconf.group(4)
            if len(m_netconf.groups()) == 6: netconf["dns"] = m_netconf.group(6)

    #  返回网络设置字典
    return netconf

if __name__ == "__main__":
    pass