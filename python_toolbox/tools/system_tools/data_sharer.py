#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python工具箱数据共享管理器
用于在不同工具之间共享数据，增强工具间的交互功能
"""

import json
import os
from datetime import datetime
from python_toolbox.config import config
from python_toolbox.tools.system_tools.console_ui import (
    print_title, print_info, print_success, print_error, print_warning,
    print_table, pause, clear_screen
)

# 数据共享存储路径
SHARED_DATA_FILE = os.path.join(config.USER_DATA_DIR, 'shared_data.json')

# 数据共享存储
_shared_data = {}
# 数据历史记录
_data_history = {}

class DataSharer:
    """数据共享管理器类"""
    
    def __init__(self):
        self._load_shared_data()
    
    def _load_shared_data(self):
        """加载共享数据"""
        global _shared_data, _data_history
        
        if os.path.exists(SHARED_DATA_FILE):
            try:
                with open(SHARED_DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    _shared_data = data.get('shared_data', {})
                    _data_history = data.get('data_history', {})
            except Exception as e:
                print_warning(f"加载共享数据失败: {str(e)}")
                _shared_data = {}
                _data_history = {}
    
    def _save_shared_data(self):
        """保存共享数据"""
        try:
            data = {
                'shared_data': _shared_data,
                'data_history': _data_history,
                'last_updated': datetime.now().isoformat()
            }
            
            # 确保目录存在
            os.makedirs(os.path.dirname(SHARED_DATA_FILE), exist_ok=True)
            
            with open(SHARED_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            print_error(f"保存共享数据失败: {str(e)}")
            return False
    
    def set_data(self, key, value, tool_name=None, description=""):
        """存储共享数据
        
        Args:
            key: 数据键名
            value: 数据值
            tool_name: 设置数据的工具名称
            description: 数据描述
        
        Returns:
            bool: 操作是否成功
        """
        try:
            # 更新共享数据
            _shared_data[key] = {
                'value': value,
                'tool': tool_name,
                'description': description,
                'timestamp': datetime.now().isoformat()
            }
            
            # 更新历史记录
            if key not in _data_history:
                _data_history[key] = []
            
            _data_history[key].append({
                'value': value,
                'tool': tool_name,
                'timestamp': datetime.now().isoformat()
            })
            
            # 限制历史记录数量
            if len(_data_history[key]) > 10:
                _data_history[key] = _data_history[key][-10:]
            
            return self._save_shared_data()
        except Exception as e:
            print_error(f"设置共享数据失败: {str(e)}")
            return False
    
    def get_data(self, key):
        """获取共享数据
        
        Args:
            key: 数据键名
            
        Returns:
            数据值，如果不存在返回None
        """
        if key in _shared_data:
            return _shared_data[key]['value']
        return None
    
    def get_data_info(self, key):
        """获取共享数据的详细信息
        
        Args:
            key: 数据键名
            
        Returns:
            dict: 数据详细信息
        """
        return _shared_data.get(key, None)
    
    def list_all_data(self):
        """列出所有共享数据
        
        Returns:
            dict: 所有共享数据
        """
        return _shared_data
    
    def delete_data(self, key):
        """删除共享数据
        
        Args:
            key: 数据键名
            
        Returns:
            bool: 操作是否成功
        """
        if key in _shared_data:
            del _shared_data[key]
            return self._save_shared_data()
        return False
    
    def clear_all_data(self):
        """清除所有共享数据
        
        Returns:
            bool: 操作是否成功
        """
        global _shared_data
        _shared_data = {}
        return self._save_shared_data()
    
    def get_history(self, key=None):
        """获取数据历史记录
        
        Args:
            key: 数据键名，为None时获取所有历史
            
        Returns:
            dict/list: 历史记录
        """
        if key is not None:
            return _data_history.get(key, [])
        return _data_history

# 创建全局数据共享实例
data_sharer = DataSharer()

def show_data_sharer_menu():
    """显示数据共享管理菜单"""
    while True:
        clear_screen()
        print_title("数据共享管理器")
        print("\n请选择操作：")
        print("1. 查看所有共享数据")
        print("2. 添加共享数据")
        print("3. 获取共享数据")
        print("4. 删除共享数据")
        print("5. 查看数据历史")
        print("6. 清除所有共享数据")
        print("0. 返回")
        
        choice = input("\n请输入选择: ")
        
        if choice == '1':
            list_shared_data()
        elif choice == '2':
            add_shared_data()
        elif choice == '3':
            get_shared_data()
        elif choice == '4':
            delete_shared_data()
        elif choice == '5':
            view_data_history()
        elif choice == '6':
            clear_all_data()
        elif choice == '0':
            break
        else:
            print_error("无效的选择，请重新输入")
            pause()

def list_shared_data():
    """列出所有共享数据"""
    clear_screen()
    print_title("所有共享数据")
    
    all_data = data_sharer.list_all_data()
    
    if not all_data:
        print_info("当前没有共享数据")
    else:
        # 准备表格数据
        table_data = []
        for key, data_info in all_data.items():
            value = str(data_info['value'])
            if len(value) > 50:
                value = value[:47] + "..."
            
            table_data.append([
                key,
                value,
                data_info.get('tool', '未知'),
                data_info.get('description', ''),
                data_info.get('timestamp', '')
            ])
        
        # 显示表格
        headers = ["键名", "数据值", "设置工具", "描述", "时间戳"]
        print_table(headers, table_data)
        
        print(f"\n共有 {len(all_data)} 条共享数据")
    
    pause()

def add_shared_data():
    """添加共享数据"""
    clear_screen()
    print_title("添加共享数据")
    
    key = input("\n请输入数据键名: ")
    if not key.strip():
        print_error("键名不能为空")
        pause()
        return
    
    # 检查键名是否已存在
    if data_sharer.get_data_info(key):
        current_value = data_sharer.get_data(key)
        print_warning(f"警告: 键 '{key}' 已存在，当前值为: {current_value}")
        overwrite = input("是否覆盖？(y/n): ").lower()
        if overwrite != 'y':
            print_info("已取消操作")
            pause()
            return
    
    value_input = input("请输入数据值: ")
    description = input("请输入数据描述 (可选): ")
    tool_name = input("请输入工具名称 (可选): ")
    
    # 尝试将输入转换为适当的数据类型
    value = value_input
    try:
        # 尝试转换为数字
        if '.' in value_input:
            value = float(value_input)
        else:
            value = int(value_input)
    except ValueError:
        # 尝试转换为布尔值
        if value_input.lower() in ['true', 'false']:
            value = value_input.lower() == 'true'
        # 尝试转换为JSON
        elif value_input.startswith('{') and value_input.endswith('}') or \
             value_input.startswith('[') and value_input.endswith(']'):
            try:
                value = json.loads(value_input)
            except json.JSONDecodeError:
                pass  # 保持为字符串
    
    if data_sharer.set_data(key, value, tool_name, description):
        print_success(f"数据 '{key}' 已成功添加")
    else:
        print_error("添加数据失败")
    
    pause()

def get_shared_data():
    """获取共享数据"""
    clear_screen()
    print_title("获取共享数据")
    
    key = input("\n请输入要获取的数据键名: ")
    
    data_info = data_sharer.get_data_info(key)
    if data_info:
        print(f"\n键名: {key}")
        print(f"数据值: {data_sharer.get_data(key)}")
        print(f"设置工具: {data_info.get('tool', '未知')}")
        print(f"描述: {data_info.get('description', '无')}")
        print(f"时间戳: {data_info.get('timestamp', '未知')}")
    else:
        print_error(f"未找到键名为 '{key}' 的共享数据")
    
    pause()

def delete_shared_data():
    """删除共享数据"""
    clear_screen()
    print_title("删除共享数据")
    
    key = input("\n请输入要删除的数据键名: ")
    
    data_info = data_sharer.get_data_info(key)
    if data_info:
        print(f"\n确认删除以下数据:")
        print(f"键名: {key}")
        print(f"数据值: {data_sharer.get_data(key)}")
        print(f"设置工具: {data_info.get('tool', '未知')}")
        
        confirm = input("\n确定要删除吗？(y/n): ").lower()
        if confirm == 'y':
            if data_sharer.delete_data(key):
                print_success(f"数据 '{key}' 已成功删除")
            else:
                print_error("删除数据失败")
        else:
            print_info("已取消操作")
    else:
        print_error(f"未找到键名为 '{key}' 的共享数据")
    
    pause()

def view_data_history():
    """查看数据历史"""
    clear_screen()
    print_title("数据历史记录")
    
    print("1. 查看所有数据的历史")
    print("2. 查看特定数据的历史")
    
    sub_choice = input("\n请选择: ")
    
    if sub_choice == '1':
        all_history = data_sharer.get_history()
        if not all_history:
            print_info("没有历史记录")
        else:
            for key, history in all_history.items():
                print(f"\n\n数据键名: {key}")
                print("历史记录:")
                for i, record in enumerate(history, 1):
                    value = str(record['value'])
                    if len(value) > 30:
                        value = value[:27] + "..."
                    print(f"  {i}. [{record['timestamp']}] 工具: {record.get('tool', '未知')} - 值: {value}")
    elif sub_choice == '2':
        key = input("请输入要查看历史的数据键名: ")
        history = data_sharer.get_history(key)
        if not history:
            print_info(f"没有键 '{key}' 的历史记录")
        else:
            print(f"\n键 '{key}' 的历史记录:")
            for i, record in enumerate(history, 1):
                print(f"  {i}. 时间: {record['timestamp']}")
                print(f"     工具: {record.get('tool', '未知')}")
                print(f"     值: {record['value']}")
                print()
    else:
        print_error("无效的选择")
    
    pause()

def clear_all_data():
    """清除所有共享数据"""
    clear_screen()
    print_title("清除所有共享数据")
    
    all_data = data_sharer.list_all_data()
    if not all_data:
        print_info("当前没有共享数据")
    else:
        print_warning("警告: 这将清除所有共享数据！")
        print(f"\n当前共有 {len(all_data)} 条共享数据")
        
        confirm = input("\n确定要清除所有共享数据吗？(yes/no): ").lower()
        if confirm == 'yes':
            if data_sharer.clear_all_data():
                print_success("所有共享数据已清除")
            else:
                print_error("清除数据失败")
        else:
            print_info("已取消操作")
    
    pause()

def main():
    """主函数"""
    try:
        show_data_sharer_menu()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print_error(f"发生错误: {str(e)}")
    finally:
        print_info("数据共享管理器已退出")

if __name__ == '__main__':
    main()