# -*- coding:utf-8 -*-

import os
import re

fp = os.path.join(os.getcwd(), "test.conf")


def change_network_conf(ip, netmask, gateway, dev="", dns_prefer="", dns_alter=""):

    def code_netmask(netmask):  # eg: "255.255.255.0" -> "24"
        netmask_parts = netmask.split(".")
        code = 0
        try:
            for part in netmask_parts:
                code += bin(int(part)).count("1")
        except:
            code = ""
        return str(code)

    def decode_netmask(code):  # eg: "24" -> "255.255.255.0"
        code = code.replace("/", "")
        code = "1"*int(code) + "0"*(32 - len(code))
        netmask = ""
        if code:
            for i in range(0, 4):
                netmask = netmask + str(int(code[i*8:i*8+8], 2)) + "."
        netmask = netmask[:-1]
        return netmask

    #  整区匹配
    r_netconf = re.compile("interface\\s(" + dev + ")\\s*\\n\\s*static\\sip_address\\s*=(.*)/(.*)\\n\\s*static\\srouters\\s*=(.*)\\n\\s*static\\sdomain_name_servers\\s*=(.*)*\\n*")

    #  分段匹配
    # r_head = re.compile("[^#]interface\\s*(" + dev + ")\\s*")  #  网卡设备
    # r_ip = re.compile("[^#]\\s*(static\\sip_address=.*)")  # ip地址/子网掩码
    # r_gateway = re.compile("[^#]\\s*(static\srouters=.*)")  # 路由器/网关地址
    # r_dns = re.compile("[^#]\\s*(static\\sdomain_name_servers=.*)")  # dns地址

    #  初始化
    line_head = "interface " + dev
    line_ipnm = " static ip_address=" + ip + "/" + code_netmask(netmask)
    line_gw = " static routers=" + gateway
    if dns_prefer:
        line_dns = " static domain_name_servers=" + dns_prefer + " " + dns_alter
    else:
        line_dns = ""

    #  构造新配置区
    new_netconf = "\n".join([line_head, line_ipnm, line_gw, line_dns])

    #  新配置替换原配置
    with open(fp, "r") as f:
        fc = f.read()
        m_netconf = re.search(r_netconf, fc)
        if m_netconf:  # 找到原配置则替换
            fc = re.sub(r_netconf, new_netconf, fc)
        else:  # 没有原配置则追加
            fc = fc + "\n\n" + new_netconf

    #  写入配置文件
    with open(fp, "w") as f:
        f.write(fc)

    if m_netconf:
        return m_netconf.groups()
    else:
        return "no matched"
        
if __name__ == "__main__":
    pass