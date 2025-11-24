#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python工具箱 - 集多种实用工具于一体的工具集合
"""

import os
import sys
import argparse
from importlib import import_module

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 使用绝对导入
from python_toolbox.config import config
from python_toolbox.tools.system_tools.console_ui import (
    print_title, print_info, print_success, print_error, print_warning,
    print_divider, print_table, pause, progress_bar
)


def load_tools():
    """加载所有工具模块，包括系统信息和图像转换工具"""
    # 处理PyInstaller打包后的路径问题
    if hasattr(sys, '_MEIPASS'):
        # 打包后运行时使用临时目录
        base_path = sys._MEIPASS
        tools_dir = os.path.join(base_path, 'python_toolbox', 'tools')
    else:
        # 开发环境下的正常路径
        tools_dir = os.path.join(os.path.dirname(__file__), 'tools')
    
    tools = {}
    total_files = 0
    loaded_files = 0
    failed_files = 0
    
    # 首先计算总文件数
    for tool_category in os.listdir(tools_dir):
        category_path = os.path.join(tools_dir, tool_category)
        if os.path.isdir(category_path) and not tool_category.startswith('__'):
            for file_name in os.listdir(category_path):
                if file_name.endswith('.py') and not file_name.startswith('__'):
                    total_files += 1
    
    current = 0
    print_info("正在加载工具模块...")
    
    # 遍历tools目录下的所有工具包
    for tool_category in os.listdir(tools_dir):
        category_path = os.path.join(tools_dir, tool_category)
        if os.path.isdir(category_path) and not tool_category.startswith('__'):
            tools[tool_category] = {}
            
            # 遍历每个工具包下的Python文件
            for file_name in os.listdir(category_path):
                if file_name.endswith('.py') and not file_name.startswith('__'):
                    current += 1
                    progress_bar(current, total_files, prefix=f"处理中 ({current}/{total_files}):", suffix="")
                    
                    tool_name = file_name[:-3]  # 去除.py后缀
                    module_path = f'python_toolbox.tools.{tool_category}.{tool_name}'
                    try:
                        module = import_module(module_path)
                        tools[tool_category][tool_name] = module
                        loaded_files += 1
                    except Exception as e:
                        failed_files += 1
                        print_error(f"\n加载工具 {tool_category}.{tool_name} 失败: {str(e)}")
    
    print()  # 进度条后的换行
    print_success(f"工具加载完成: 成功 {loaded_files}, 失败 {failed_files}")
    return tools


def show_menu(tools):
    """显示主菜单"""
    print_divider('=', 60)
    print_title("欢迎使用 Python工具箱".center(58))
    print_divider('=', 60)
    print("1. 浏览所有工具")
    print("2. 搜索工具")
    print("3. 查看使用帮助")
    print("4. 查看最近使用的工具")
    print("5. 配置管理")
    print("6. 数据共享管理器")
    print("7. 工具箱测试")
    print("0. 退出")
    print_divider('=', 60)


def browse_tools(tools):
    """浏览所有工具"""
    print_title("\n可用工具分类:")
    
    categories = list(tools.keys())
    
    # 创建分类数据用于表格显示
    category_data = []
    for i, category in enumerate(categories, 1):
        tool_count = len(tools[category])
        category_data.append([str(i), category, str(tool_count)])
    
    # 显示分类表格
    print_table(["序号", "分类名称", "工具数量"], category_data)
    
    choice = input("\n请选择工具分类 (输入序号或0返回): ")
    if choice == '0':
        return
    
    try:
        category_index = int(choice) - 1
        if 0 <= category_index < len(categories):
            category = categories[category_index]
            category_tools = tools[category]
            
            print_title(f"\n{category} 分类下的工具:")
            
            # 创建工具数据用于表格显示
            tool_data = []
            tool_names = list(category_tools.keys())
            for i, tool_name in enumerate(tool_names, 1):
                tool_module = category_tools[tool_name]
                # 获取工具描述
                description = getattr(tool_module, '__doc__', '无描述').strip().split('\n')[0] if tool_module.__doc__ else '无描述'
                if len(description) > 50:
                    description = description[:47] + "..."
                tool_data.append([str(i), tool_name, description])
            
            # 显示工具表格
            print_table(["序号", "工具名称", "描述"], tool_data)
            
            tool_choice = input("\n请选择要使用的工具 (输入序号或0返回): ")
            if tool_choice != '0':
                try:
                    tool_index = int(tool_choice) - 1
                    if 0 <= tool_index < len(tool_names):
                        tool_name = tool_names[tool_index]
                        tool_module = category_tools[tool_name]
                        print_success(f"\n正在启动工具: {tool_name}")
                        
                        # 添加到最近使用的工具
                        from python_toolbox.config.config import add_recent_tool
                        add_recent_tool(f"{category}.{tool_name}")
                        
                        # 调用工具的main函数
                        if hasattr(tool_module, 'main'):
                            pause("按回车键继续...\n")
                            tool_module.main()
                        else:
                            print_warning(f"警告: 工具 {tool_name} 没有实现main函数")
                except ValueError:
                    print_error("无效的输入")
    except ValueError:
        print_error("无效的输入")


def search_tools(tools):
    """搜索工具"""
    keyword = input("\n请输入搜索关键词: ")
    results = []
    
    for category, category_tools in tools.items():
        for tool_name, tool_module in category_tools.items():
            # 搜索工具名称、分类名称和描述
            description = getattr(tool_module, '__doc__', '').strip()
            if (keyword.lower() in tool_name.lower() or 
                keyword.lower() in category.lower() or
                keyword.lower() in description.lower()):
                # 获取工具的简短描述
                short_desc = description.split('\n')[0] if description else '无描述'
                if len(short_desc) > 50:
                    short_desc = short_desc[:47] + "..."
                results.append((category, tool_name, short_desc))
    
    if results:
        print_success(f"\n找到 {len(results)} 个匹配的工具:")
        
        # 创建搜索结果数据用于表格显示
        result_data = []
        for i, (category, tool_name, description) in enumerate(results, 1):
            result_data.append([str(i), f"{category}.{tool_name}", description])
        
        # 显示搜索结果表格
        print_table(["序号", "工具路径", "描述"], result_data)
        
        choice = input("\n请选择要使用的工具 (输入序号或0返回): ")
        if choice != '0':
            try:
                index = int(choice) - 1
                if 0 <= index < len(results):
                    category, tool_name, _ = results[index]
                    tool_module = tools[category][tool_name]
                    print_success(f"\n正在启动工具: {tool_name}")
                    
                    # 添加到最近使用的工具
                    from python_toolbox.config.config import add_recent_tool
                    add_recent_tool(f"{category}.{tool_name}")
                    
                    if hasattr(tool_module, 'main'):
                        pause("按回车键继续...\n")
                        tool_module.main()
                    else:
                        print_warning(f"警告: 工具 {tool_name} 没有实现main函数")
            except ValueError:
                print_error("无效的输入")
    else:
        print_info("\n未找到匹配的工具")


def show_help():
    """显示使用帮助"""
    print_title("\nPython工具箱使用说明")
    print_divider()
    print("1. 本工具箱集成了多种实用工具，包括文件操作、文本处理、网络工具等。")
    print("2. 在主菜单中选择相应的功能进行操作。")
    print("3. 可以通过浏览或搜索的方式找到需要的工具。")
    print("4. 每个工具都有独立的使用说明。")
    print("5. 工具箱会自动记录您最近使用的工具。")
    print("6. 可以通过命令行参数直接运行特定工具。")
    print()
    print("命令行用法:")
    print("  python main.py --list      # 列出所有可用工具")
    print("  python main.py --tool category.tool_name  # 直接运行指定工具")
    print_divider()
    pause("按回车键继续...")

def show_recent_tools(tools):
    """显示最近使用的工具"""
    from python_toolbox.config.config import get_recent_tools
    recent_tools = get_recent_tools()
    
    if recent_tools:
        print_title("\n最近使用的工具")
        
        # 创建最近工具数据用于表格显示
        recent_data = []
        valid_recent_tools = []
        
        for i, tool_path in enumerate(recent_tools, 1):
            try:
                category, tool_name = tool_path.split('.')
                if category in tools and tool_name in tools[category]:
                    tool_module = tools[category][tool_name]
                    description = getattr(tool_module, '__doc__', '无描述').strip().split('\n')[0] if tool_module.__doc__ else '无描述'
                    if len(description) > 50:
                        description = description[:47] + "..."
                    recent_data.append([str(i), tool_path, description])
                    valid_recent_tools.append((category, tool_name))
            except:
                continue
        
        if recent_data:
            print_table(["序号", "工具路径", "描述"], recent_data)
            
            choice = input("\n请选择要使用的工具 (输入序号或0返回): ")
            if choice != '0':
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(valid_recent_tools):
                        category, tool_name = valid_recent_tools[index]
                        tool_module = tools[category][tool_name]
                        print_success(f"\n正在启动工具: {tool_name}")
                        
                        # 更新最近使用记录
                        from python_toolbox.config.config import add_recent_tool
                        add_recent_tool(f"{category}.{tool_name}")
                        
                        if hasattr(tool_module, 'main'):
                            pause("按回车键继续...\n")
                            tool_module.main()
                        else:
                            print_warning(f"警告: 工具 {tool_name} 没有实现main函数")
                except ValueError:
                    print_error("无效的输入")
        else:
            print_info("\n没有有效的最近使用记录")
    else:
        print_info("\n您还没有使用过任何工具")
    
    pause("按回车键继续...")


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Python工具箱 - 集多种实用工具于一体')
    parser.add_argument('--list', action='store_true', help='列出所有可用工具')
    parser.add_argument('--tool', type=str, help='直接运行指定的工具 (格式: category.tool_name)，包括system_tools.system_info和image_tools.image_converter在内的所有工具')
    args = parser.parse_args()
    
    # 打印启动信息
    print_title("Python工具箱 v1.0.0")
    print_info(f"正在加载配置文件")
    print_info("工具箱准备就绪")
    
    # 加载所有工具
    tools = load_tools()
    
    # 命令行模式
    if args.list:
        print_title("\n所有可用工具:")
        for category, category_tools in tools.items():
            print(f"\n{category}:")
            for tool_name in category_tools.keys():
                tool_module = category_tools[tool_name]
                description = getattr(tool_module, '__doc__', '').strip().split('\n')[0] if tool_module.__doc__ else ''
                print(f"  - {tool_name}: {description}")
        return
    
    if args.tool:
        try:
            category, tool_name = args.tool.split('.')
            if category in tools and tool_name in tools[category]:
                tool_module = tools[category][tool_name]
                print_success(f"\n正在启动工具: {args.tool}")
                
                # 添加到最近使用的工具
                from python_toolbox.config.config import add_recent_tool
                add_recent_tool(args.tool)
                
                if hasattr(tool_module, 'main'):
                    tool_module.main()
                else:
                    print_error(f"错误: 工具 {args.tool} 没有实现main函数")
            else:
                print_error(f"错误: 找不到工具 {args.tool}")
        except ValueError:
            print_error("错误: 工具格式错误，请使用 category.tool_name 格式")
        return
    
    # 交互式模式
    while True:
        show_menu(tools)
        choice = input("请选择功能: ")
        
        if choice == '1':
            browse_tools(tools)
        elif choice == '2':
            search_tools(tools)
        elif choice == '3':
            show_help()
        elif choice == '4':
            show_recent_tools(tools)
        elif choice == '5':
            # 导入并运行配置管理工具
            try:
                from python_toolbox.tools.system_tools.config_manager import main as config_manager_main
                config_manager_main()
            except ImportError:
                print_error("配置管理工具未找到")
            except Exception as e:
                print_error(f"配置管理工具运行错误: {str(e)}")
        elif choice == '6':
            # 导入并运行数据共享管理器
            try:
                from python_toolbox.tools.system_tools.data_sharer import main as data_sharer_main
                data_sharer_main()
            except ImportError:
                print_error("数据共享管理器未找到")
            except Exception as e:
                print_error(f"数据共享管理器运行错误: {str(e)}")
        elif choice == '7':
            # 导入并运行工具箱测试工具
            try:
                from python_toolbox.tools.system_tools.tool_tester import main as tool_tester_main
                tool_tester_main()
            except ImportError:
                print_error("工具箱测试工具未找到")
            except Exception as e:
                print_error(f"工具箱测试工具运行错误: {str(e)}")
        elif choice == '0':
            print_success("\n感谢使用Python工具箱，再见！")
            break
        else:
            print_error("无效的选择，请重新输入")
        
        pause("\n按回车键继续...")


if __name__ == '__main__':
    main()