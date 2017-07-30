# -*- coding:utf-8 -*-

# 测试内容：
#   1.  修改网络配置后：
#       1)  一个设备只能有一套配置
#       2)    

import unittest
import os
from changeNetwork import change_network_conf
from getNetwork import get_network_conf

fp = os.getcwd() + "test.conf"


class unitTest(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_change_network_conf(self):
        print("test_change_network_conf:")
        print("\t" + change_network_conf(dev="eth0", ip="192.168.39.112", netmask="255.255.255.0", gateway="192.168.39.1", dns_prefer="223.5.5.5", dns_alter="223.6.6.6"))
        # print("\t" + change_network_conf(dev="eth1", ip="", netmask="", gateway="", dns_prefer="", dns_alter=""))

    def test_get_network_conf(self):
        print("test_get_network_conf:")
        print("\t" + str(get_network_conf(dev="eth0")))

if __name__ == '__main__':
    unittest.main()