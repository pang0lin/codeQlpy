#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import io
import sys
import shutil
import pathlib
import zipfile
import subprocess

from utils.log    import log
from utils.option import qlConfig

def readFile(filepath):
    if not os.path.isfile(filepath):
        return ""
    with open(filepath) as r:
        return r.read()

def dirFiles(dirpath):
    ret = []
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        if os.path.isfile(filepath):
            ret.append(filename)
    return ret

def delDirFile(path):
    if os.path.isfile(path):
        os.remove(path)
        return True
    if os.path.isdir(path):
        shutil.rmtree(dir_path)
        return True
    return False

def unzipFile(filepath, save_path=False):
    if not save_path:
        save_path = os.path.join(os.path.dirname(filepath), ".".join(os.path.basename(filepath).split(".")[:-1]))
    if not os.path.isfile(filepath):
        log.error(f"unzip file {filepath} is not exists")
        return False
    # if not os.path.isdir(save_path):
    #     log.error(f"unzip savepath {filepath} is not exists")
    #     return False

    f = zipfile.ZipFile(filepath,'r')
    for file in f.namelist():
        f.extract(file, save_path)               # 解压位置
    f.close()
    return save_path

def copyFile(srcpath, destpath):
    if srcpath == destpath:
        return False
    dest_dirname = os.path.dirname(destpath)
    if not os.path.isdir(dest_dirname):
        os.makedirs(dest_dirname)
    if not os.path.isfile(srcpath):
        log.error(f"{srcpath} is not exists")
        return False
    shutil.copy(srcpath, destpath)

def execute(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
    proc.wait()
    stream_stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8')
    stream_stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8')
    str_stdout = stream_stdout.read()
    if qlConfig("debug").lower() == "on":
        str_stderr = stream_stderr.read()
        log.warning(str_stderr)
    
    return str_stdout


def cvsClean(content):
    return content.replace(",", " ").replace("\n", " ")

def getFilesFromPath(filepath, extension):
    return pathlib.Path(filepath).glob(f'**/*.{extension}')

def execJar(args, version=8):
    if version == 8:
        jdk = qlConfig("jdk8")
    else:
        jdk = qlConfig("jdk11")

    if isinstance(args,list):
        args = " ".join(args)
    exec_str = jdk  + args
    return execute(exec_str)

    