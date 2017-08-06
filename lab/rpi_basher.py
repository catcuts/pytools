# -*- coding:utf-8 -*-

import paramiko
import threading
import sys
import os
import re
import time

ip_part123 = "192.168.38."
supp_opts_text = ["0)返回","1)关机","2)重启","3)指定脚本","4)逐条输入"]
login_timout = 10

def ssh_client(ip,username,passwd,cmd):
    pass
#     try:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(ip,22,username,passwd,timeout=5)
#         for m in cmd:
#             stdin, stdout, stderr = ssh.exec_command(m)
# #           stdin.write("Y")   #简单交互，输入 ‘Y’ 
#             out = stdout.readlines()
#             #屏幕输出
#             for o in out:
#                 print o,
#         print '%s\tOK\n'%(ip)
#         ssh.close()
#     except :
#         print '%s\tError\n'%(ip)


def ssh_cmder(ssh,cmds):
    pass

def print_inline(preamble="",plist=[],delay=0,stop=False):

    if stop: 
        sys.stdout.write('\n')
    else:
        # sys.stdout.write(' ' * 1 + '\r')  # 从头（\r）覆盖
        sys.stdout.flush()  # 暂时输出

        for i in range(0,len(plist)):
            sys.stdout.write(preamble)  # 不换行
            sys.stdout.write(', '.join(plist[0:i+1]) + '\r')  # 从头（\r）覆盖
            sys.stdout.flush()  # 暂时输出
            time.sleep(delay)

if __name__ == '__main__':
    try:
        print("树莓派 IP 地址前 3 段已被设定为 192.168.38。可根据需要通过 ip_part123 来修改。")
        
        input_ip = True
        while input_ip:
            input_ip = False

            ip_part4s = re.sub(r"\s+",",",input("请输入需要批量操作的树莓派 IP 地址的第 4 段，并用空格隔开：")).split(",")

            input_opt = True
            while input_opt:
                input_opt = False
                cmd_nr = input(("树莓派"+" %s"*len(ip_part4s)+" 支持如下操作\n%s\n输入操作序号：") %(*tuple(ip_part4s),"\n".join(supp_opts_text)))
                # cmd = input(("树莓派 " + ", ".join(['{'+str(x)+'}' for x in range(0, len(ip_part4s))])).format(*tuple(ip_part4s)))

                cmds = []

                if cmd_nr == "0": input_ip = True
                elif cmd_nr == "1": cmds.append("sudo shutdown -h now")
                elif cmd_nr == "2": cmds.append("sudo shutdown -r now")
                elif cmd_nr == "3": 
                    input_cmd_fp = True
                    while input_cmd_fp:
                        input_cmd_fp = False
                        cmd_fp = input("输入脚本路径或按 0 返回：")
                        if cmd_fp == "0":
                            input_opt = True
                        elif os.path.isfile(cmd_fp):
                            with open(cmd_fp,"r") as cmd_f:
                                for cmd in cmd_f.readlines():
                                    cmds.append(cmd)
                        else:
                            input_cmd_fp = True
                else:
                    input_opt = True

            if not input_ip:
                username = "pi"  # 用户名
                passwd = "raspberry"   # 密码
                threads = []  # 多线程

                login_status = list(map(lambda x: x + "(...)",ip_part4s))
                ssh_co = []
                ssh_nc = []
                connect_ssh = True
                while connect_ssh:
                    connect_ssh = False
                    for i in range(0,len(ip_part4s)):
                        ip = ip_part123 + ip_part4s[i]
                        try:
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(ip,22,username,passwd,login_timout=10)
                            login_status[i] = login_status[i].replace("(...)","(成功)")
                            ssh_co.append(ssh)
                        except:
                            login_status[i] = login_status[i].replace("(...)","(失败)")
                            ssh_nc.append(ip_part4s[i])
                        
                        print_inline("登录树莓派：",login_status,1)

                    print_inline(stop=True)

                    if ssh_nc:
                        opt_ssh_nc = input("有 %d 粒树莓派登录失败，你是选择：\n1)重试\n2)忽略\n3)取消\n输入操作序号：" %len(ssh_nc))
                        if opt_ssh_nc == "1":
                            connect_ssh = True
                            ip_part4s = ssh_nc
                            login_status = list(map(lambda x: x + "(...)",ip_part4s))
                            ssh_nc = []
                        elif opt_ssh_nc == "2":
                            pass
                        else:
                            exit()

                print("批量操作中 ...")
                for ssh in ssh_co:
                    th = threading.Thread(target=ssh_cmder,args=(ssh,cmds))
                    th.start()

    except KeyboardInterrupt:
        print("bye")
        exit()
