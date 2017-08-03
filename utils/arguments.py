# -*- coding:utf-8 -*-


def arguments_values(loca):
    argvs = []
    for key in loca.keys:
        argvs.append(loca[key])
    return tuple(argvs)