#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图像格式转换工具
用于在不同图像格式之间进行转换
"""

import os
from PIL import Image
import argparse


def convert_image(input_path, output_path):
    """
    将图像从一种格式转换为另一种格式
    
    Args:
        input_path: 输入图像的路径
        output_path: 输出图像的路径
    
    Returns:
        bool: 如果转换成功返回True，否则返回False
        str: 错误消息，如果成功则为空字符串
    """
    try:
        # 验证输入文件存在
        if not os.path.exists(input_path):
            return False, f"错误：输入文件 '{input_path}' 不存在"
        
        # 验证输出目录存在，如果不存在则创建
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 打开并转换图像
        img = Image.open(input_path)
        
        # 获取输出格式（从文件扩展名）
        output_format = os.path.splitext(output_path)[1].lower().replace('.', '')
        
        # 对于不同的格式有特殊处理
        if output_format == 'jpg' or output_format == 'jpeg':
            # JPEG不支持透明度，需要转换模式
            if img.mode == 'RGBA':
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                # 粘贴图像并保留不透明部分
                background.paste(img, mask=img.split()[3])  # 3是alpha通道
                background.save(output_path, 'JPEG')
            else:
                img.convert('RGB').save(output_path, 'JPEG')
        elif output_format == 'png':
            img.save(output_path, 'PNG')
        elif output_format == 'bmp':
            img.save(output_path, 'BMP')
        elif output_format == 'gif':
            img.save(output_path, 'GIF')
        elif output_format == 'tiff' or output_format == 'tif':
            img.save(output_path, 'TIFF')
        else:
            # 尝试使用PIL支持的格式
            img.save(output_path)
        
        return True, ""
    except Exception as e:
        return False, f"转换失败: {str(e)}"


def batch_convert(input_dir, output_dir, output_format):
    """
    批量转换目录中的所有图像文件
    
    Args:
        input_dir: 输入目录的路径
        output_dir: 输出目录的路径
        output_format: 输出图像格式（不包含点）
    
    Returns:
        dict: 包含转换结果的字典 {"成功": 数量, "失败": 数量, "失败列表": [(文件路径, 错误消息)]}
    """
    results = {"成功": 0, "失败": 0, "失败列表": []}
    
    # 验证输入目录存在
    if not os.path.exists(input_dir):
        results["失败"] += 1
        results["失败列表"].append((input_dir, "输入目录不存在"))
        return results
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 支持的图像格式
    supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif']
    
    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        # 检查文件扩展名是否为支持的图像格式
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in supported_formats:
            input_path = os.path.join(input_dir, filename)
            # 创建输出文件名
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, f"{base_name}.{output_format}")
            
            # 转换图像
            success, message = convert_image(input_path, output_path)
            if success:
                results["成功"] += 1
            else:
                results["失败"] += 1
                results["失败列表"].append((input_path, message))
    
    return results


def resize_image(input_path, output_path, width=None, height=None, maintain_ratio=True):
    """
    调整图像大小
    
    Args:
        input_path: 输入图像的路径
        output_path: 输出图像的路径
        width: 新宽度
        height: 新高度
        maintain_ratio: 是否保持宽高比
    
    Returns:
        bool: 如果调整大小成功返回True，否则返回False
        str: 错误消息，如果成功则为空字符串
    """
    try:
        # 验证输入文件存在
        if not os.path.exists(input_path):
            return False, f"错误：输入文件 '{input_path}' 不存在"
        
        # 验证输出目录存在，如果不存在则创建
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 打开图像
        img = Image.open(input_path)
        
        # 计算新尺寸
        original_width, original_height = img.size
        
        if maintain_ratio:
            if width is None and height is None:
                return False, "错误：必须指定宽度或高度"
            elif width is not None and height is None:
                # 按宽度缩放，保持比例
                ratio = width / original_width
                new_width = width
                new_height = int(original_height * ratio)
            elif width is None and height is not None:
                # 按高度缩放，保持比例
                ratio = height / original_height
                new_width = int(original_width * ratio)
                new_height = height
            else:
                # 同时指定了宽度和高度，选择缩放比例较大的那个以避免留空白
                width_ratio = width / original_width
                height_ratio = height / original_height
                if width_ratio < height_ratio:
                    ratio = width_ratio
                    new_width = width
                    new_height = int(original_height * ratio)
                else:
                    ratio = height_ratio
                    new_width = int(original_width * ratio)
                    new_height = height
        else:
            # 不保持比例，直接使用指定的宽度和高度
            if width is None or height is None:
                return False, "错误：不保持宽高比时必须同时指定宽度和高度"
            new_width = width
            new_height = height
        
        # 调整图像大小
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # 保存调整后的图像
        resized_img.save(output_path)
        
        return True, f"已将图像调整为 {new_width}x{new_height}"
    except Exception as e:
        return False, f"调整大小失败: {str(e)}"


def convert_to_grayscale(input_path, output_path):
    """
    将图像转换为灰度图
    
    Args:
        input_path: 输入图像的路径
        output_path: 输出图像的路径
    
    Returns:
        bool: 如果转换成功返回True，否则返回False
        str: 错误消息，如果成功则为空字符串
    """
    try:
        # 验证输入文件存在
        if not os.path.exists(input_path):
            return False, f"错误：输入文件 '{input_path}' 不存在"
        
        # 验证输出目录存在，如果不存在则创建
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 打开图像并转换为灰度
        img = Image.open(input_path).convert('L')
        
        # 保存灰度图
        img.save(output_path)
        
        return True, ""
    except Exception as e:
        return False, f"转换为灰度图失败: {str(e)}"


def display_image_info(input_path):
    """
    显示图像信息
    
    Args:
        input_path: 输入图像的路径
    
    Returns:
        dict: 图像信息字典
        str: 错误消息，如果成功则为空字符串
    """
    try:
        # 验证输入文件存在
        if not os.path.exists(input_path):
            return {}, f"错误：输入文件 '{input_path}' 不存在"
        
        # 打开图像
        img = Image.open(input_path)
        
        # 获取图像信息
        info = {
            "文件路径": input_path,
            "文件名": os.path.basename(input_path),
            "格式": img.format,
            "模式": img.mode,
            "尺寸": f"{img.width}x{img.height}",
            "宽度": img.width,
            "高度": img.height,
            "文件大小": f"{os.path.getsize(input_path) / 1024:.2f} KB"
        }
        
        # 如果是彩色图像，添加色彩通道信息
        if img.mode == 'RGB':
            info["色彩通道"] = "RGB"
        elif img.mode == 'RGBA':
            info["色彩通道"] = "RGBA (带透明度)"
        elif img.mode == 'L':
            info["色彩通道"] = "灰度"
        elif img.mode == 'CMYK':
            info["色彩通道"] = "CMYK"
        else:
            info["色彩通道"] = img.mode
        
        return info, ""
    except Exception as e:
        return {}, f"获取图像信息失败: {str(e)}"


def main():
    """
    主函数，用于命令行调用
    """
    parser = argparse.ArgumentParser(description='图像格式转换工具')
    
    # 创建子命令解析器
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 单个文件转换命令
    convert_parser = subparsers.add_parser('convert', help='转换单个图像')
    convert_parser.add_argument('input', help='输入图像路径')
    convert_parser.add_argument('output', help='输出图像路径')
    
    # 批量转换命令
    batch_parser = subparsers.add_parser('batch', help='批量转换图像')
    batch_parser.add_argument('input_dir', help='输入目录')
    batch_parser.add_argument('output_dir', help='输出目录')
    batch_parser.add_argument('format', help='输出格式 (如: png, jpg, bmp等)')
    
    # 调整大小命令
    resize_parser = subparsers.add_parser('resize', help='调整图像大小')
    resize_parser.add_argument('input', help='输入图像路径')
    resize_parser.add_argument('output', help='输出图像路径')
    resize_parser.add_argument('--width', type=int, help='新宽度')
    resize_parser.add_argument('--height', type=int, help='新高度')
    resize_parser.add_argument('--no-ratio', action='store_true', help='不保持宽高比')
    
    # 转换为灰度图命令
    gray_parser = subparsers.add_parser('grayscale', help='转换为灰度图')
    gray_parser.add_argument('input', help='输入图像路径')
    gray_parser.add_argument('output', help='输出图像路径')
    
    # 显示图像信息命令
    info_parser = subparsers.add_parser('info', help='显示图像信息')
    info_parser.add_argument('input', help='输入图像路径')
    
    args = parser.parse_args()
    
    # 根据命令执行相应操作
    if args.command == 'convert':
        success, message = convert_image(args.input, args.output)
        if success:
            print(f"图像已成功转换: {args.input} -> {args.output}")
        else:
            print(message)
    
    elif args.command == 'batch':
        results = batch_convert(args.input_dir, args.output_dir, args.format)
        print(f"批量转换完成：")
        print(f"  成功: {results['成功']}")
        print(f"  失败: {results['失败']}")
        if results['失败'] > 0:
            print("失败的文件：")
            for path, msg in results['失败列表']:
                print(f"  - {path}: {msg}")
    
    elif args.command == 'resize':
        success, message = resize_image(args.input, args.output, 
                                        args.width, args.height, 
                                        not args.no_ratio)
        if success:
            print(f"图像大小已调整: {args.input} -> {args.output}")
            print(message)
        else:
            print(message)
    
    elif args.command == 'grayscale':
        success, message = convert_to_grayscale(args.input, args.output)
        if success:
            print(f"图像已转换为灰度图: {args.input} -> {args.output}")
        else:
            print(message)
    
    elif args.command == 'info':
        info, message = display_image_info(args.input)
        if info:
            print("图像信息:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        else:
            print(message)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()