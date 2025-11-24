#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文本分析工具
用于分析文本内容，统计字符数、单词数、行数等信息
"""

import os
import re
from collections import Counter


def analyze_text_from_file(file_path):
    """
    从文件中读取文本并分析
    
    Args:
        file_path: 文件路径
    
    Returns:
        dict: 包含文本分析结果的字典
        str: 错误信息，如果有
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return None, f"错误: 文件 '{file_path}' 不存在"
        
        # 检查是否为文件
        if not os.path.isfile(file_path):
            return None, f"错误: '{file_path}' 不是一个文件"
        
        # 尝试以不同的编码读取文件
        encodings = ['utf-8', 'gbk', 'latin-1']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            return None, "错误: 无法解码文件内容，请检查文件编码"
        
        return analyze_text(content), None
    
    except Exception as e:
        return None, f"读取文件时发生错误: {str(e)}"


def analyze_text(text):
    """
    分析文本内容
    
    Args:
        text: 要分析的文本内容
    
    Returns:
        dict: 包含文本分析结果的字典
    """
    # 计算行数
    lines = text.split('\n')
    line_count = len(lines)
    
    # 计算非空行数
    non_empty_lines = sum(1 for line in lines if line.strip())
    
    # 计算字符数（包括空格）
    char_count = len(text)
    
    # 计算字符数（不包括空格）
    char_count_no_space = len(text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', ''))
    
    # 计算中文字符数
    chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', text))
    
    # 计算单词数（英文单词）
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    word_count = len(words)
    
    # 计算单词频率
    word_freq = Counter(words)
    top_words = word_freq.most_common(10)
    
    # 计算句子数（简单判断，以句号、问号、感叹号结尾）
    sentences = re.split(r'[.!?。！？]', text)
    sentence_count = sum(1 for s in sentences if s.strip())
    
    # 计算平均每行字符数
    avg_chars_per_line = char_count / line_count if line_count > 0 else 0
    
    # 计算平均每句单词数
    avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
    
    # 计算空格数
    space_count = text.count(' ')
    
    # 计算数字字符数
    digit_count = len(re.findall(r'\d', text))
    
    # 计算标点符号数
    punctuation_count = len(re.findall(r'[.,;:\'"!?()\[\]{}，。；：‘’“”！？（）【】{}]', text))
    
    # 构建分析结果
    result = {
        '总行数': line_count,
        '非空行数': non_empty_lines,
        '总字符数（含空格）': char_count,
        '总字符数（不含空格）': char_count_no_space,
        '中文字符数': chinese_chars,
        '英文字符数': char_count_no_space - chinese_chars - digit_count,
        '数字字符数': digit_count,
        '空格数': space_count,
        '标点符号数': punctuation_count,
        '单词数': word_count,
        '句子数': sentence_count,
        '平均每行字符数': f"{avg_chars_per_line:.2f}",
        '平均每句单词数': f"{avg_words_per_sentence:.2f}"
    }
    
    if top_words:
        result['出现频率最高的10个单词'] = ', '.join([f"{word}({count})" for word, count in top_words])
    
    return result


def display_analysis_result(result):
    """
    显示文本分析结果
    
    Args:
        result: 分析结果字典
    """
    print("=" * 50)
    print("文本分析结果".center(48))
    print("=" * 50)
    
    for key, value in result.items():
        print(f"{key:<25}: {value}")
    
    print("=" * 50)


def main():
    """
    主函数
    """
    print("文本分析工具")
    print("=" * 30)
    
    while True:
        print("\n请选择分析方式:")
        print("1. 从文件分析")
        print("2. 直接输入文本分析")
        print("q. 退出")
        
        choice = input("\n请选择 (1/2/q): ")
        
        if choice.lower() == 'q':
            print("\n感谢使用文本分析工具！")
            break
        
        if choice == '1':
            file_path = input("请输入文件路径: ")
            
            # 处理相对路径
            if not os.path.isabs(file_path):
                file_path = os.path.join(os.getcwd(), file_path)
            
            result, error = analyze_text_from_file(file_path)
            if error:
                print(error)
            else:
                display_analysis_result(result)
        
        elif choice == '2':
            print("\n请输入要分析的文本 (输入单独一行的 'END' 结束输入):")
            lines = []
            while True:
                line = input()
                if line == 'END':
                    break
                lines.append(line)
            
            text = '\n'.join(lines)
            if text.strip():
                result = analyze_text(text)
                display_analysis_result(result)
            else:
                print("警告: 输入的文本为空")
        
        else:
            print("无效的选择，请重新输入")


if __name__ == '__main__':
    main()