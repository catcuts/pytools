# -*- coding:utf-8 -*-


import unittest
from utils.platform_wrapper import *

class unitTest(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        self.assertEquals(is_raspbian(), False)
        self.assertEquals(platform_is("windows"), True)
        self.assertEquals(platform_name(), "windows")

if __name__ == '__main__':
    unittest.main()
