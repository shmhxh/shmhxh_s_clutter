#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统信息查看工具
用于获取和显示系统详细信息
"""

import os
import platform
import socket
import time
import psutil
from datetime import datetime


def get_system_basic_info():
    """
    获取系统基本信息
    
    Returns:
        dict: 包含系统基本信息的字典
    """
    info = {}
    
    # 系统信息
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()
    
    info['操作系统'] = f"{system} {release}"
    info['系统版本'] = version
    info['架构'] = machine
    info['处理器'] = processor
    
    # 主机名和IP
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "无法获取"
    
    info['主机名'] = hostname
    info['IP地址'] = ip_address
    
    # Python信息
    info['Python版本'] = platform.python_version()
    
    # 当前时间
    info['当前时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return info


def get_cpu_info():
    """
    获取CPU信息
    
    Returns:
        dict: 包含CPU信息的字典
    """
    info = {}
    
    # CPU核心数
    info['物理核心数'] = psutil.cpu_count(logical=False)
    info['逻辑核心数'] = psutil.cpu_count(logical=True)
    
    # CPU使用率（总体和每个核心）
    info['总体CPU使用率'] = f"{psutil.cpu_percent(interval=0.1)}%"
    info['每个核心CPU使用率'] = [f"{percent}%" for percent in psutil.cpu_percent(interval=0.1, percpu=True)]
    
    return info


def get_memory_info():
    """
    获取内存信息
    
    Returns:
        dict: 包含内存信息的字典
    """
    memory = psutil.virtual_memory()
    
    # 转换为GB
    total_gb = memory.total / (1024 ** 3)
    available_gb = memory.available / (1024 ** 3)
    used_gb = memory.used / (1024 ** 3)
    
    info = {
        '总内存': f"{total_gb:.2f} GB",
        '可用内存': f"{available_gb:.2f} GB",
        '已用内存': f"{used_gb:.2f} GB",
        '内存使用率': f"{memory.percent}%"
    }
    
    return info


def get_disk_info():
    """
    获取磁盘信息
    
    Returns:
        dict: 包含磁盘信息的字典
    """
    disks = []
    
    for partition in psutil.disk_partitions():
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            
            # 转换为GB
            total_gb = partition_usage.total / (1024 ** 3)
            used_gb = partition_usage.used / (1024 ** 3)
            free_gb = partition_usage.free / (1024 ** 3)
            
            disk_info = {
                '设备': partition.device,
                '挂载点': partition.mountpoint,
                '文件系统类型': partition.fstype,
                '总容量': f"{total_gb:.2f} GB",
                '已用容量': f"{used_gb:.2f} GB",
                '可用容量': f"{free_gb:.2f} GB",
                '使用率': f"{partition_usage.percent}%"
            }
            
            disks.append(disk_info)
        except (PermissionError, OSError):
            # 某些磁盘可能需要管理员权限才能访问
            continue
    
    return disks


def get_network_info():
    """
    获取网络信息
    
    Returns:
        dict: 包含网络信息的字典
    """
    net_io = psutil.net_io_counters()
    
    # 转换为MB
    bytes_sent_mb = net_io.bytes_sent / (1024 ** 2)
    bytes_recv_mb = net_io.bytes_recv / (1024 ** 2)
    
    info = {
        '发送字节数': f"{bytes_sent_mb:.2f} MB",
        '接收字节数': f"{bytes_recv_mb:.2f} MB",
        '发送数据包数': net_io.packets_sent,
        '接收数据包数': net_io.packets_recv,
        '发送错误数': net_io.errout,
        '接收错误数': net_io.errin,
        '丢弃的数据包数': net_io.dropout + net_io.dropin
    }
    
    return info


def get_process_info(top_n=10):
    """
    获取进程信息（CPU占用率最高的进程）
    
    Args:
        top_n: 返回的进程数量
    
    Returns:
        list: 包含进程信息的列表
    """
    processes = []
    
    # 获取所有进程
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'create_time']):
        try:
            proc_info = proc.info
            # 计算进程运行时间
            create_time = datetime.fromtimestamp(proc_info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
            
            process_info = {
                'PID': proc_info['pid'],
                '名称': proc_info['name'],
                '用户名': proc_info['username'] if proc_info['username'] else 'N/A',
                'CPU使用率': f"{proc_info['cpu_percent']}%",
                '内存使用率': f"{proc_info['memory_percent']:.2f}%",
                '创建时间': create_time
            }
            
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    # 按CPU使用率排序，返回前N个
    processes = sorted(processes, key=lambda x: float(x['CPU使用率'].replace('%', '')), reverse=True)
    
    return processes[:top_n]


def display_system_info():
    """
    显示完整的系统信息
    """
    # 导入console_ui用于美化输出
    try:
        from python_toolbox.tools.system_tools.console_ui import (
            print_color, print_table, print_separator
        )
        has_ui = True
    except ImportError:
        has_ui = False
    
    if has_ui:
        print_color("系统基本信息", "cyan", bold=True)
        print_separator()
    else:
        print("系统基本信息")
        print("-" * 50)
    
    # 显示基本信息
    basic_info = get_system_basic_info()
    if has_ui:
        for key, value in basic_info.items():
            print_color(f"{key}: ", "green", end="")
            print(value)
    else:
        for key, value in basic_info.items():
            print(f"{key}: {value}")
    
    print()
    
    # 显示CPU信息
    if has_ui:
        print_color("CPU信息", "cyan", bold=True)
        print_separator()
    else:
        print("CPU信息")
        print("-" * 50)
    
    cpu_info = get_cpu_info()
    if has_ui:
        for key, value in cpu_info.items():
            if key != "每个核心CPU使用率":
                print_color(f"{key}: ", "green", end="")
                print(value)
        # 显示每个核心的使用率
        print_color("每个核心CPU使用率: ", "green", end="")
        print(" ".join(cpu_info["每个核心CPU使用率"]))
    else:
        for key, value in cpu_info.items():
            if key != "每个核心CPU使用率":
                print(f"{key}: {value}")
        print(f"每个核心CPU使用率: {' '.join(cpu_info['每个核心CPU使用率'])}")
    
    print()
    
    # 显示内存信息
    if has_ui:
        print_color("内存信息", "cyan", bold=True)
        print_separator()
    else:
        print("内存信息")
        print("-" * 50)
    
    memory_info = get_memory_info()
    if has_ui:
        for key, value in memory_info.items():
            print_color(f"{key}: ", "green", end="")
            print(value)
    else:
        for key, value in memory_info.items():
            print(f"{key}: {value}")
    
    print()
    
    # 显示磁盘信息
    if has_ui:
        print_color("磁盘信息", "cyan", bold=True)
        print_separator()
    else:
        print("磁盘信息")
        print("-" * 50)
    
    disk_info = get_disk_info()
    if has_ui and disk_info:
        # 提取表头
        headers = list(disk_info[0].keys())
        # 提取数据
        data = [list(d.values()) for d in disk_info]
        print_table(data, headers)
    elif disk_info:
        for disk in disk_info:
            print(f"设备: {disk['设备']}")
            for key, value in disk.items():
                if key != '设备':
                    print(f"  {key}: {value}")
            print()
    else:
        print("无法获取磁盘信息")
    
    print()
    
    # 显示网络信息
    if has_ui:
        print_color("网络信息", "cyan", bold=True)
        print_separator()
    else:
        print("网络信息")
        print("-" * 50)
    
    network_info = get_network_info()
    if has_ui:
        for key, value in network_info.items():
            print_color(f"{key}: ", "green", end="")
            print(value)
    else:
        for key, value in network_info.items():
            print(f"{key}: {value}")
    
    print()
    
    # 显示进程信息
    if has_ui:
        print_color("CPU占用率最高的进程", "cyan", bold=True)
        print_separator()
    else:
        print("CPU占用率最高的进程")
        print("-" * 50)
    
    process_info = get_process_info()
    if has_ui and process_info:
        # 提取表头
        headers = list(process_info[0].keys())
        # 提取数据
        data = [list(p.values()) for p in process_info]
        print_table(data, headers)
    elif process_info:
        for process in process_info:
            print(f"PID: {process['PID']} | 名称: {process['名称']} | CPU使用率: {process['CPU使用率']} | 内存使用率: {process['内存使用率']}")
    else:
        print("无法获取进程信息")


def main():
    """
    主函数
    """
    try:
        display_system_info()
    except KeyboardInterrupt:
        print("\n程序已退出")
    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    main()