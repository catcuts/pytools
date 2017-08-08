# -*- coding:utf-8 -*-


import unittest
from utils.testing import on_off
from utils.platform_wrapper import *

SWITCHES = {
    "test_in_windows":True,
    "test_in_raspbian":False
}

class unitTest(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @on_off(SWITCHES)
    def test_in_windows(self):
        self.assertEquals(is_raspbian(), False)
        self.assertEquals(platform_is("windows"), True)
        self.assertEquals(platform_name(), "windows")

    @on_off(SWITCHES)
    def test_in_raspbian(self):
        self.assertEquals(is_raspbian(), True)
        self.assertEquals(platform_is("raspbian"), True)
        self.assertEquals(platform_name(), "raspbian")

if __name__ == '__main__':
    unittest.main()
