#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的GUI测试程序
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QListWidget, QComboBox, QLabel, QTextEdit)
from PyQt5.QtCore import Qt

# 添加项目根目录到路径
sys.path.append(os.path.dirname(__file__))

# 导入工具箱功能
from python_toolbox.main import load_tools


class SimpleToolboxGUI(QMainWindow):
    """
    简化的工具箱GUI
    """
    
    def __init__(self):
        super().__init__()
        self.tools = {}
        self.categories = {}
        self.init_ui()
        self.load_tools()
    
    def init_ui(self):
        """
        初始化界面
        """
        self.setWindowTitle("简化的Python工具箱")
        self.setGeometry(100, 100, 800, 600)
        
        # 中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel("Python工具箱")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # 分类选择
        category_layout = QHBoxLayout()
        category_label = QLabel("分类:")
        self.category_combo = QComboBox()
        self.category_combo.currentIndexChanged.connect(self.on_category_changed)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        main_layout.addLayout(category_layout)
        
        # 工具列表
        tool_layout = QHBoxLayout()
        tool_label = QLabel("工具:")
        self.tool_list = QListWidget()
        self.tool_list.currentItemChanged.connect(self.on_tool_selected)
        tool_layout.addWidget(tool_label)
        tool_layout.addWidget(self.tool_list)
        main_layout.addLayout(tool_layout)
        
        # 工具信息
        info_label = QLabel("工具信息:")
        main_layout.addWidget(info_label)
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        main_layout.addWidget(self.info_text)
    
    def load_tools(self):
        """
        加载工具
        """
        print("开始加载工具...")
        tools_dict = load_tools()
        
        # 组织工具
        for category, category_tools in tools_dict.items():
            print(f"加载分类: {category}")
            self.categories[category] = []
            
            for tool_name, module in category_tools.items():
                tool_path = f"{category}.{tool_name}"
                tool_info = {
                    'module': module,
                    'name': tool_name,
                    'category': category,
                    'description': getattr(module, '__doc__', '无描述').strip().split('\n')[0] if getattr(module, '__doc__', '') else '无描述',
                    'has_main': hasattr(module, 'main')
                }
                
                self.categories[category].append(tool_info)
                self.tools[tool_path] = tool_info
                print(f"  - {tool_path}")
        
        # 添加分类到下拉框
        self.category_combo.addItem("所有工具")
        for category in sorted(self.categories.keys()):
            self.category_combo.addItem(category)
        
        # 显示所有工具
        self.show_tools("所有工具")
        print(f"加载完成，共 {len(self.tools)} 个工具")
    
    def show_tools(self, category):
        """
        显示指定分类的工具
        """
        self.tool_list.clear()
        
        if category == "所有工具":
            # 显示所有工具
            for tool_path, tool_info in self.tools.items():
                self.tool_list.addItem(f"{tool_path} - {tool_info['description']}")
        else:
            # 显示指定分类的工具
            if category in self.categories:
                for tool_info in self.categories[category]:
                    tool_path = f"{category}.{tool_info['name']}"
                    self.tool_list.addItem(f"{tool_info['name']} - {tool_info['description']}")
    
    def on_category_changed(self, index):
        """
        分类选择变化时的处理
        """
        category = self.category_combo.itemText(index)
        self.show_tools(category)
    
    def on_tool_selected(self, current, previous):
        """
        工具选择变化时的处理
        """
        if current:
            tool_text = current.text()
            self.info_text.setText(f"选中的工具: {tool_text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleToolboxGUI()
    window.show()
    sys.exit(app.exec_())