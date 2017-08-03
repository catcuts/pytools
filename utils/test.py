# -*- coding:utf-8 -*-


import unittest
from platform_wrapper import *

class unitTest(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

#    def test_in_windows(self):
#        self.assertEquals(is_raspbian(), False)
#        self.assertEquals(platform_is("windows"), True)
#        self.assertEquals(platform_name(), "windows")

    def test_in_raspbian(self):
#        self.assertEquals(is_raspbian(), True)
#        self.assertEquals(platform_is("raspbian"), True)
        self.assertEquals(platform_name(), "raspbian")

if __name__ == '__main__':
    unittest.main()
