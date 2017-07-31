# -*- coding:utf-8 -*-

import os

import env

# Raspbian 路径
dhcpcd_conf_rpi = '/etc/dhcpcd.conf' if not env.test \
    else os.path.join(os.getcwd(), "test.dhcpcd.conf")  # 配置 ip / netmask / gateway / dns
                
resolv_conf_rpi = '/etc/resolv.conf' if not env.test \
    else os.path.join(os.getcwd(), "test.resolv.conf") # 获取 dns
