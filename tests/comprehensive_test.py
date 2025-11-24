#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合测试脚本 - 验证工具加载、显示和运行流程
"""

import sys
import os
import importlib

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

from python_toolbox.main import load_tools


def test_tool_loading():
    """测试工具加载功能"""
    print("=== 测试工具加载功能 ===")
    try:
        tools_dict = load_tools()
        print(f"[成功] 工具加载完成，共加载 {len(tools_dict)} 个分类")
        
        total_tools = 0
        for category, category_tools in tools_dict.items():
            print(f"  {category}: {len(category_tools)} 个工具")
            for tool_name, module in category_tools.items():
                total_tools += 1
                # 检查工具是否有main函数
                has_main = hasattr(module, 'main')
                description = getattr(module, '__doc__', '无描述').strip().split('\n')[0] if getattr(module, '__doc__', '') else '无描述'
                print(f"    - {tool_name}: {description} {'(有main函数)' if has_main else '(无main函数)'}")
        
        print(f"\n[总结] 共加载 {total_tools} 个工具")
        return True, tools_dict
    except Exception as e:
        print(f"[失败] 工具加载失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def test_tool_imports():
    """测试工具导入功能"""
    print("\n=== 测试工具导入功能 ===")
    try:
        # 测试导入console_ui模块
        from python_toolbox.tools.system_tools.console_ui import pause
        print("[成功] 从console_ui导入pause函数")
        
        # 测试导入特定工具
        from python_toolbox.tools.file_tools.file_info import main
        print("[成功] 从file_info导入main函数")
        
        return True
    except Exception as e:
        print(f"[失败] 工具导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_gui_imports():
    """测试GUI相关导入"""
    print("\n=== 测试GUI相关导入 ===")
    try:
        # 测试PyQt5导入
        from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
        print("[成功] PyQt5模块导入正常")
        
        return True
    except Exception as e:
        print(f"[失败] GUI相关导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Python工具箱综合测试")
    print("=" * 50)
    
    # 运行所有测试
    test_results = []
    
    test_results.append(test_tool_loading())
    test_results.append(test_tool_imports())
    test_results.append(test_gui_imports())
    
    # 汇总测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for i, result in enumerate(test_results):
        test_name = ["工具加载测试", "工具导入测试", "GUI导入测试"][i]
        if isinstance(result, tuple):
            if result[0]:
                passed += 1
                print(f"{test_name}: 通过")
            else:
                print(f"{test_name}: 失败")
        else:
            if result:
                passed += 1
                print(f"{test_name}: 通过")
            else:
                print(f"{test_name}: 失败")
    
    print(f"\n[总结] 通过: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有测试通过！工具箱可以正常使用。")
        print("\n使用说明:")
        print("1. 运行GUI程序: python python_toolbox_gui.py")
        print("2. 或运行极简版GUI: python simple_gui_fixed.py")
    else:
        print(f"\n❌ {total - passed} 个测试未通过，请检查错误信息。")