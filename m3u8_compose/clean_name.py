#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import os
import sys
import subprocess
#file_name = "当时的sdsおはようございますbbbbb!@#$%^&*(){}【】「「」|dddd～@#\%……&***（）-+——+「」|：“？》《\~    ～\":><?~aaaa"
#ile_name = "在线播放 - 043019_841 ローションエロエロくねくねダンス〜あいら - sss视频 sss.txt"
#print os.getcwd()

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
    #print file_name
    return file_name


#mv_files()
