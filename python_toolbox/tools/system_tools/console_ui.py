#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化版控制台UI工具
"""

import sys

# 简单的打印函数，不使用颜色
def print_title(text, **kwargs):
    print("=" * 50)
    print(text)
    print("=" * 50)

def print_info(text, **kwargs):
    print(f"[信息] {text}")

def print_success(text, **kwargs):
    print(f"[成功] {text}")

def print_error(text, **kwargs):
    print(f"[错误] {text}")

def print_warning(text, **kwargs):
    print(f"[警告] {text}")

def print_divider(char='=', length=50, **kwargs):
    print(char * length)

def print_table(headers, rows, **kwargs):
    # 简单表格实现
    max_lens = []
    for i in range(len(headers)):
        max_len = len(headers[i])
        for row in rows:
            if i < len(row):
                max_len = max(max_len, len(str(row[i])))
        max_lens.append(max_len)
    
    # 打印表头
    header_line = " | ".join(h.ljust(max_lens[i]) for i, h in enumerate(headers))
    print("-" * (len(header_line) + 4))
    print(f"| {header_line} |")
    print("-" * (len(header_line) + 4))
    
    # 打印数据
    for row in rows:
        row_line = " | ".join(str(row[i]).ljust(max_lens[i]) for i in range(len(row)))
        print(f"| {row_line} |")
    
    print("-" * (len(header_line) + 4))

def main(message="按回车键继续..."):
    """
    暂停程序执行，等待用户输入
    """
    input(message)

# 添加pause别名，保持向后兼容
pause = main

def clear_screen():
    """
    清除屏幕
    """
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def progress_bar(current, total, width=50, prefix='', suffix='', **kwargs):
    percent = 100 * (current / float(total))
    filled_length = int(width * current // total)
    bar = '█' * filled_length + '-' * (width - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent:.1f}% {suffix}')
    sys.stdout.flush()
    if current >= total:
        print()

if __name__ == '__main__':
    print_title("测试")
    print_info("信息")
    print_success("成功")
    print_error("错误")
    print_warning("警告")
    main()