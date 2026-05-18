#!/usr/bin/env python3
"""
任务类型分类器 - 根据用户输入自动识别任务类型
"""

import argparse
import re
from typing import Tuple, Optional


# 重构任务关键词
REFACTORING_KEYWORDS = [
    '重构', 'refactor', 'refactoring',
    '优化', 'optimization', 'optimize',
    '迁移', 'migration', 'migrate',
    '升级', 'upgrade',
    '改造', 'transform',
    '重写', 'rewrite',
    '改写', 'restructure',
    '性能优化', '代码优化', '结构优化',
    '清理', 'cleanup', 'clean up',
    '整理', 'reorganize'
]

# 新需求任务关键词
NEW_FEATURE_KEYWORDS = [
    '新需求', 'new feature', 'feature',
    '新增', '新增功能', 'add',
    '开发', 'develop', 'development',
    '实现', 'implement', 'implementation',
    '添加功能', '添加',
    '创建', 'create',
    '构建', 'build',
    '需求完成', '功能完成',
    '新功能', '新模块'
]


def classify_task(text: str) -> Tuple[str, float, str]:
    """
    根据输入文本分类任务类型
    
    Args:
        text: 用户输入文本
    
    Returns:
        (任务类型, 置信度, 匹配到的关键词)
    """
    text_lower = text.lower()
    
    refactoring_score = 0
    new_feature_score = 0
    matched_refactor_keyword = ""
    matched_feature_keyword = ""
    
    # 检查重构关键词
    for keyword in REFACTORING_KEYWORDS:
        if keyword.lower() in text_lower:
            refactoring_score += 1
            if not matched_refactor_keyword:
                matched_refactor_keyword = keyword
    
    # 检查新需求关键词
    for keyword in NEW_FEATURE_KEYWORDS:
        if keyword.lower() in text_lower:
            new_feature_score += 1
            if not matched_feature_keyword:
                matched_feature_keyword = keyword
    
    # 判断任务类型
    if refactoring_score > new_feature_score:
        confidence = min(refactoring_score / 2, 1.0)
        return '重构', confidence, matched_refactor_keyword
    elif new_feature_score > refactoring_score:
        confidence = min(new_feature_score / 2, 1.0)
        return '新需求', confidence, matched_feature_keyword
    else:
        # 无法确定，返回未知
        return '未知', 0.0, ""


def extract_module_name(text: str) -> Optional[str]:
    """
    尝试从文本中提取模块/页面名称
    
    Args:
        text: 用户输入文本
    
    Returns:
        提取的模块名称，如果无法提取则返回 None
    """
    # 常见模式匹配
    patterns = [
        r'([\\u4e00-\\u9fa5]+(?:页面|模块|功能|组件|接口|系统))',  # 中文页面/模块/功能
        r'(\\w+(?:Page|Module|Component|Feature|API))',  # 英文页面/模块
        r'["\\']([^"\\']+)["\\']',  # 引号中的内容
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return None


def main():
    parser = argparse.ArgumentParser(description='任务类型分类器')
    parser.add_argument('text', help='用户输入文本')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    task_type, confidence, keyword = classify_task(args.text)
    module_name = extract_module_name(args.text)
    
    if args.verbose:
        print(f"输入文本: {args.text}")
        print(f"任务类型: {task_type}")
        print(f"置信度: {confidence:.2%}")
        print(f"匹配关键词: {keyword}")
        if module_name:
            print(f"提取模块名: {module_name}")
        else:
            print("提取模块名: 未识别")
    else:
        print(task_type)


if __name__ == '__main__':
    main()
