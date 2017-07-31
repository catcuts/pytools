# -*- coding:utf-8 -*-

# Raspbian 正则
def network_conf_rpi(dev):
    return "\\n[^#]*interface\\s(" + dev + ")\\s*\\n\\s*static\\sip_address\\s*=(.*)/(.*)\\n\\s*static\\srouters\\s*=(.*)\\n\\s*(static\\sdomain_name_servers\\s*=(.*))?\\n*"  # 获取 ip / netmask / gateway
                            # \n[^#]*\s*interface\s(eth0)\s*\n\s*static\sip_address\s*=([^/]*)/(.*)\n\s*static\srouters\s*=(.*)\n\s*(static\sdomain_name_servers\s*=(.*))?\n*
