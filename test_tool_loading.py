#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试工具加载功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(__file__))

# 导入工具箱功能
from python_toolbox.main import load_tools

# 加载工具
tools_dict = load_tools()

# 打印工具结构
print("\n工具加载完成，结构如下:")
print("=" * 50)

for category, category_tools in tools_dict.items():
    print(f"\n分类: {category}")
    print(f"工具数量: {len(category_tools)}")
    print("-" * 30)
    
    for tool_name, module in category_tools.items():
        print(f"  工具: {tool_name}")
        print(f"  模块: {module}")
        print(f"  文档: {getattr(module, '__doc__', '无文档')}")
        print(f"  是否有main函数: {hasattr(module, 'main')}")
        print("  " + "-" * 25)

print("\n" + "=" * 50)
print(f"总工具数量: {sum(len(tools) for tools in tools_dict.values())}")