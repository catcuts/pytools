# -*- coding:utf-8 -*-


# 命名规则：<匹配组1名>_<匹配组2名>_<匹配组3名>_..._<匹配组n名>_<描述>_<r(读)|w(写) (不指定则无差别)>_<平台名>
# 如果组太多，可以用：<匹配集名(只能有一个)>_<描述>_<auto(自动)|manu(手动) (不指定则无差别)>_<平台名>


# Raspbian 正则
def network_conf_w_rpi(dev):  # 匹配手动配置的 ip / netmask / gateway / dns
    return "\\n[^#]*interface\\s(" + dev + ")\\s*\\n\\s*static\\sip_address\\s*=(.*)/(.*)\\n\\s*static\\srouters\\s*=(.*)\\n\\s*(static\\sdomain_name_servers\\s*=(.*))?\\n*"  
                            # \n[^#]*\s*interface\s(eth0)\s*\n\s*static\sip_address\s*=([^/]*)/(.*)\n\s*static\srouters\s*=(.*)\n\s*(static\sdomain_name_servers\s*=(.*))?\n*


def ip_nm_conf_r_rpi(dev):
    return "(" + dev + ")\\s+.+\\n\\s+inet\\saddr:(\\d+\\.\\d+\\.\\d+\\.\\d+)\\s+.*Mask:(\\d+\\.\\d+\\.\\d+\\.\\d+)"
        # "(eth0)\s+.+\n\s+inet\saddr:(\d+\.\d+\.\d+\.\d+)\s+.*Mask:(\d+\.\d+\.\d+\.\d+)"


def gw_conf_r_rpi(dev):
    return ""


dns_conf_r_rpi = "nameserver\\s(\\d+\\.\\d+\\.\\d+\\.\\d+)\\s*\\nnameserver\\s(\\d+\\.\\d+\\.\\d+\\.\\d+)*\\s*"  # 匹配手动设置的 dns
                # nameserver\s(\d+\.\d+\.\d+\.\d+)\s*\nnameserver\s(\d+\.\d+\.\d+\.\d+)*\s*