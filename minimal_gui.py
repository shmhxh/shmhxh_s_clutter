#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简版工具箱GUI
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(__file__))

# 导入PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QLabel, QComboBox
from PyQt5.QtCore import Qt

# 导入工具箱功能
from python_toolbox.main import load_tools


class MinimalToolboxGUI(QMainWindow):
    """
    极简版工具箱GUI
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
        self.setWindowTitle("极简工具箱")
        self.setGeometry(100, 100, 600, 400)
        
        # 中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 分类选择
        self.category_combo = QComboBox()
        self.category_combo.addItem("所有工具")
        self.category_combo.currentIndexChanged.connect(self.on_category_changed)
        main_layout.addWidget(self.category_combo)
        
        # 工具列表
        self.tool_list = QListWidget()
        main_layout.addWidget(self.tool_list)
    
    def load_tools(self):
        """
        加载工具
        """
        print("加载工具...")
        tools_dict = load_tools()
        
        # 组织工具
        for category, category_tools in tools_dict.items():
            print(f"分类: {category}, 工具数量: {len(category_tools)}")
            
            # 添加分类到下拉框
            self.category_combo.addItem(category)
            
            for tool_name, module in category_tools.items():
                tool_path = f"{category}.{tool_name}"
                description = getattr(module, '__doc__', '无描述').strip().split('\n')[0] if getattr(module, '__doc__', '') else '无描述'
                item_text = f"{tool_path} - {description}"
                
                # 添加到工具列表
                self.tool_list.addItem(item_text)
                print(f"  - {item_text}")
        
        print(f"加载完成，共 {self.tool_list.count()} 个工具")
    
    def on_category_changed(self, index):
        """
        分类选择变化时的处理
        """
        category = self.category_combo.currentText()
        print(f"选择分类: {category}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinimalToolboxGUI()
    window.show()
    sys.exit(app.exec_())