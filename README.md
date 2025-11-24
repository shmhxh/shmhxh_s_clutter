# Python工具箱

![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

一个集多种实用工具于一体的Python工具箱，旨在提供便捷的日常工具集合。

## 功能特性

- 模块化设计，易于扩展
- 丰富的工具集合，包括文件操作、文本处理、网络工具、系统工具和图像处理等
- 交互式命令行界面，使用简单
- 支持命令行直接调用特定工具
- 配置化设计，可自定义工具箱行为

## 目录结构

```
shmhxh_s_clutter/
├── python_toolbox/      # 核心工具库目录
│   ├── main.py          # 主程序入口
│   ├── tools/           # 工具模块目录
│   │   ├── file_tools/  # 文件操作工具
│   │   ├── text_tools/  # 文本处理工具
│   │   ├── network_tools/ # 网络相关工具
│   │   ├── system_tools/  # 系统工具
│   │   └── image_tools/   # 图像处理工具
│   ├── config/          # 配置相关
│   │   └── config.py    # 配置管理模块
│   └── docs/            # 文档目录
├── tests/               # 测试文件目录
│   ├── comprehensive_test.py      # 综合测试脚本
│   ├── simple_gui_test.py         # 简化版GUI测试
│   ├── test_gui_tool_display.py   # GUI工具显示测试
│   └── test_tool_loading.py       # 工具加载测试
├── python_toolbox_gui.py  # 完整版GUI程序
├── simple_gui_fixed.py    # 简化版GUI程序
├── minimal_gui.py         # 极简版GUI程序
├── fix_null_bytes.py      # 修复空字节工具
├── README.md              # 项目说明文档
└── .gitignore             # Git忽略文件
```

## 安装说明

### 基本要求

- Python 3.6 或更高版本

### 安装步骤

1. 克隆或下载本项目到本地

2. 进入项目目录
   ```bash
   cd python_toolbox
   ```

3. 安装依赖（如果有）
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

### 交互式模式

运行主程序，进入交互式界面：

```bash
python main.py
```

然后按照提示进行操作，可以浏览工具、搜索工具或查看帮助。

### 命令行模式

#### 列出所有可用工具

```bash
python main.py --list
```

#### 直接运行特定工具

```bash
python main.py --tool category.tool_name
```

例如：
```bash
python main.py --tool file_tools.file_info
```

### GUI模式

本项目提供了三种不同版本的GUI程序，您可以根据需要选择使用：

#### 完整版GUI程序

功能最完善的GUI版本，提供了完整的工具分类和搜索功能：

```bash
python python_toolbox_gui.py
```

#### 简化版GUI程序

功能简化但使用更轻量的GUI版本：

```bash
python simple_gui_fixed.py
```

#### 极简版GUI程序

仅包含最基本功能的极简GUI版本：

```bash
python minimal_gui.py
```

## 工具列表

### 文件操作工具 (file_tools)
- 文件信息查看
- 文件批量重命名
- 文件内容搜索
- 文件压缩/解压
- 文件转换

### 文本处理工具 (text_tools)
- 文本编码转换
- 文本格式化
- 文本统计
- 文本加密/解密
- 正则表达式匹配

### 网络工具 (network_tools)
- HTTP 请求测试
- IP查询
- 网络速度测试
- 域名解析
- 端口扫描

### 系统工具 (system_tools)
- 系统信息查看
- 进程管理
- 服务管理
- 磁盘空间分析
- 环境变量管理

### 图像处理工具 (image_tools)
- 图片格式转换
- 图片压缩
- 图片尺寸调整
- 图片水印添加
- 图片特效处理

## 添加新工具

要向工具箱添加新工具，请按照以下步骤操作：

1. 在相应的工具分类目录下创建新的Python文件
2. 在文件中实现必要的功能，并确保有main()函数作为入口点
3. 添加适当的文档字符串说明工具功能和用法
4. 重新运行主程序，新工具将自动加载

## 配置说明

工具箱的配置文件位于用户目录下的`.python_toolbox/config.json`。您可以通过修改此文件或在程序中使用配置管理功能来更改设置。

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件获取更多信息。

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v1.0.0
- 初始版本发布
- 实现基础框架和工具加载机制
- 添加常用工具模块