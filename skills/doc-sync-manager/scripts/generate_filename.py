#!/usr/bin/env python3
"""
生成符合规范的文档文件名和飞书文档标题
"""

import argparse
from datetime import datetime


def generate_filename(task_type: str, module_name: str, date: str = None) -> str:
    """
    生成本地文档文件名
    
    Args:
        task_type: 任务类型 ('重构' 或 '新需求')
        module_name: 模块/页面名称
        date: 日期字符串 (YYYY-MM-DD)，默认为今天
    
    Returns:
        文件名，如: 2025-05-14_重构_用户中心页面.md
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # 清理模块名称，移除特殊字符
    clean_module = module_name.replace('/', '_').replace('\\\\', '_').replace(':', '_')
    
    return f"{date}_{task_type}_{clean_module}.md"


def generate_lark_title(task_type: str, module_name: str, date: str = None) -> str:
    """
    生成飞书文档标题
    
    Args:
        task_type: 任务类型 ('重构' 或 '新需求')
        module_name: 模块/页面名称
        date: 日期字符串 (YYYY-MM-DD)，默认为今天
    
    Returns:
        飞书文档标题，如: [重构] 用户中心页面 - 2025-05-14
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    return f"[{task_type}] {module_name} - {date}"


def main():
    parser = argparse.ArgumentParser(description='生成文档文件名和飞书标题')
    parser.add_argument('task_type', choices=['重构', '新需求'], help='任务类型')
    parser.add_argument('module_name', help='模块/页面名称')
    parser.add_argument('--date', help='日期 (YYYY-MM-DD)，默认为今天')
    parser.add_argument('--format', choices=['filename', 'title', 'both'], 
                        default='both', help='输出格式')
    
    args = parser.parse_args()
    
    if args.format == 'filename':
        print(generate_filename(args.task_type, args.module_name, args.date))
    elif args.format == 'title':
        print(generate_lark_title(args.task_type, args.module_name, args.date))
    else:
        print(f"文件名: {generate_filename(args.task_type, args.module_name, args.date)}")
        print(f"飞书标题: {generate_lark_title(args.task_type, args.module_name, args.date)}")


if __name__ == '__main__':
    main()
