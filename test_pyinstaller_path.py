#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PyInstaller打包后的路径处理
模拟PyInstaller打包后的环境，测试load_tools()函数是否能正确加载工具
"""

import sys
import os

# 模拟PyInstaller的_MEIPASS环境变量
# 这个环境变量在PyInstaller打包后会指向临时目录
def test_with_meipass():
    print("测试PyInstaller打包后的环境...")
    
    # 保存原始的sys._MEIPASS（如果存在）
    original_meipass = getattr(sys, '_MEIPASS', None)
    
    try:
        # 设置_MEIPASS为当前项目根目录
        sys._MEIPASS = os.path.dirname(os.path.abspath(__file__))
        
        print(f"设置sys._MEIPASS为: {sys._MEIPASS}")
        
        # 导入load_tools函数
        from python_toolbox.main import load_tools
        
        # 测试加载工具
        tools = load_tools()
        
        print(f"成功加载 {len(tools)} 个工具分类:")
        for category, category_tools in tools.items():
            print(f"- {category}: {len(category_tools)} 个工具")
            for tool_name in category_tools.keys():
                print(f"  * {tool_name}")
        
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 恢复原始的_MEIPASS
        if original_meipass is not None:
            sys._MEIPASS = original_meipass
        elif hasattr(sys, '_MEIPASS'):
            del sys._MEIPASS

# 测试正常开发环境
def test_without_meipass():
    print("\n测试正常开发环境...")
    
    # 确保没有_MEIPASS
    if hasattr(sys, '_MEIPASS'):
        del sys._MEIPASS
    
    try:
        # 导入load_tools函数
        from python_toolbox.main import load_tools
        
        # 测试加载工具
        tools = load_tools()
        
        print(f"成功加载 {len(tools)} 个工具分类:")
        for category, category_tools in tools.items():
            print(f"- {category}: {len(category_tools)} 个工具")
            for tool_name in category_tools.keys():
                print(f"  * {tool_name}")
        
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("PyInstaller路径处理测试")
    print("=" * 40)
    
    meipass_result = test_with_meipass()
    print(f"\nPyInstaller环境测试结果: {'通过' if meipass_result else '失败'}")
    
    normal_result = test_without_meipass()
    print(f"正常环境测试结果: {'通过' if normal_result else '失败'}")
    
    if meipass_result and normal_result:
        print("\n所有测试通过! 路径处理修改有效。")
        sys.exit(0)
    else:
        print("\n测试失败! 请检查路径处理代码。")
        sys.exit(1)