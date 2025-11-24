#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
极简版Python工具箱GUI
确保工具能够正常显示
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QLabel, QComboBox, QTextEdit, QPushButton, 
    QSplitter, QTabWidget, QLineEdit, QStatusBar, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入load_tools函数
from python_toolbox.main import load_tools

class SimpleToolboxGUI(QMainWindow):
    """极简版工具箱GUI"""
    
    def __init__(self):
        super().__init__()
        self.tools = {}
        self.categories = {}
        
        # 初始化界面
        self.init_ui()
        
        # 加载工具
        self.load_tools()
        
        # 显示工具
        self.display_tools()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("极简Python工具箱")
        self.setGeometry(100, 100, 800, 600)
        
        # 中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # 分类选择
        category_label = QLabel("分类:")
        left_layout.addWidget(category_label)
        self.category_combo = QComboBox()
        self.category_combo.addItem("所有工具")
        self.category_combo.currentIndexChanged.connect(self.display_tools)
        left_layout.addWidget(self.category_combo)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索工具...")
        self.search_input.textChanged.connect(self.filter_tools)
        left_layout.addWidget(self.search_input)
        
        # 工具列表
        tool_list_label = QLabel("工具列表:")
        left_layout.addWidget(tool_list_label)
        self.tool_list = QListWidget()
        left_layout.addWidget(self.tool_list)
        
        # 右侧面板
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 工具信息
        info_label = QLabel("工具信息:")
        right_layout.addWidget(info_label)
        self.tool_info = QTextEdit()
        self.tool_info.setReadOnly(True)
        right_layout.addWidget(self.tool_info)
        
        # 底部按钮
        run_button = QPushButton("运行工具")
        right_layout.addWidget(run_button)
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 使用分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 500])
        
        main_layout.addWidget(splitter)
    
    def load_tools(self):
        """加载工具"""
        try:
            self.status_bar.showMessage("正在加载工具...")
            
            # 加载工具
            tools_dict = load_tools()
            
            # 组织工具
            for category, category_tools in tools_dict.items():
                # 添加分类到下拉框
                if category not in [self.category_combo.itemText(i) for i in range(self.category_combo.count())]:
                    self.category_combo.addItem(category)
                
                # 组织工具到分类
                if category not in self.categories:
                    self.categories[category] = []
                
                for tool_name, module in category_tools.items():
                    tool_path = f"{category}.{tool_name}"
                    description = getattr(module, '__doc__', '无描述').strip().split('\n')[0] if getattr(module, '__doc__', '') else '无描述'
                    
                    tool_info = {
                        'module': module,
                        'name': tool_name,
                        'category': category,
                        'description': description,
                        'full_description': getattr(module, '__doc__', '无描述')
                    }
                    
                    self.categories[category].append(tool_info)
                    self.tools[tool_path] = tool_info
            
            self.status_bar.showMessage(f"工具加载完成: {len(self.tools)} 个工具")
            
        except Exception as e:
            self.status_bar.showMessage(f"工具加载失败: {str(e)}")
    
    def display_tools(self):
        """显示工具"""
        self.tool_list.clear()
        
        # 获取当前选择的分类
        current_category = self.category_combo.currentText()
        
        # 遍历所有工具
        for tool_path, tool_info in self.tools.items():
            if current_category == "所有工具" or tool_info['category'] == current_category:
                # 创建工具列表项
                item = QListWidgetItem(f"{tool_path} - {tool_info['description']}")
                self.tool_list.addItem(item)
    
    def filter_tools(self, search_text):
        """过滤工具"""
        search_text = search_text.lower()
        
        # 获取当前选择的分类
        current_category = self.category_combo.currentText()
        
        # 遍历所有工具
        for i in range(self.tool_list.count()):
            item = self.tool_list.item(i)
            tool_path = item.text().split(" - ")[0]
            tool_info = self.tools.get(tool_path, {})
            
            # 检查是否匹配分类
            if current_category != "所有工具" and tool_info.get('category') != current_category:
                item.setHidden(True)
                continue
            
            # 检查是否匹配搜索文本
            if search_text and search_text not in item.text().lower():
                item.setHidden(True)
            else:
                item.setHidden(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleToolboxGUI()
    window.show()
    sys.exit(app.exec_())