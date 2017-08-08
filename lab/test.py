# -*- coding:utf-8 -*-


import unittest
import paramiko
from paramiko_expect import SSHClientInteraction

PROMPT = "root@raspberrypi:/home/pi#\s+"

class unitTest(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ssh_client(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("192.168.38.175",22,"pi","raspberry",timeout=10)
            print("登录成功")
        except:
            print("登录失败")

        try:
            interact = SSHClientInteraction(ssh, timeout=10, display=True)
            interact.send("su")
            interact.expect("Password:\s+")
            interact.send("hhh")
            interact.expect(PROMPT)
        except:
            print("切换 root 失败")

if __name__ == '__main__':
    unittest.main()
