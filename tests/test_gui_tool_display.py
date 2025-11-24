#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试GUI工具加载和显示流程
"""

import sys
import os
from importlib import import_module

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入load_tools函数
try:
    from python_toolbox.main import load_tools
    print("✓ 成功导入load_tools函数")
except Exception as e:
    print(f"✗ 导入load_tools函数失败: {e}")
    sys.exit(1)

# 加载工具
print("\n=== 加载工具 ===")
tools = load_tools()

# 验证工具加载结果
print("\n=== 工具加载结果验证 ===")
print(f"工具分类数量: {len(tools)}")
print(f"工具分类: {list(tools.keys())}")

# 统计总工具数量
total_tools = 0
for category, category_tools in tools.items():
    category_tool_count = len(category_tools)
    total_tools += category_tool_count
    print(f"  {category}: {category_tool_count} 个工具")
    for tool_name, module in category_tools.items():
        # 检查工具模块的基本属性
        has_doc = hasattr(module, '__doc__') and module.__doc__
        has_main = hasattr(module, 'main') and callable(module.main)
        
        doc_summary = module.__doc__.strip().split('\n')[0] if has_doc else '无文档'
        print(f"    - {tool_name}: {doc_summary} {'(有main函数)' if has_main else '(无main函数)'}")

print(f"\n总工具数量: {total_tools}")

# 模拟GUI界面的工具显示
print("\n=== 模拟GUI工具显示 ===")
print("1. 分类下拉框内容:")
for i, category in enumerate(tools.keys(), 1):
    print(f"   {i}. {category}")

print("\n2. 工具列表内容:")
for category, category_tools in tools.items():
    print(f"   {category} 分类下的工具:")
    for tool_name, module in category_tools.items():
        doc_summary = module.__doc__.strip().split('\n')[0] if hasattr(module, '__doc__') and module.__doc__ else '无文档'
        print(f"     - {tool_name} - {doc_summary}")

print("\n✅ 工具加载和显示流程测试完成")
print("如果GUI界面正常，您应该能在下拉框看到所有分类，并在工具列表看到所有工具。")