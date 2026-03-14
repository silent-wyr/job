#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job Info Parser - 招聘信息解析脚本

这个脚本从原始文本中提取结构化的招聘信息，包括：
- 公司名称
- 岗位名称
- 工作地点
- 学历要求
- 毕业年份
- 每周最少工作天数
- 实习类型
- 工作职责
- 技能要求
"""

import json
import re
from typing import Dict, Optional, List


class JobParser:
    """招聘信息解析器"""

    def __init__(self, target_companies_path: str = "assets/config/target_companies.json"):
        """初始化解析器

        Args:
            target_companies_path: 目标公司配置文件路径
        """
        with open(target_companies_path, 'r', encoding='utf-8') as f:
            companies_data = json.load(f)
        self.companies = {c['name']: c for c in companies_data['companies']}
        self.company_aliases = {}
        for company in companies_data['companies']:
            for alias in company.get('aliases', []):
                self.company_aliases[alias] = company['name']

    def parse_job(self, text: str, source: str = "") -> Dict:
        """解析招聘信息文本

        Args:
            text: 招聘信息文本
            source: 数据来源

        Returns:
            结构化的职位信息字典
        """
        job = {
            'company': self._extract_company(text),
            'position_title': self._extract_position_title(text),
            'location': self._extract_location(text),
            'education': self._extract_education(text),
            'graduation_year': self._extract_graduation_year(text),
            'min_work_days_per_week': self._extract_work_days(text),
            'internship_type': self._extract_internship_type(text),
            'internship_duration': self._extract_internship_duration(text),
            'description': text,
            'job_responsibilities': self._extract_job_responsibilities(text),
            'skill_requirements': self._extract_skill_requirements(text),
            'source': source
        }
        return job

    def _extract_company(self, text: str) -> Dict:
        """提取公司信息

        Args:
            text: 招聘文本

        Returns:
            公司信息字典，包含名称和优先级
        """
        # 先尝试直接匹配公司名
        for company_name, company_info in self.companies.items():
            if company_name in text:
                return {
                    'name': company_name,
                    'priority': company_info['priority'],
                    'aliases': company_info.get('aliases', [])
                }

        # 尝试匹配别名
        for alias, company_name in self.company_aliases.items():
            if alias in text:
                company_info = self.companies[company_name]
                return {
                    'name': company_name,
                    'priority': company_info['priority'],
                    'aliases': company_info.get('aliases', [])
                }

        return {'name': '未知公司', 'priority': 'P3', 'aliases': []}

    def _extract_position_title(self, text: str) -> str:
        """提取岗位名称

        Args:
            text: 招聘文本

        Returns:
            岗位名称
        """
        # 常见岗位标题模式
        patterns = [
            r'岗位[:：]\s*([^\n，。]+)',
            r'职位[:：]\s*([^\n，。]+)',
            r'招聘[:：]\s*([^\n，。]+)',
            r'^(.+?)实习生',  # "XXX实习生"格式
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        return "未知岗位"

    def _extract_location(self, text: str) -> str:
        """提取工作地点

        Args:
            text: 招聘文本

        Returns:
            工作地点
        """
        # 常见地点模式
        patterns = [
            r'工作地点[:：]\s*([^\n，。]+)',
            r'地点[:：]\s*([^\n，。]+)',
            r'工作城市[:：]\s*([^\n，。]+)',
            r'地点[:：]\s*([北京上海广州深圳]+)',
            r'\[([北京上海广州深圳]+)\]',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        # 查找城市名
        cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉']
        for city in cities:
            if city in text:
                return city

        return "未知地点"

    def _extract_education(self, text: str) -> str:
        """提取学历要求

        Args:
            text: 招聘文本

        Returns:
            学历要求
        """
        patterns = [
            r'学历要求[:：]\s*([^\n，。]+)',
            r'学历[:：]\s*([^\n，。]+)',
            r'要求[:：]\s*([^\n，。]*?本科[^\n，。]*)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        # 检查是否提到学历
        if '本科' in text or '大学' in text:
            return "本科"
        elif '硕士' in text:
            return "硕士"
        elif '不限' in text:
            return "不限"

        return "未知"

    def _extract_graduation_year(self, text: str) -> Optional[str]:
        """提取毕业年份要求

        Args:
            text: 招聘文本

        Returns:
            毕业年份，如 "2028"
        """
        # 匹配毕业年份
        patterns = [
            r'(\d{4})届',
            r'毕业年份[:：]\s*(\d{4})',
            r'(\d{4})年毕业',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return None

    def _extract_work_days(self, text: str) -> Optional[int]:
        """提取每周最少工作天数

        Args:
            text: 招聘文本

        Returns:
            每周最少工作天数，如 3
        """
        patterns = [
            r'每周至少\s*(\d+)\s*天',
            r'每周不少于\s*(\d+)\s*天',
            r'每周(\d+)天以上',
            r'每周\s*(\d+)\s*天',
            r'每周(\d+)天',
            r'至少(\d+)天',
            r'全勤(\d+)天',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))

        return None

    def _extract_job_responsibilities(self, text: str) -> Optional[str]:
        """提取工作职责

        Args:
            text: 招聘文本

        Returns:
            工作职责文本（条目以"；"分隔），若未提取到则返回 None
        """
        # 匹配"岗位职责"/"工作职责"/"主要职责"段落
        patterns = [
            r'(?:岗位职责|工作职责|主要职责|职责描述)[:：]\s*((?:.|\n)+?)(?=任职要求|技能要求|岗位要求|\n\n|$)',
            r'(?:岗位职责|工作职责|主要职责)[:：]?\n((?:\d+[.、．]?.+\n?)+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                raw = match.group(1).strip()
                # 去掉行首序号，合并成分号分隔的字符串
                lines = [re.sub(r'^\d+[.、．\s]+', '', l).strip() for l in raw.splitlines() if l.strip()]
                return '；'.join(lines)
        return None

    def _extract_skill_requirements(self, text: str) -> Optional[str]:
        """提取技能要求

        Args:
            text: 招聘文本

        Returns:
            技能要求文本（条目以"；"分隔），若未提取到则返回 None
        """
        patterns = [
            r'(?:任职要求|岗位要求|技能要求|资质要求)[:：]\s*((?:.|\n)+?)(?=岗位职责|工作职责|\n\n|$)',
            r'(?:任职要求|岗位要求|技能要求)[:：]?\n((?:\d+[.、．]?.+\n?)+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                raw = match.group(1).strip()
                lines = [re.sub(r'^\d+[.、．\s]+', '', l).strip() for l in raw.splitlines() if l.strip()]
                return '；'.join(lines)
        return None

    def _extract_internship_type(self, text: str) -> str:
        """提取实习类型

        Args:
            text: 招聘文本

        Returns:
            实习类型："日常实习" 或 "暑期实习"
        """
        if '日常实习' in text or '长期实习' in text:
            return "日常实习"
        elif '暑期实习' in text or '暑假实习' in text:
            return "暑期实习"
        elif '实习' in text:
            return "日常实习"  # 默认为日常实习

        return "未知"

    def _extract_internship_duration(self, text: str) -> Optional[str]:
        """提取实习时长

        Args:
            text: 招聘文本

        Returns:
            实习时长，如 "3个月"
        """
        patterns = [
            r'实习时长[:：]\s*([^\n，。]+)',
            r'实习(\d+)\s*个月',
            r'至少实习(\d+)\s*个月',
            r'(\d+)个月以上',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        return None


def main():
    """主函数示例"""
    parser = JobParser()

    # 示例招聘文本
    sample_text = """
    【腾讯音乐-音乐运营实习生】
    工作地点：北京
    学历要求：本科及以上
    毕业年份：2025届、2026届、2027届、2028届均可
    每周工作：每周4天
    实习时长：至少3个月
    实习类型：日常实习

    岗位职责：
    1. 协助团队进行音乐内容运营
    2. 挖掘优质音乐内容
    3. 参与活动策划和执行

    任职要求：
    1. 热爱音乐，对音乐有敏锐度
    2. 本科在读，音乐相关专业优先
    3. 每周可实习4天，持续3个月以上
    """

    # 解析职位
    job = parser.parse_job(sample_text, source="微信公众号")

    # 输出结果
    print(json.dumps(job, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
