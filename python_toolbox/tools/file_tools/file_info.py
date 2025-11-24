#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件信息查看工具
用于查看文件的详细信息，如大小、创建时间、修改时间等
"""

import os
import time
import platform
from datetime import datetime


def get_file_info(file_path):
    """
    获取文件的详细信息
    
    Args:
        file_path: 文件路径
    
    Returns:
        dict: 包含文件信息的字典
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return None, f"错误: 文件 '{file_path}' 不存在"
        
        # 检查是否为文件
        if not os.path.isfile(file_path):
            return None, f"错误: '{file_path}' 不是一个文件"
        
        # 获取文件基本信息
        stat_info = os.stat(file_path)
        
        # 构建文件信息字典
        file_info = {
            '文件名': os.path.basename(file_path),
            '文件路径': os.path.abspath(file_path),
            '文件大小': f"{stat_info.st_size} 字节 ({stat_info.st_size / 1024:.2f} KB)",
            '创建时间': datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            '修改时间': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            '访问时间': datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            '文件权限': oct(stat_info.st_mode)[-3:],
            '文件类型': '文件',
            '是否为符号链接': os.path.islink(file_path)
        }
        
        # 尝试获取文件扩展名
        _, ext = os.path.splitext(file_path)
        if ext:
            file_info['文件扩展名'] = ext[1:].upper()  # 去除点号并转为大写
        
        # 尝试获取文件所有者信息（在Windows上可能不可用）
        if platform.system() != 'Windows':
            try:
                import pwd
                import grp
                file_info['所有者'] = pwd.getpwuid(stat_info.st_uid).pw_name
                file_info['所属组'] = grp.getgrgid(stat_info.st_gid).gr_name
            except:
                pass
        
        return file_info, None
    
    except Exception as e:
        return None, f"获取文件信息时发生错误: {str(e)}"


def get_directory_info(dir_path):
    """
    获取目录的详细信息
    
    Args:
        dir_path: 目录路径
    
    Returns:
        dict: 包含目录信息的字典
    """
    try:
        # 检查目录是否存在
        if not os.path.exists(dir_path):
            return None, f"错误: 目录 '{dir_path}' 不存在"
        
        # 检查是否为目录
        if not os.path.isdir(dir_path):
            return None, f"错误: '{dir_path}' 不是一个目录"
        
        # 获取目录基本信息
        stat_info = os.stat(dir_path)
        
        # 统计目录内容
        file_count = 0
        dir_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(dir_path):
            dir_count += len(dirs)
            file_count += len(files)
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
                except:
                    continue
        
        # 构建目录信息字典
        dir_info = {
            '目录名': os.path.basename(dir_path),
            '目录路径': os.path.abspath(dir_path),
            '创建时间': datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            '修改时间': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            '访问时间': datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            '目录权限': oct(stat_info.st_mode)[-3:],
            '文件数量': file_count,
            '子目录数量': dir_count,
            '总文件大小': f"{total_size} 字节 ({total_size / 1024:.2f} KB)"
        }
        
        # 尝试获取目录所有者信息（在Windows上可能不可用）
        if platform.system() != 'Windows':
            try:
                import pwd
                import grp
                dir_info['所有者'] = pwd.getpwuid(stat_info.st_uid).pw_name
                dir_info['所属组'] = grp.getgrgid(stat_info.st_gid).gr_name
            except:
                pass
        
        return dir_info, None
    
    except Exception as e:
        return None, f"获取目录信息时发生错误: {str(e)}"


def display_file_info(file_path):
    """
    显示文件或目录的信息
    
    Args:
        file_path: 文件或目录路径
    """
    # 判断是文件还是目录
    if os.path.isfile(file_path):
        info, error = get_file_info(file_path)
    else:
        info, error = get_directory_info(file_path)
    
    if error:
        print(error)
        return
    
    print("=" * 50)
    print(f"{'文件信息' if os.path.isfile(file_path) else '目录信息':^48}")
    print("=" * 50)
    
    for key, value in info.items():
        print(f"{key:<20}: {value}")
    
    print("=" * 50)


def main():
    """
    主函数
    """
    print("文件信息查看工具")
    print("=" * 30)
    
    while True:
        file_path = input("\n请输入文件或目录路径 (输入 'q' 退出): ")
        
        if file_path.lower() == 'q':
            print("\n感谢使用文件信息查看工具！")
            break
        
        # 处理相对路径
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)
        
        display_file_info(file_path)


if __name__ == '__main__':
    main()