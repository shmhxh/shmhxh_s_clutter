#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python工具箱配置管理工具
用于管理工具箱的各种设置和配置选项
"""

import os
import platform
from python_toolbox.config import config as config_module
from python_toolbox.tools.system_tools.console_ui import (
    print_title, print_info, print_success, print_error, print_warning,
    print_table, pause, clear_screen
)

def show_config_menu():
    """显示配置菜单"""
    while True:
        clear_screen()
        print_title("Python工具箱配置管理")
        print("\n请选择要修改的配置选项：")
        print("1. 语言设置")
        print("2. 主题设置")
        print("3. 自动更新设置")
        print("4. 编辑器设置")
        print("5. 日志级别设置")
        print("6. 清除最近使用工具记录")
        print("7. 重置为默认配置")
        print("8. 查看当前配置")
        print("0. 返回主菜单")
        
        choice = input("\n请输入选择: ")
        
        if choice == '1':
            set_language()
        elif choice == '2':
            set_theme()
        elif choice == '3':
            set_auto_update()
        elif choice == '4':
            set_editor()
        elif choice == '5':
            set_log_level()
        elif choice == '6':
            clear_recent_tools()
        elif choice == '7':
            reset_to_default()
        elif choice == '8':
            show_current_config()
        elif choice == '0':
            break
        else:
            print_error("无效的选择，请重新输入")
            pause()

def set_language():
    """设置语言"""
    clear_screen()
    print_title("语言设置")
    
    current = config_module.get_config('language', 'zh_CN')
    print(f"当前语言设置: {current}")
    print("\n可用语言选项：")
    print("1. 中文 (zh_CN)")
    print("2. 英文 (en_US)")
    
    choice = input("\n请选择语言 (输入序号): ")
    
    if choice == '1':
        config_module.set_config('language', 'zh_CN')
        print_success("语言设置已更新为：中文 (zh_CN)")
    elif choice == '2':
        config_module.set_config('language', 'en_US')
        print_success("语言设置已更新为：英文 (en_US)")
    else:
        print_error("无效的选择，语言设置未更改")
    
    pause()

def set_theme():
    """设置主题"""
    clear_screen()
    print_title("主题设置")
    
    current = config_module.get_config('theme', 'default')
    print(f"当前主题: {current}")
    print("\n可用主题选项：")
    print("1. 默认主题 (default)")
    print("2. 暗黑主题 (dark)")
    print("3. 亮色主题 (light)")
    
    choice = input("\n请选择主题 (输入序号): ")
    
    themes = {'1': 'default', '2': 'dark', '3': 'light'}
    if choice in themes:
        config_module.set_config('theme', themes[choice])
        print_success(f"主题设置已更新为：{themes[choice]}")
    else:
        print_error("无效的选择，主题设置未更改")
    
    pause()

def set_auto_update():
    """设置自动更新"""
    clear_screen()
    print_title("自动更新设置")
    
    current = config_module.get_config('auto_update', True)
    print(f"当前自动更新设置: {'启用' if current else '禁用'}")
    
    choice = input("\n是否启用自动更新？(y/n): ").lower()
    
    if choice == 'y':
        config_module.set_config('auto_update', True)
        print_success("自动更新已启用")
    elif choice == 'n':
        config_module.set_config('auto_update', False)
        print_success("自动更新已禁用")
    else:
        print_error("无效的选择，设置未更改")
    
    pause()

def set_editor():
    """设置默认编辑器"""
    clear_screen()
    print_title("编辑器设置")
    
    current = config_module.get_config('editor', '')
    print(f"当前默认编辑器: {current}")
    
    new_editor = input("\n请输入新的默认编辑器路径或命令: ")
    if new_editor.strip():
        config_module.set_config('editor', new_editor)
        print_success(f"默认编辑器已更新为: {new_editor}")
    else:
        print_error("编辑器不能为空，设置未更改")
    
    pause()

def set_log_level():
    """设置日志级别"""
    clear_screen()
    print_title("日志级别设置")
    
    current = config_module.get_config('log_level', 'INFO')
    print(f"当前日志级别: {current}")
    print("\n可用日志级别：")
    print("1. DEBUG")
    print("2. INFO")
    print("3. WARNING")
    print("4. ERROR")
    
    levels = {'1': 'DEBUG', '2': 'INFO', '3': 'WARNING', '4': 'ERROR'}
    choice = input("\n请选择日志级别 (输入序号): ")
    
    if choice in levels:
        config_module.set_config('log_level', levels[choice])
        print_success(f"日志级别已更新为: {levels[choice]}")
    else:
        print_error("无效的选择，日志级别未更改")
    
    pause()

def clear_recent_tools():
    """清除最近使用的工具记录"""
    clear_screen()
    print_title("清除最近使用工具记录")
    
    recent_tools = config_module.get_recent_tools()
    if recent_tools:
        print("当前最近使用的工具：")
        for i, tool in enumerate(recent_tools, 1):
            print(f"  {i}. {tool}")
        
        confirm = input("\n确定要清除所有最近使用的工具记录吗？(y/n): ").lower()
        if confirm == 'y':
            config_module.set_config('recent_tools', [])
            print_success("最近使用的工具记录已清除")
        else:
            print_info("已取消操作")
    else:
        print_info("没有最近使用的工具记录")
    
    pause()

def reset_to_default():
    """重置为默认配置"""
    clear_screen()
    print_title("重置配置")
    
    print_warning("警告: 这将把所有配置重置为默认值！")
    print("\n当前配置将被清除，这是一个不可逆操作。")
    
    confirm = input("\n确定要重置所有配置吗？(yes/no): ").lower()
    if confirm == 'yes':
        config_module.reset_config()
        print_success("配置已重置为默认值")
    else:
        print_info("已取消操作")
    
    pause()

def show_current_config():
    """显示当前配置"""
    clear_screen()
    print_title("当前配置")
    
    config_data = config_module.load_config()
    
    # 准备表格数据
    config_table = []
    for key, value in config_data.items():
        config_table.append([key, str(value)])
    
    # 显示表格
    print_table(["配置项", "当前值"], config_table)
    print(f"\n配置文件位置: {config_module.CONFIG_FILE}")
    
    pause()

def main():
    """主函数"""
    try:
        show_config_menu()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print_error(f"发生错误: {str(e)}")
    finally:
        print_info("配置管理工具已退出")

if __name__ == '__main__':
    main()