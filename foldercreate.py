#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
###############################################################################
# Script Created by William Leatham IV in October of 2023
# Description:
# This program created to check if a directory exists and creates it if it 
# does not.
###############################################################################
"""
import os
def folder_check():
    usrdir = os.path.expanduser('~')+"/DataRequests/"
# Checking if the main output directory exists and if it does not then it 
# creates it. Along with subdirectories.
    if not os.path.exists(usrdir):
        os.makedirs(usrdir)
        print("Output directory created: "+usrdir)
        
    if not os.path.exists(usrdir+"/ACIS/"):
        os.makedirs(usrdir+"ACIS/")
        print("Output subdirectory created!: "+usrdir+"ACIS/")
        
    return(usrdir+"ACIS/")
if __name__ == '__main__':
    # Running the folder check.
    folder_check()
