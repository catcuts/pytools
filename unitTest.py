# -*- coding:utf-8 -*-

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
        print("\t" + change_network_conf(dev="eth0", ip="192.168.39.112", netmask="255.255.255.0", gateway="192.168.39.1"))

    def test_get_network_conf(self):
        print("test_get_network_conf:")
        print("\t" + str(get_network_conf(dev="eth0")))

if __name__ == '__main__':
    unittest.main()
