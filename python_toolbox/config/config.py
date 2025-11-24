#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python工具箱配置文件
管理工具箱的各种设置和配置
"""

import os
import json
import platform

# 获取配置目录
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(CONFIG_DIR))

# 用户数据目录
USER_DATA_DIR = os.path.join(os.path.expanduser('~'), '.python_toolbox')

# 创建用户数据目录
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

# 配置文件路径
CONFIG_FILE = os.path.join(USER_DATA_DIR, 'config.json')

# 默认配置
DEFAULT_CONFIG = {
    'language': 'zh_CN',
    'theme': 'default',
    'recent_tools': [],
    'max_recent_tools': 10,
    'auto_update': True,
    'update_check_interval': 7,  # 天
    'last_update_check': '',
    'temp_dir': os.path.join(USER_DATA_DIR, 'temp'),
    'log_level': 'INFO',
    'log_file': os.path.join(USER_DATA_DIR, 'toolbox.log'),
    'editor': 'notepad' if platform.system() == 'Windows' else 'nano'
}

# 配置缓存
_config_cache = None

def load_config():
    """加载配置文件"""
    global _config_cache
    
    if _config_cache is not None:
        return _config_cache
    
    config = DEFAULT_CONFIG.copy()
    
    # 如果配置文件存在，读取并合并配置
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                config.update(user_config)
        except Exception as e:
            print(f"警告: 读取配置文件失败: {str(e)}")
    else:
        # 如果配置文件不存在，创建默认配置文件
        save_config(config)
    
    # 创建必要的目录
    if not os.path.exists(config['temp_dir']):
        os.makedirs(config['temp_dir'])
    
    _config_cache = config
    return config

def save_config(config=None):
    """保存配置文件"""
    global _config_cache
    
    if config is None:
        config = _config_cache or DEFAULT_CONFIG
    
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        _config_cache = config
        return True
    except Exception as e:
        print(f"警告: 保存配置文件失败: {str(e)}")
        return False

def get_config(key, default=None):
    """获取指定配置项"""
    config = load_config()
    return config.get(key, default)

def set_config(key, value):
    """设置指定配置项"""
    config = load_config()
    config[key] = value
    return save_config(config)

def add_recent_tool(tool_name):
    """添加最近使用的工具"""
    config = load_config()
    recent_tools = config.get('recent_tools', [])
    
    # 如果工具已经在列表中，先移除
    if tool_name in recent_tools:
        recent_tools.remove(tool_name)
    
    # 添加到列表开头
    recent_tools.insert(0, tool_name)
    
    # 限制列表长度
    max_recent = config.get('max_recent_tools', 10)
    recent_tools = recent_tools[:max_recent]
    
    config['recent_tools'] = recent_tools
    return save_config(config)

def get_recent_tools():
    """获取最近使用的工具列表"""
    config = load_config()
    return config.get('recent_tools', [])

def reset_config():
    """重置配置为默认值"""
    global _config_cache
    _config_cache = DEFAULT_CONFIG.copy()
    return save_config(_config_cache)

def get_system_info():
    """获取系统信息"""
    return {
        'platform': platform.system(),
        'release': platform.release(),
        'python_version': platform.python_version(),
        'config_dir': CONFIG_DIR,
        'user_data_dir': USER_DATA_DIR
    }

# 加载配置
config = load_config()

# 将配置项添加到全局变量
for key, value in config.items():
    globals()[key.upper()] = value

def get_tool_path(tool_category, tool_name):
    """获取工具模块路径"""
    return os.path.join(ROOT_DIR, 'tools', tool_category, f'{tool_name}.py')

def is_tool_available(tool_category, tool_name):
    """检查工具是否可用"""
    tool_path = get_tool_path(tool_category, tool_name)
    return os.path.exists(tool_path)