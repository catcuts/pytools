# -*- coding:utf-8 -*-

import re

def changeNetWork(dev, (ip, netmask, gateway, dns_prefer="", dns_alter="")):
  fp = "C:\\Users\\Administrator\\Desktop\  est.conf"

  r_netconf = re.compile("^interface\s" + dev + "\s*\n\s*static\sip_address\s*=.*\n\s*static\srouters\s*=.*\n\s*static\sdomain_name_server\s*=.*\n*")

  with open(fp, "r") as f:
    fc = f.read()
    m_netconf = re.search()


if __name__ == "__main__":
  ipPattern = re.compile("\s*static\sip_address=.*") #ip地址/子网掩码
  routersPattern = re.compile("\s*static\srouters=.*") #路由器/网关地址
  dnsPattern = re.compile("\s*static\sdomain_name_servers=.*") #dns地址