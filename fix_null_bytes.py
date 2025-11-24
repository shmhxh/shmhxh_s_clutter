#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Python文件中的null字节问题
"""

import os
import sys
import re


def fix_null_bytes(file_path):
    """
    修复文件中的null字节
    :param file_path: 文件路径
    :return: 是否修复成功
    """
    try:
        # 以二进制模式读取文件
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # 检查是否包含null字节
        if b'\x00' in content:
            print(f"修复文件: {file_path}")
            # 移除所有null字节
            content_fixed = content.replace(b'\x00', b'')
            
            # 保存修复后的文件
            with open(file_path, 'wb') as f:
                f.write(content_fixed)
            return True
        return False
    except Exception as e:
        print(f"修复文件失败 {file_path}: {e}")
        return False


def process_directory(directory):
    """
    处理目录中的所有Python文件
    :param directory: 目录路径
    """
    fixed_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                total_count += 1
                if fix_null_bytes(file_path):
                    fixed_count += 1
    
    print(f"\n处理完成: 共检查 {total_count} 个Python文件，修复了 {fixed_count} 个包含null字节的文件")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        # 默认处理当前目录
        target_dir = os.getcwd()
    
    print(f"开始修复目录: {target_dir}")
    process_directory(target_dir)