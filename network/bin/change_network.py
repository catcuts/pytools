# -*- coding:utf-8 -*-

import os
import re

from network.var import path, regexp
from utils.platform_wrapper import *
from utils.arguments import *

def change_network_conf(ip, netmask, gateway, dev="eth0", dns_prefer="", dns_alter=""):

    argvs = arguments_values(locals())

    if platform_is("raspbian"): change_network_conf_rpi(*argvs)  # 有点像平台策略管理器


def change_network_conf_rpi(ip, netmask, gateway, dev="eth0", dns_prefer="", dns_alter=""):
    fp = path.dhcpcd_conf_rpi

    #  整区匹配
    r_netconf = re.compile(regexp.network_conf_w_rpi(dev))

    #  分段匹配
    # r_head = re.compile("[^#]interface\\s*(" + dev + ")\\s*")  #  网卡设备
    # r_ip = re.compile("[^#]\\s*(static\\sip_address=.*)")  # ip地址/子网掩码
    # r_gateway = re.compile("[^#]\\s*(static\srouters=.*)")  # 路由器/网关地址
    # r_dns = re.compile("[^#]\\s*(static\\sdomain_name_servers=.*)")  # dns地址

    # 开始 -> 构造 -> 替换/追加 -> 写入 -> 结束
    # 一个生命周期从开始到结束
    # 每个环节都应该是尽量互相独立的，保证低耦合，高可维护，易扩展
    # 如果需要更新某个环节，则不影响其他环节
    # 如果需要加入某个环节，应继续保证与其他环节独立

    if not (ip or netmask or gateway):  # 重置
        new_netconf = ""
    else:  # 非重置
        #  初始化
        line_head = "interface " + dev
        line_ipnm = " static ip_address=" + ip + "/" + code_netmask(netmask)
        line_gw = " static routers=" + gateway
        if dns_prefer:
            line_dns = " static domain_name_servers=" + dns_prefer + " " + dns_alter
        else:
            line_dns = ""

        #  构造新配置区
        new_netconf = "\n\n\n" + "\n".join([line_head, line_ipnm, line_gw, line_dns])

    #  新配置替换原配置
    with open(fp, "r") as f:
        fc = f.read()
        m_netconf = re.search(r_netconf, fc)
        if m_netconf:  # 找到原配置则替换
            fc = re.sub(r_netconf, new_netconf, fc)
        else:  # 没有原配置则追加
            fc = fc + new_netconf

    #  写入配置文件
    with open(fp, "w") as f:
        f.write(fc)
   

def code_netmask(netmask):  # eg: "255.255.255.0" -> "24"
    netmask_parts = netmask.split(".")
    code = 0
    try:
        for part in netmask_parts:
            code += bin(int(part)).count("1")
    except:
        code = ""
    return str(code)

         
if __name__ == "__main__":
    pass
