# -*- coding:utf-8 -*-

def codeNetmask(self,netmask):
        """
        @attention: code netmask to part of ip formated like 192.168.0.103/24.
                    return '/24'(in this example) or ''(no set)
        """ 
        netmask_parts = netmask.split(".")
        code = 0
        try:
            for part in netmask_parts:
                code += bin(int(part)).count("1")
            code = "/" + str(code)
        except:
            code = ""
        return str(code)