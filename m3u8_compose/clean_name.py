#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import os
import sys
import subprocess

def mv_files():
    dir_name = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    current_dir = os.getcwd()
    os.chdir("..")
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    os.chdir(current_dir)
    #print os.getcwd()
    cmd = "mv *.mp4 ../" + dir_name
    #os.system(cmd)
    returnCode = subprocess.call(cmd, shell=True)
    return returnCode
    
def clean_file_name(file_name):
    #print file_name
    file_name = file_name.replace("b","D").replace("(","_") \
        .replace(")","_").replace("（","_") \
        .replace("）","_").replace("!","_") \
        .replace("！","_").replace("@","_") \
        .replace("@","_").replace("#","_") \
        .replace("#","_").replace("$","_") \
        .replace("%","_").replace("%","_") \
        .replace("^","_").replace("&","_") \
        .replace("&","_").replace("*","_") \
        .replace("*","_").replace("——","_") \
        .replace("+","_").replace("[","_") \
        .replace("「","_").replace("[","_") \
        .replace("「","_").replace("]","_") \
        .replace("」","_").replace("|","_") \
        .replace("|","_").replace("\\","_") \
        .replace("、","_").replace(".","_") \
        .replace("。","_").replace("'","_") \
        .replace("‘","_").replace(";","_") \
        .replace("；","_").replace("“","_") \
        .replace("”","_").replace("\"","_") \
        .replace("\'","_").replace("‘","_") \
        .replace(":","_").replace("：","_") \
        .replace("’","_").replace(",","_") \
        .replace("，","_").replace("?","_") \
        .replace("？","_").replace("/","_") \
        .replace("/","_").replace("·","_") \
        .replace("`","_").replace("《","_") \
        .replace("》","_").replace(">","_") \
        .replace("<","_").replace("……","_") \
        .replace("=","_").replace("=","_") \
        .replace("…","_").replace("{","_") \
        .replace("}","_").replace("【","_") \
        .replace("】","_").replace("～","_") \
        .replace("~","_").replace(" ","_") \
        .replace(" ","_")
    return file_name


#mv_files()
