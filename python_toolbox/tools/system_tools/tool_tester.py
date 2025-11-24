#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python工具箱测试工具
用于测试所有工具模块的加载和基本功能
"""

import os
import sys
import time
import importlib
import traceback
from python_toolbox.tools.system_tools.console_ui import (
    print_title, print_info, print_success, print_error, print_warning,
    print_table, pause, clear_screen, progress_bar
)
from python_toolbox.config import config

def test_all_tools():
    """测试所有工具模块"""
    clear_screen()
    print_title("Python工具箱测试工具")
    print_info("开始测试所有工具模块...\n")
    
    # 获取tools目录路径
    tools_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'tools')
    
    # 记录测试结果
    test_results = []
    total_tools = 0
    successful_tools = 0
    failed_tools = 0
    
    # 计算总工具数
    for category in os.listdir(tools_dir):
        category_path = os.path.join(tools_dir, category)
        if os.path.isdir(category_path) and not category.startswith('__'):
            for file_name in os.listdir(category_path):
                if file_name.endswith('.py') and not file_name.startswith('__') and file_name != 'tool_tester.py':
                    total_tools += 1
    
    current = 0
    print_info(f"发现 {total_tools} 个工具模块需要测试\n")
    
    # 开始测试
    start_time = time.time()
    
    # 遍历所有工具分类
    for category in os.listdir(tools_dir):
        category_path = os.path.join(tools_dir, category)
        if os.path.isdir(category_path) and not category.startswith('__'):
            print_info(f"测试分类: {category}")
            
            # 遍历分类下的工具
            for file_name in os.listdir(category_path):
                if file_name.endswith('.py') and not file_name.startswith('__') and file_name != 'tool_tester.py':
                    current += 1
                    tool_name = file_name[:-3]  # 去除.py后缀
                    module_path = f'python_toolbox.tools.{category}.{tool_name}'
                    
                    # 显示进度条
                    progress_bar(current, total_tools, prefix=f"测试进度:", suffix=f"{current}/{total_tools}")
                    
                    try:
                        # 测试加载时间
                        load_start = time.time()
                        module = importlib.import_module(module_path)
                        load_time = time.time() - load_start
                        
                        # 检查是否有main函数
                        has_main = hasattr(module, 'main')
                        
                        # 检查是否有__doc__字符串
                        has_doc = hasattr(module, '__doc__') and module.__doc__
                        
                        # 收集工具信息
                        tool_info = {
                            'category': category,
                            'name': tool_name,
                            'loaded': True,
                            'has_main': has_main,
                            'has_doc': has_doc,
                            'load_time': load_time,
                            'error': None
                        }
                        
                        test_results.append(tool_info)
                        successful_tools += 1
                        
                    except Exception as e:
                        # 记录错误信息
                        error_info = traceback.format_exc().split('\n')[-2]
                        tool_info = {
                            'category': category,
                            'name': tool_name,
                            'loaded': False,
                            'has_main': False,
                            'has_doc': False,
                            'load_time': 0,
                            'error': error_info
                        }
                        
                        test_results.append(tool_info)
                        failed_tools += 1
    
    total_time = time.time() - start_time
    print("\n" * 2)  # 清空进度条行
    
    # 显示测试结果摘要
    print_title("测试结果摘要")
    print(f"总工具数: {total_tools}")
    print(f"成功加载: {successful_tools}")
    print(f"加载失败: {failed_tools}")
    print(f"总测试时间: {total_time:.2f} 秒")
    
    if failed_tools > 0:
        print_error(f"警告: 有 {failed_tools} 个工具加载失败")
    else:
        print_success("所有工具加载成功！")
    
    # 显示详细结果
    show_detailed_results(test_results)
    
    # 显示性能分析
    show_performance_analysis(test_results)

def show_detailed_results(test_results):
    """显示详细测试结果"""
    print("\n")
    print_title("详细测试结果")
    
    # 按分类分组
    results_by_category = {}
    for result in test_results:
        category = result['category']
        if category not in results_by_category:
            results_by_category[category] = []
        results_by_category[category].append(result)
    
    # 显示每个分类的结果
    for category, results in results_by_category.items():
        print(f"\n{category}:")
        
        category_data = []
        for result in results:
            status = "✅ 成功" if result['loaded'] else f"❌ 失败: {result['error']}"
            main_status = "是" if result['has_main'] else "否"
            doc_status = "是" if result['has_doc'] else "否"
            
            category_data.append([
                result['name'],
                status,
                main_status,
                doc_status,
                f"{result['load_time']*1000:.2f} ms"
            ])
        
        print_table(["工具名称", "状态", "有main函数", "有文档", "加载时间"], category_data)

def show_performance_analysis(test_results):
    """显示性能分析"""
    print("\n")
    print_title("性能分析")
    
    # 计算平均加载时间
    loaded_tools = [r for r in test_results if r['loaded']]
    if loaded_tools:
        avg_load_time = sum(r['load_time'] for r in loaded_tools) / len(loaded_tools)
        print(f"平均加载时间: {avg_load_time*1000:.2f} ms")
        
        # 找出加载最慢的工具
        slowest_tool = max(loaded_tools, key=lambda x: x['load_time'])
        print(f"加载最慢的工具: {slowest_tool['category']}.{slowest_tool['name']} ({slowest_tool['load_time']*1000:.2f} ms)")
        
        # 找出加载最快的工具
        fastest_tool = min(loaded_tools, key=lambda x: x['load_time'])
        print(f"加载最快的工具: {fastest_tool['category']}.{fastest_tool['name']} ({fastest_tool['load_time']*1000:.2f} ms)")
        
        # 计算文档覆盖率
        doc_coverage = sum(r['has_doc'] for r in loaded_tools) / len(loaded_tools) * 100
        print(f"文档覆盖率: {doc_coverage:.1f}%")
        
        # 计算main函数覆盖率
        main_coverage = sum(r['has_main'] for r in loaded_tools) / len(loaded_tools) * 100
        print(f"main函数覆盖率: {main_coverage:.1f}%")

def check_dependencies():
    """检查工具箱依赖"""
    clear_screen()
    print_title("依赖检查")
    print_info("检查工具箱运行所需的依赖...\n")
    
    # 基础依赖列表
    dependencies = {
        'os': 'Python标准库',
        'sys': 'Python标准库',
        'json': 'Python标准库',
        'time': 'Python标准库',
        'datetime': 'Python标准库',
        'importlib': 'Python标准库',
        'platform': 'Python标准库',
        'traceback': 'Python标准库',
        'argparse': 'Python标准库',
        'PIL': 'Pillow (图像处理)',
        'requests': 'requests (网络请求)'
    }
    
    missing_deps = []
    
    for module, desc in dependencies.items():
        try:
            if module == 'PIL':
                import PIL
            else:
                __import__(module)
            print_success(f"✓ {module} - {desc}")
        except ImportError:
            missing_deps.append((module, desc))
            print_error(f"✗ {module} - {desc}")
    
    print("\n")
    if missing_deps:
        print_warning(f"发现 {len(missing_deps)} 个缺失的依赖:")
        for module, desc in missing_deps:
            print(f"  - {module}: {desc}")
            
        if 'PIL' in [m[0] for m in missing_deps]:
            print("\n安装Pillow的命令: pip install pillow")
        if 'requests' in [m[0] for m in missing_deps]:
            print("安装requests的命令: pip install requests")
    else:
        print_success("所有依赖都已安装！")

def show_system_info():
    """显示系统信息"""
    clear_screen()
    print_title("系统环境信息")
    
    import platform
    import sys
    
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {platform.python_version()}")
    print(f"Python解释器路径: {sys.executable}")
    print(f"工具箱配置目录: {config.USER_DATA_DIR}")
    print(f"工具箱安装目录: {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")
    print(f"当前工作目录: {os.getcwd()}")

def main():
    """主函数"""
    try:
        while True:
            clear_screen()
            print_title("Python工具箱测试工具")
            print("\n请选择测试选项：")
            print("1. 测试所有工具模块")
            print("2. 检查依赖")
            print("3. 显示系统信息")
            print("0. 返回")
            
            choice = input("\n请输入选择: ")
            
            if choice == '1':
                test_all_tools()
                pause()
            elif choice == '2':
                check_dependencies()
                pause()
            elif choice == '3':
                show_system_info()
                pause()
            elif choice == '0':
                break
            else:
                print_error("无效的选择，请重新输入")
                pause()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print_error(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print_info("测试工具已退出")

if __name__ == '__main__':
    main()