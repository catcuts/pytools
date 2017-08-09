# -*- coding:utf-8 -*-


import unittest
import os
from network.bin.change_network import change_network_conf
from network.bin.get_network import get_network_conf

class unitTest(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_change_network_conf(self):
        # 测试内容：
        # 1. 配置文件内无 eth0 的相关配置，即 eth0 为自动配置
        # 2. 给 eth0 进行主动配置，不出错，配置完后，配置文件包含 / 不包含 eth0 的配置信息
        #   2.1. ip / netmask / gateway 均不为空
        #       2.1.1. dns_prefer / dns_alter 为空与否四种情况 => 包含预期的 eht0 配置信息
        #   2.2. ip / netmask / gateway 均为空
        #       2.2.1. dns_prefer / dns_alter 为空与否四种情况 => 不包含 eth0 的配置信息
        # 3. 修改 eth0 的配置，轮流修改，均不出错，且达预期
        # 4. 给 eth1 进行主动配置，重复 2 / 3/ 4
        # 5. 复位 eht0 为自动配置，配置文件不包含 eht0 的配置信息，且包含 eth1 的配置信息不变
        # 6. 复位 eht1 为自动配置，配置文件不包含 eht1 的配置信息
        # 7. 检查上述 6 步测试后，配置文件是否与测试前相同
        change_network_conf(dev="eth0", ip="192.168.38.112", netmask="255.255.255.0", gateway="192.168.38.1", dns_prefer="223.5.5.5", dns_alter="223.6.6.6")

    def test_get_network_conf(self):
        print("test_get_network_conf:")
        print("\t" + str(get_network_conf(dev="eth0")))

if __name__ == '__main__':
    unittest.main()
