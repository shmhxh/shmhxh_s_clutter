#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文本转换工具
用于文本的各种转换操作，如大小写转换、全半角转换、去除空白等
"""

import os
import re
import argparse
from typing import Optional


def to_uppercase(text: str) -> str:
    """
    将文本转换为全大写
    
    Args:
        text: 输入文本
    
    Returns:
        str: 转换后的文本
    """
    return text.upper()


def to_lowercase(text: str) -> str:
    """
    将文本转换为全小写
    
    Args:
        text: 输入文本
    
    Returns:
        str: 转换后的文本
    """
    return text.lower()


def to_titlecase(text: str) -> str:
    """
    将文本转换为标题大小写（每个单词首字母大写）
    
    Args:
        text: 输入文本
    
    Returns:
        str: 转换后的文本
    """
    return text.title()


def to_sentencecase(text: str) -> str:
    """
    将文本转换为句子大小写（每个句子首字母大写）
    
    Args:
        text: 输入文本
    
    Returns:
        str: 转换后的文本
    """
    # 分割句子并将每个句子首字母大写
    sentences = re.split(r'(\.\s+|!\s+|\?\s+)', text)
    result = []
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        if sentence:
            # 将句子首字母大写
            sentence = sentence[0].upper() + sentence[1:].lower()
        result.append(sentence)
        
        # 添加分隔符（如果存在）
        if i + 1 < len(sentences):
            result.append(sentences[i + 1])
    
    return ''.join(result)


def full_to_half(text: str) -> str:
    """
    将全角字符转换为半角字符
    
    Args:
        text: 输入文本
    
    Returns:
        str: 转换后的文本
    """
    result = []
    for char in text:
        code = ord(char)
        # 全角空格转换为半角空格
        if code == 0x3000:
            result.append(' ')
        # 全角ASCII字符（！"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~）
        elif 0xFF01 <= code <= 0xFF5E:
            result.append(chr(code - 0xFEE0))
        else:
            result.append(char)
    return ''.join(result)


def half_to_full(text: str) -> str:
    """
    将半角字符转换为全角字符
    
    Args:
        text: 输入文本
    
    Returns:
        str: 转换后的文本
    """
    result = []
    for char in text:
        code = ord(char)
        # 半角空格转换为全角空格
        if code == 0x20:
            result.append('　')
        # 半角ASCII字符
        elif 0x21 <= code <= 0x7E:
            result.append(chr(code + 0xFEE0))
        else:
            result.append(char)
    return ''.join(result)


def remove_whitespace(text: str, mode: str = 'all') -> str:
    """
    去除空白字符
    
    Args:
        text: 输入文本
        mode: 去除模式
            'all': 去除所有空白字符
            'leading': 只去除开头的空白字符
            'trailing': 只去除结尾的空白字符
            'duplicate': 只去除连续的重复空白字符
    
    Returns:
        str: 转换后的文本
    """
    if mode == 'all':
        return re.sub(r'\s+', '', text)
    elif mode == 'leading':
        return re.sub(r'^\s+', '', text)
    elif mode == 'trailing':
        return re.sub(r'\s+$', '', text)
    elif mode == 'duplicate':
        return re.sub(r'\s{2,}', ' ', text)
    else:
        return text


def strip_lines(text: str, remove_empty_lines: bool = False) -> str:
    """
    去除每行首尾的空白字符
    
    Args:
        text: 输入文本
        remove_empty_lines: 是否同时移除空行
    
    Returns:
        str: 转换后的文本
    """
    lines = text.split('\n')
    if remove_empty_lines:
        # 去除空白行并去除每行的首尾空白
        lines = [line.strip() for line in lines if line.strip()]
    else:
        # 只去除每行的首尾空白
        lines = [line.strip() for line in lines]
    return '\n'.join(lines)


def reverse_text(text: str, mode: str = 'character') -> str:
    """
    反转文本
    
    Args:
        text: 输入文本
        mode: 反转模式
            'character': 按字符反转
            'line': 按行反转
            'word': 按单词反转（保持单词内部顺序）
    
    Returns:
        str: 转换后的文本
    """
    if mode == 'character':
        return text[::-1]
    elif mode == 'line':
        lines = text.split('\n')
        return '\n'.join(reversed(lines))
    elif mode == 'word':
        # 按单词反转，但保持单词内部顺序
        words = re.findall(r'\S+|\s+', text)
        return ''.join(reversed(words))
    else:
        return text


def escape_special_chars(text: str, mode: str = 'python') -> str:
    """
    转义特殊字符
    
    Args:
        text: 输入文本
        mode: 转义模式
            'python': Python字符串转义
            'html': HTML实体转义
            'json': JSON字符串转义
    
    Returns:
        str: 转换后的文本
    """
    if mode == 'python':
        return repr(text)[1:-1]  # 使用repr但去除首尾的引号
    elif mode == 'html':
        # 简单的HTML实体转义
        html_escape_table = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }
        return ''.join(html_escape_table.get(c, c) for c in text)
    elif mode == 'json':
        # 简单的JSON字符串转义
        import json
        return json.dumps(text)[1:-1]  # 使用json.dumps但去除首尾的引号
    else:
        return text


def convert_text(input_text: str, conversion_type: str, **kwargs) -> str:
    """
    根据指定的转换类型转换文本
    
    Args:
        input_text: 输入文本
        conversion_type: 转换类型
        **kwargs: 额外的转换参数
    
    Returns:
        str: 转换后的文本
    """
    conversion_type = conversion_type.lower()
    
    if conversion_type == 'upper':
        return to_uppercase(input_text)
    elif conversion_type == 'lower':
        return to_lowercase(input_text)
    elif conversion_type == 'title':
        return to_titlecase(input_text)
    elif conversion_type == 'sentence':
        return to_sentencecase(input_text)
    elif conversion_type == 'full2half':
        return full_to_half(input_text)
    elif conversion_type == 'half2full':
        return half_to_full(input_text)
    elif conversion_type == 'strip':
        mode = kwargs.get('mode', 'all')
        return remove_whitespace(input_text, mode)
    elif conversion_type == 'strip_lines':
        remove_empty = kwargs.get('remove_empty', False)
        return strip_lines(input_text, remove_empty)
    elif conversion_type == 'reverse':
        mode = kwargs.get('mode', 'character')
        return reverse_text(input_text, mode)
    elif conversion_type == 'escape':
        mode = kwargs.get('mode', 'python')
        return escape_special_chars(input_text, mode)
    else:
        raise ValueError(f"未知的转换类型: {conversion_type}")


def process_file(input_path: str, output_path: Optional[str], conversion_type: str, **kwargs) -> bool:
    """
    处理文件中的文本
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径，如果为None则直接覆盖输入文件
        conversion_type: 转换类型
        **kwargs: 额外的转换参数
    
    Returns:
        bool: 处理是否成功
    """
    try:
        # 读取输入文件
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # 转换文本
        converted_text = convert_text(text, conversion_type, **kwargs)
        
        # 确定输出路径
        if output_path is None:
            output_path = input_path
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 写入输出文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(converted_text)
        
        return True
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return False


def batch_process(directory: str, conversion_type: str, extension: str = '.txt', recursive: bool = False, **kwargs) -> dict:
    """
    批量处理目录中的文件
    
    Args:
        directory: 目录路径
        conversion_type: 转换类型
        extension: 文件扩展名，默认为.txt
        recursive: 是否递归处理子目录
        **kwargs: 额外的转换参数
    
    Returns:
        dict: 处理结果统计 {"成功": 数量, "失败": 数量, "失败列表": [(文件路径, 错误消息)]}
    """
    results = {"成功": 0, "失败": 0, "失败列表": []}
    
    try:
        if recursive:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(extension):
                        file_path = os.path.join(root, file)
                        if process_file(file_path, None, conversion_type, **kwargs):
                            results["成功"] += 1
                        else:
                            results["失败"] += 1
                            results["失败列表"].append((file_path, "处理失败"))
        else:
            # 只处理当前目录
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path) and file.endswith(extension):
                    if process_file(file_path, None, conversion_type, **kwargs):
                        results["成功"] += 1
                    else:
                        results["失败"] += 1
                        results["失败列表"].append((file_path, "处理失败"))
    except Exception as e:
        results["失败"] += 1
        results["失败列表"].append((directory, str(e)))
    
    return results


def main():
    """
    主函数，用于命令行调用
    """
    parser = argparse.ArgumentParser(description='文本转换工具')
    
    # 创建子命令解析器
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 文本转换命令
    text_parser = subparsers.add_parser('text', help='转换文本')
    text_parser.add_argument('type', choices=['upper', 'lower', 'title', 'sentence', 'full2half', 'half2full', 
                                             'strip', 'strip_lines', 'reverse', 'escape'], 
                            help='转换类型')
    text_parser.add_argument('--input', type=str, help='输入文件路径，不指定则从标准输入读取')
    text_parser.add_argument('--output', type=str, help='输出文件路径，不指定则输出到标准输出')
    text_parser.add_argument('--mode', type=str, help='特定转换类型的模式')
    text_parser.add_argument('--remove-empty', action='store_true', help='strip_lines时移除空行')
    
    # 文件处理命令
    file_parser = subparsers.add_parser('file', help='处理单个文件')
    file_parser.add_argument('input', help='输入文件路径')
    file_parser.add_argument('--output', type=str, help='输出文件路径，不指定则覆盖输入文件')
    file_parser.add_argument('type', choices=['upper', 'lower', 'title', 'sentence', 'full2half', 'half2full', 
                                            'strip', 'strip_lines', 'reverse', 'escape'], 
                            help='转换类型')
    file_parser.add_argument('--mode', type=str, help='特定转换类型的模式')
    file_parser.add_argument('--remove-empty', action='store_true', help='strip_lines时移除空行')
    
    # 批量处理命令
    batch_parser = subparsers.add_parser('batch', help='批量处理文件')
    batch_parser.add_argument('directory', help='目录路径')
    batch_parser.add_argument('type', choices=['upper', 'lower', 'title', 'sentence', 'full2half', 'half2full', 
                                             'strip', 'strip_lines', 'reverse', 'escape'], 
                             help='转换类型')
    batch_parser.add_argument('--extension', type=str, default='.txt', help='文件扩展名，默认为.txt')
    batch_parser.add_argument('--recursive', action='store_true', help='递归处理子目录')
    batch_parser.add_argument('--mode', type=str, help='特定转换类型的模式')
    batch_parser.add_argument('--remove-empty', action='store_true', help='strip_lines时移除空行')
    
    args = parser.parse_args()
    
    # 准备额外参数
    kwargs = {}
    if hasattr(args, 'mode') and args.mode:
        kwargs['mode'] = args.mode
    if hasattr(args, 'remove_empty') and args.remove_empty:
        kwargs['remove_empty'] = True
    
    # 执行命令
    if args.command == 'text':
        # 读取输入
        if args.input:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            text = input("请输入要转换的文本: ")
        
        # 转换文本
        try:
            converted_text = convert_text(text, args.type, **kwargs)
            
            # 输出结果
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(converted_text)
                print(f"转换结果已保存到: {args.output}")
            else:
                print("\n转换结果:")
                print(converted_text)
        except ValueError as e:
            print(f"错误: {str(e)}")
    
    elif args.command == 'file':
        if process_file(args.input, args.output, args.type, **kwargs):
            if args.output:
                print(f"文件已转换并保存到: {args.output}")
            else:
                print(f"文件已转换: {args.input}")
    
    elif args.command == 'batch':
        results = batch_process(args.directory, args.type, args.extension, args.recursive, **kwargs)
        print(f"批量处理完成:")
        print(f"  成功: {results['成功']}")
        print(f"  失败: {results['失败']}")
        if results['失败'] > 0:
            print("失败的文件:")
            for path, msg in results['失败列表']:
                print(f"  - {path}: {msg}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()