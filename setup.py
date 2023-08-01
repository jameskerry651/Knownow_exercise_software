#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'James'
import sys
from cx_Freeze import setup, Executable

# 判断windows系统
if sys.platform == 'win32':
    base = 'Win32GUI'

build_options = {
    "packages": ["random", "pandas", "PyQt5"],   # 需要包含的额外包
    "excludes": ["tkinter"],            # 需要排除的模块
    "include_files": [],                # 需要包含的额外文件（如果有的话）
    "build_exe": "build"                # 打包输出目录
}

executables = [
    Executable(
        'main.py'  # 入口文件
        , base=base
        , target_name='KnowNow.exe'  # 生成的exe的名称
        , icon="./ui/cat.png"  # 生成的exe的图标
    )
]


setup(name='KnowNow',
      version='1.0',
      description='This project is designed for daily practice of skills in a specific field, especially exam questions.',
      options={"build_exe": build_options},
      executables=executables
      )

