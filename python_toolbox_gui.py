#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python工具箱GUI界面
提供图形化界面来管理和运行Python工具箱中的各种工具
"""

import sys
import os
import threading
import time
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(__file__))

# 导入PyQt5
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QLabel, QComboBox, QTextEdit, QPushButton, 
    QSplitter, QTabWidget, QLineEdit, QProgressBar, QStatusBar, 
    QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

# 导入工具箱功能
from python_toolbox.main import load_tools


class ToolRunnerThread(QThread):
    """
    工具运行线程
    """
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)
    progress_signal = pyqtSignal(int)
    
    def __init__(self, tool_module, args=None):
        super().__init__()
        self.tool_module = tool_module
        self.args = args or []
        self.running = False
    
    def run(self):
        """
        运行工具
        """
        self.running = True
        
        try:
            # 检查是否有main函数
            if hasattr(self.tool_module, 'main'):
                # 重定向标准输出
                import io
                import contextlib
                
                with io.StringIO() as buffer, contextlib.redirect_stdout(buffer):
                    # 运行工具的main函数
                    self.tool_module.main()
                    output = buffer.getvalue()
                    self.output_signal.emit(output)
            else:
                self.output_signal.emit("工具没有实现main函数")
                self.finished_signal.emit(False)
                return
        
        except Exception as e:
            self.output_signal.emit(f"工具运行错误: {str(e)}")
            self.finished_signal.emit(False)
        else:
            self.finished_signal.emit(True)
        finally:
            self.running = False
    
    def stop(self):
        """
        停止工具运行
        """
        self.running = False


class PythonToolboxGUI(QMainWindow):
    """
    Python工具箱GUI主界面
    """
    
    def __init__(self):
        super().__init__()
        self.tools = {}
        self.categories = {}
        self.current_tool = None
        self.tool_thread = None
        
        # 初始化界面
        self.init_ui()
        
        # 连接信号
        self.category_combo.currentIndexChanged.connect(self.display_tools)
        self.tool_list.currentItemChanged.connect(self.show_tool_info)
        self.search_input.textChanged.connect(self.filter_tools)
        self.run_button.clicked.connect(self.run_tool)
        self.stop_button.clicked.connect(self.stop_tool)
        
        # 加载工具
        self.load_toolbox()
    
    def init_ui(self):
        """
        初始化界面
        """
        self.setWindowTitle("Python工具箱")
        self.setGeometry(100, 100, 900, 600)
        
        # 设置字体
        font = QFont("Microsoft YaHei", 9)
        QApplication.setFont(font)
        
        # 中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧面板（工具列表）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMinimumWidth(250)
        
        # 分类选择
        category_label = QLabel("分类:")
        left_layout.addWidget(category_label)
        self.category_combo = QComboBox()
        self.category_combo.addItem("所有工具")
        left_layout.addWidget(self.category_combo)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索工具...")
        left_layout.addWidget(self.search_input)
        
        # 工具列表
        tool_list_label = QLabel("工具列表:")
        left_layout.addWidget(tool_list_label)
        self.tool_list = QListWidget()
        self.tool_list.setMinimumHeight(400)
        left_layout.addWidget(self.tool_list)
        
        # 右侧面板（工具信息和输出）
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 选项卡
        self.tab_widget = QTabWidget()
        
        # 工具信息选项卡
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        
        self.tool_name_label = QLabel("工具名称:")
        self.tool_name_label.setWordWrap(True)
        info_layout.addWidget(self.tool_name_label)
        
        self.tool_description_label = QLabel("工具描述:")
        self.tool_description_label.setWordWrap(True)
        info_layout.addWidget(self.tool_description_label)
        
        self.tool_info_text = QTextEdit()
        self.tool_info_text.setReadOnly(True)
        info_layout.addWidget(self.tool_info_text)
        
        self.tab_widget.addTab(info_tab, "工具信息")
        
        # 工具输出选项卡
        output_tab = QWidget()
        output_layout = QVBoxLayout(output_tab)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)
        
        self.tab_widget.addTab(output_tab, "工具输出")
        
        right_layout.addWidget(self.tab_widget)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        right_layout.addWidget(self.progress_bar)
        
        # 底部控制栏
        control_layout = QHBoxLayout()
        
        self.run_button = QPushButton("运行工具")
        self.run_button.setEnabled(False)
        control_layout.addWidget(self.run_button)
        
        self.stop_button = QPushButton("停止运行")
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.stop_button)
        
        control_layout.addStretch()
        
        right_layout.addLayout(control_layout)
        
        # 直接使用HBoxLayout，不使用分割器
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        main_layout.setStretch(0, 1)  # 左侧面板占1份
        main_layout.setStretch(1, 2)  # 右侧面板占2份
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("欢迎使用Python工具箱")
    
    def load_toolbox(self):
        """
        加载工具箱
        """
        try:
            self.status_bar.showMessage("正在加载工具...")
            self.output_text.append("正在加载工具...")
            
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
                        'full_description': getattr(module, '__doc__', '无描述'),
                        'has_main': hasattr(module, 'main')
                    }
                    
                    self.categories[category].append(tool_info)
                    self.tools[tool_path] = tool_info
            
            # 显示工具
            self.display_tools()
            
            self.status_bar.showMessage(f"工具加载完成: 成功 {len(self.tools)}, 失败 0")
            self.output_text.append(f"工具加载完成: 成功 {len(self.tools)}, 失败 0")
            
        except Exception as e:
            self.status_bar.showMessage(f"工具加载失败: {str(e)}")
            self.output_text.append(f"工具加载失败: {str(e)}")
    
    def display_tools(self):
        """
        显示工具
        """
        self.tool_list.clear()
        
        # 获取当前选择的分类
        current_category = self.category_combo.currentText()
        
        # 遍历所有工具
        for tool_path, tool_info in self.tools.items():
            if current_category == "所有工具" or tool_info['category'] == current_category:
                # 创建工具列表项
                item = QListWidgetItem(f"{tool_path} - {tool_info['description']}")
                item.setToolTip(tool_info['description'])
                self.tool_list.addItem(item)
        
        # 确保至少有一个项被选中
        if self.tool_list.count() > 0:
            self.tool_list.setCurrentRow(0)
    
    def filter_tools(self, search_text):
        """
        过滤工具
        """
        search_text = search_text.lower()
        
        # 获取当前选择的分类
        current_category = self.category_combo.currentText()
        
        # 遍历所有工具
        for i in range(self.tool_list.count()):
            item = self.tool_list.item(i)
            tool_path = item.text().split(" - ")[0]
            tool_info = self.tools.get(tool_path, {})
            
            # 检查是否匹配分类
            if current_category == "所有工具" or tool_info.get('category') == current_category:
                # 检查是否匹配搜索文本
                if search_text in tool_path.lower() or search_text in tool_info.get('description', '').lower():
                    item.setHidden(False)
                else:
                    item.setHidden(True)
            else:
                item.setHidden(True)
    
    def show_tool_info(self, current_item, previous_item):
        """
        显示工具信息
        """
        if not current_item:
            return
        
        # 获取工具路径
        tool_path = current_item.text().split(" - ")[0]
        tool_info = self.tools.get(tool_path, {})
        
        if not tool_info:
            return
        
        # 更新工具信息
        self.tool_name_label.setText(f"工具名称: {tool_path}")
        self.tool_description_label.setText(f"工具描述: {tool_info.get('description', '无描述')}")
        self.tool_info_text.setText(tool_info.get('full_description', '无描述'))
        
        # 更新当前工具
        self.current_tool = tool_info
        
        # 启用运行按钮
        self.run_button.setEnabled(True)
    
    def run_tool(self):
        """
        运行工具
        """
        if not self.current_tool:
            QMessageBox.warning(self, "警告", "请选择一个工具")
            return
        
        if not self.current_tool['has_main']:
            QMessageBox.warning(self, "警告", "该工具没有实现main函数")
            return
        
        # 清空输出
        self.output_text.clear()
        
        # 禁用按钮
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # 更新状态
        self.status_bar.showMessage(f"正在运行工具: {self.current_tool['name']}")
        self.output_text.append(f"正在运行工具: {self.current_tool['name']}")
        self.output_text.append(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.output_text.append("=" * 50)
        
        # 创建工具运行线程
        self.tool_thread = ToolRunnerThread(self.current_tool['module'])
        self.tool_thread.output_signal.connect(self.append_output)
        self.tool_thread.finished_signal.connect(self.tool_finished)
        self.tool_thread.start()
    
    def stop_tool(self):
        """
        停止运行工具
        """
        if self.tool_thread and self.tool_thread.running:
            self.tool_thread.stop()
            self.status_bar.showMessage("正在停止工具...")
    
    def append_output(self, output):
        """
        添加工具输出
        """
        self.output_text.append(output)
    
    def tool_finished(self, success):
        """
        工具运行完成
        """
        # 更新状态
        if success:
            self.status_bar.showMessage(f"工具运行完成: {self.current_tool['name']}")
            self.output_text.append("=" * 50)
            self.output_text.append(f"工具运行完成: {self.current_tool['name']}")
        else:
            self.status_bar.showMessage(f"工具运行失败: {self.current_tool['name']}")
            self.output_text.append("=" * 50)
            self.output_text.append(f"工具运行失败: {self.current_tool['name']}")
        
        # 启用按钮
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PythonToolboxGUI()
    window.show()
    sys.exit(app.exec_())