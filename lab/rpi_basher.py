# -*- coding:utf-8 -*-
#!/usr/bin/env python3

import paramiko
import threading
import sys
import os
import re
import time
from paramiko_expect import SSHClientInteraction

ip_part123 = "192.168.116."
supp_opts_text = ["\t00)返回","\t01)关机","\t02)重启","\t03)指定脚本","\t04)逐条输入"]
login_timeout = 10

cmder_count = 0
cmder_status = []

su_passwd = "hhh"
su_prompt = "root@raspberrypi:/home/pi#\s+"

default_expect = "pi@raspberrypi.*"

def ssh_cmder(ip,ssh,cmds):
    global cmder_count, cmder_status
    
    if cmder_status: 
        cmder_status[-1] = cmder_status[-1].replace(" ...","")
    cmder_count -= 1

    try:
        interact = SSHClientInteraction(ssh, timeout=10, display=False)
        interact.expect(default_expect)
        # cmds = ['ls']
        count = 0
        m = False
        failure_caused_by_shutdown = False
        for cmd in cmds:
            if ("shutdown" in cmd) or ("reboot" in cmd):
                failure_caused_by_shutdown = True
            if m:
                interact.expect(m.group(1))
            else:
                interact.send(cmd)  # 每个 send 后必须跟 expect
                if count < (len(cmds) - 1):
                    m = re.search(r"^expect:\s+(.*)", cmds[count + 1])
                if not m:
                    interact.expect(default_expect)
                cmd_output_uname = interact.current_output_clean
                print("cmd_output_uname: %s" %cmd_output_uname)
            count+=1
        ssh.close()
        cmder_status.append("%s(成功) ..." %ip)
    except:
        ssh.close()
        if failure_caused_by_shutdown:
            cmder_status.append("%s(成功) ..." %ip)
        else:
            cmder_status.append(("%s(失败) ...\n" + interact.current_output_clean + "\n") %ip)

    print_inline(plist=cmder_status)

    if cmder_count == 0:
        print_inline(stop=True)

    if cmder_count == 0:
        next_wish = input("选择继续(y) 或 退出(N)：")
        input_wish = True
        while input_wish:
            input_wish = False
            if next_wish == "y" or next_wish == "Y":
                main()
            elif next_wish == "N":
                exit()
            elif next_wish == "n":
                next_wish = input("用大写 N 退出，或选择继续(y)：")
                input_wish = True
            else:
                input_wish = True

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

def main():
    global cmder_count
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

                if cmd_nr == "00": input_ip = True
                elif cmd_nr == "01": cmds.append("sudo shutdown -h now")
                elif cmd_nr == "02": cmds.append("sudo shutdown -r now")
                elif cmd_nr == "03": 
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
                ssh_co = {}
                ssh_nc = []
                connect_ssh = True
                while connect_ssh:
                    connect_ssh = False
                    for i in range(0,len(ip_part4s)):
                        ip = ip_part123 + ip_part4s[i]
                        try:
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(ip,22,username,passwd,timeout=login_timeout)
                            login_status[i] = login_status[i].replace("(...)","(成功)")
                            ssh_co[ip_part4s[i]] = ssh
                        except:
                            login_status[i] = login_status[i].replace("(...)","(失败)")
                            ssh_nc.append(ip_part4s[i])
                        
                        print_inline("登录树莓派：",login_status,1)

                    print_inline(stop=True)

                    if ssh_nc:
                        opt_ssh_nc = input("有 %d 粒树莓派登录失败，你是选择：\n\t1)重试\n\t2)忽略\n\t3)取消\n输入操作序号：" %len(ssh_nc))
                        if opt_ssh_nc == "1":
                            connect_ssh = True
                            ip_part4s = ssh_nc
                            login_status = list(map(lambda x: x + "(...)",ip_part4s))
                            ssh_nc = []
                        elif opt_ssh_nc == "2":
                            pass
                        else:
                            exit()
 
                print_inline(preamble="批量操作中 ...",plist=[""],delay=1)

                for ip_p4 in ssh_co:
                    cmder_count += 1
                    th = threading.Thread(target=ssh_cmder,args=(ip_p4,ssh_co[ip_p4],cmds))
                    th.start()

    except KeyboardInterrupt:
        print("bye")
        exit()

if __name__ == '__main__':
    main()
