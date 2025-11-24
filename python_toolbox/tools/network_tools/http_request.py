#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP请求测试工具
用于发送HTTP请求并查看响应结果
"""

import requests
import json
import time


def send_http_request(url, method='GET', headers=None, params=None, data=None, json_data=None, timeout=10, verify=True):
    """
    发送HTTP请求
    
    Args:
        url: 请求URL
        method: 请求方法 (GET, POST, PUT, DELETE, etc.)
        headers: 请求头
        params: URL参数
        data: 请求体数据（表单格式）
        json_data: 请求体数据（JSON格式）
        timeout: 超时时间（秒）
        verify: 是否验证SSL证书
    
    Returns:
        dict: 包含响应信息的字典
        str: 错误信息，如果有
    """
    try:
        # 准备请求参数
        request_kwargs = {
            'timeout': timeout,
            'verify': verify
        }
        
        if headers:
            request_kwargs['headers'] = headers
        
        if params:
            request_kwargs['params'] = params
        
        if data:
            request_kwargs['data'] = data
        
        if json_data:
            request_kwargs['json'] = json_data
        
        # 记录开始时间
        start_time = time.time()
        
        # 发送请求
        response = requests.request(method, url, **request_kwargs)
        
        # 计算响应时间
        response_time = (time.time() - start_time) * 1000  # 毫秒
        
        # 尝试解析JSON响应
        try:
            content = response.json()
            content_type = 'json'
        except ValueError:
            content = response.text
            content_type = 'text'
        
        # 构建响应信息
        result = {
            'url': url,
            'method': method,
            'status_code': response.status_code,
            'status_message': response.reason,
            'response_time': f"{response_time:.2f} 毫秒",
            'content_length': len(response.content),
            'content_type': response.headers.get('content-type', 'unknown'),
            'headers': dict(response.headers),
            'content_type_parsed': content_type,
            'content': content
        }
        
        return result, None
    
    except requests.exceptions.RequestException as e:
        return None, f"请求出错: {str(e)}"
    except Exception as e:
        return None, f"发生未知错误: {str(e)}"


def display_response_info(response_info):
    """
    显示HTTP响应信息
    
    Args:
        response_info: 响应信息字典
    """
    print("=" * 50)
    print("HTTP请求响应结果".center(48))
    print("=" * 50)
    
    print(f"URL: {response_info['url']}")
    print(f"方法: {response_info['method']}")
    print(f"状态码: {response_info['status_code']} {response_info['status_message']}")
    print(f"响应时间: {response_info['response_time']}")
    print(f"内容长度: {response_info['content_length']} 字节")
    print(f"内容类型: {response_info['content_type']}")
    
    print("\n响应头:")
    for key, value in response_info['headers'].items():
        print(f"  {key}: {value}")
    
    print("\n响应内容:")
    if response_info['content_type_parsed'] == 'json':
        # 格式化JSON输出
        print(json.dumps(response_info['content'], indent=2, ensure_ascii=False))
    else:
        # 限制文本输出长度
        content = response_info['content']
        if len(content) > 1000:
            print(content[:1000] + "\n... (内容过长，已截断)")
        else:
            print(content)
    
    print("=" * 50)


def parse_headers(headers_str):
    """
    解析用户输入的请求头字符串
    
    Args:
        headers_str: 以换行分隔的请求头字符串
    
    Returns:
        dict: 请求头字典
    """
    headers = {}
    if headers_str.strip():
        for line in headers_str.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
    return headers


def main():
    """
    主函数
    """
    print("HTTP请求测试工具")
    print("=" * 30)
    
    while True:
        print("\n请选择操作:")
        print("1. 发送GET请求")
        print("2. 发送POST请求")
        print("3. 发送自定义请求")
        print("q. 退出")
        
        choice = input("\n请选择 (1/2/3/q): ")
        
        if choice.lower() == 'q':
            print("\n感谢使用HTTP请求测试工具！")
            break
        
        url = input("请输入请求URL: ")
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # 设置默认请求头
        headers = {'User-Agent': 'Python-Toolbox-HTTP-Request/1.0'}
        
        # 询问是否添加自定义请求头
        add_headers = input("是否添加自定义请求头？(y/n): ")
        if add_headers.lower() == 'y':
            print("请输入请求头（每行一个，格式: Key: Value，输入空行结束）:")
            headers_lines = []
            while True:
                line = input()
                if not line:
                    break
                headers_lines.append(line)
            custom_headers = parse_headers('\n'.join(headers_lines))
            headers.update(custom_headers)
        
        if choice == '1':
            # GET请求
            print("请输入URL参数（格式: key1=value1&key2=value2，留空表示无参数）:")
            params_str = input()
            params = {}
            if params_str.strip():
                for param in params_str.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        params[key] = value
            
            response_info, error = send_http_request(url, method='GET', headers=headers, params=params)
            
        elif choice == '2':
            # POST请求
            print("请选择POST数据格式:")
            print("1. 表单数据 (application/x-www-form-urlencoded)")
            print("2. JSON数据 (application/json)")
            data_type = input("请选择 (1/2): ")
            
            if data_type == '1':
                print("请输入表单数据（格式: key1=value1&key2=value2，留空表示无数据）:")
                data_str = input()
                data = {}
                if data_str.strip():
                    for param in data_str.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            data[key] = value
                
                response_info, error = send_http_request(url, method='POST', headers=headers, data=data)
            
            else:
                print("请输入JSON数据（留空表示无数据）:")
                json_str = input()
                json_data = None
                if json_str.strip():
                    try:
                        json_data = json.loads(json_str)
                    except json.JSONDecodeError:
                        print("错误: JSON格式无效")
                        continue
                
                # 添加Content-Type头
                headers['Content-Type'] = 'application/json'
                response_info, error = send_http_request(url, method='POST', headers=headers, json_data=json_data)
        
        elif choice == '3':
            # 自定义请求
            method = input("请输入请求方法 (GET/POST/PUT/DELETE等): ").upper()
            
            # 询问是否添加URL参数
            add_params = input("是否添加URL参数？(y/n): ")
            params = None
            if add_params.lower() == 'y':
                print("请输入URL参数（格式: key1=value1&key2=value2）:")
                params_str = input()
                params = {}
                if params_str.strip():
                    for param in params_str.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            params[key] = value
            
            # 询问是否添加请求体
            add_body = input("是否添加请求体？(y/n): ")
            data = None
            json_data = None
            if add_body.lower() == 'y':
                print("请选择请求体格式:")
                print("1. 表单数据 (application/x-www-form-urlencoded)")
                print("2. JSON数据 (application/json)")
                body_type = input("请选择 (1/2): ")
                
                if body_type == '1':
                    print("请输入表单数据（格式: key1=value1&key2=value2）:")
                    data_str = input()
                    data = {}
                    if data_str.strip():
                        for param in data_str.split('&'):
                            if '=' in param:
                                key, value = param.split('=', 1)
                                data[key] = value
                
                else:
                    print("请输入JSON数据:")
                    json_str = input()
                    try:
                        json_data = json.loads(json_str)
                    except json.JSONDecodeError:
                        print("错误: JSON格式无效")
                        continue
                    
                    # 添加Content-Type头
                    headers['Content-Type'] = 'application/json'
            
            # 询问是否跳过SSL验证
            skip_ssl = input("是否跳过SSL证书验证？(y/n): ")
            verify = skip_ssl.lower() != 'y'
            
            response_info, error = send_http_request(
                url, method=method, headers=headers, params=params, 
                data=data, json_data=json_data, verify=verify
            )
        
        else:
            print("无效的选择，请重新输入")
            continue
        
        if error:
            print(f"\n{error}")
        else:
            display_response_info(response_info)


if __name__ == '__main__':
    main()