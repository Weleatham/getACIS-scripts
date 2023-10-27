#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
###############################################################################
# Script Created by William Leatham IV in October of 2023
# Description:
# This program created to check if a directory structure exists and creates it 
# if it does not.
###############################################################################
"""
import os
def folder_check(*args):
    usrdir = os.path.expanduser('~')+"/"
    cwd = os.getcwd()+"/"
    if len(args) == 0:
        print("Saving in current working dir, make sure this is right: "+cwd)
        return(cwd)
    elif len(args) >= 1:
        wrkdir = "/".join(str(arg) for arg in args)
        if not os.path.exists(usrdir+wrkdir):
            os.makedirs(usrdir+wrkdir)
            print("Output directory created: "+usrdir+wrkdir+"/")
            return(usrdir+wrkdir+"/")
        else:
            return(usrdir+wrkdir+"/")
            print("Directory exists. Saving in: "+usrdir+wrkdir+"/")
if __name__ == '__main__':
    # Running the folder check.
    folder_check()
