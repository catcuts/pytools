# -*- coding:utf-8 -*-


import unittest
import subprocess


class unitTest(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ssh_client(self):
        subprocess.Popen("python3 -m rpi_basher.py", shell=True)

if __name__ == '__main__':
    unittest.main()
