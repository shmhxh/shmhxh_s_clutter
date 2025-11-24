#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python工具箱打包脚本
使用PyInstaller将应用程序打包为可执行文件
"""

import os
import sys
import subprocess
import shutil

def package_app():
    """打包应用程序"""
    # 项目根目录
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 确保dist目录存在
    dist_dir = os.path.join(root_dir, 'dist')
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    
    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--onefile',  # 生成单个可执行文件
        '--windowed',  # 无控制台窗口（GUI应用）
        '--name=PythonToolbox',  # 可执行文件名称
        '--add-data=python_toolbox\tools;python_toolbox/tools',  # 添加工具目录
        '--add-data=python_toolbox\config;python_toolbox/config',  # 添加配置目录
        '--icon=None',  # 图标文件（可选）
        '--distpath', dist_dir,  # 输出目录
        'python_toolbox_gui.py'  # 主程序入口
    ]
    
    print(f"执行打包命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, cwd=root_dir, check=True, capture_output=True, text=True)
        print("打包成功!")
        print("标准输出:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        print("标准错误:")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"打包过程中发生意外错误: {e}")
        return False

if __name__ == '__main__':
    print("Python工具箱打包脚本")
    print("=" * 40)
    print("正在打包应用程序...")
    
    if package_app():
        print("\n打包完成! 可执行文件已生成在 dist 目录中")
        sys.exit(0)
    else:
        print("\n打包失败!")
        sys.exit(1)