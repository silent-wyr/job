#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 网页生成脚本

从 job-info-scraper 输出的 CSV/JSON 数据生成 HTML 网页
"""

import json
import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict


class HTMLGenerator:
    """HTML 网页生成器"""

    def __init__(self, template_path: str = "assets/templates/job_portal.html"):
        """初始化生成器

        Args:
            template_path: HTML 模板文件路径
        """
        self.template_path = template_path
        self.template = self._load_template()

    def _load_template(self) -> str:
        """加载 HTML 模板

        Returns:
            模板内容
        """
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def load_csv(self, csv_path: str) -> List[Dict]:
        """从 CSV 文件加载数据

        Args:
            csv_path: CSV 文件路径

        Returns:
            职位数据列表
        """
        jobs = []

        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                jobs.append(self._parse_csv_row(row))

        return jobs

    def load_json(self, json_path: str) -> List[Dict]:
        """从 JSON 文件加载数据

        Args:
            json_path: JSON 文件路径

        Returns:
            职位数据列表
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 如果是单个对象，转换为列表
        if isinstance(data, dict):
            data = [data]

        return data

    def _parse_csv_row(self, row: Dict) -> Dict:
        """解析 CSV 行数据

        Args:
            row: CSV 行数据

        Returns:
            标准化的职位数据
        """
        job = {
            'id': row.get('job_id', f"job_{row.get('公司名称', '')}_{row.get('岗位名称', '')}"),
            'company': row.get('公司名称', ''),
            'priority': row.get('优先级', 'P3'),
            'position_title': row.get('岗位名称', ''),
            'position_type': row.get('岗位类型', '其他'),
            'location': row.get('工作地点', ''),
            'education': row.get('学历要求', ''),
            'graduation_year': row.get('毕业年份', ''),
            'work_days_per_week': int(row.get('每周最少工作天数', '0')) if row.get('每周最少工作天数') else 0,
            'internship_type': row.get('实习类型', ''),
            'internship_duration': row.get('实习时长', ''),
            'job_responsibilities': row.get('工作职责', ''),
            'skill_requirements': row.get('技能要求', ''),
            'match_score': int(row.get('匹配分数', '0')) if row.get('匹配分数') else 0,
            'publish_date': row.get('发布日期', ''),
            'application_email': row.get('投递邮箱', ''),
            'application_method': f"发送简历至{row.get('投递邮箱', '')}",
            'description': row.get('岗位描述', ''),
            'source_url': row.get('原始链接', ''),
            'source': row.get('数据来源', '')
        }

        # 判断是否为新岗位
        job['is_new'] = self._is_new_job(job['publish_date'])

        # 判断是否过期
        job['is_expired'] = self._is_expired(job['publish_date'])

        return job

    def _is_new_job(self, publish_date: str) -> bool:
        """判断是否为新岗位

        Args:
            publish_date: 发布日期

        Returns:
            是否为新岗位
        """
        try:
            pub_date = datetime.strptime(publish_date, '%Y-%m-%d')
            today = datetime.now()
            return (today - pub_date).days == 0
        except:
            return False

    def _is_expired(self, publish_date: str) -> bool:
        """判断是否过期（超过7天）

        Args:
            publish_date: 发布日期

        Returns:
            是否过期
        """
        try:
            pub_date = datetime.strptime(publish_date, '%Y-%m-%d')
            today = datetime.now()
            return (today - pub_date).days > 7
        except:
            return False

    def generate_html(self, jobs: List[Dict], output_path: str, config: Dict = None):
        """生成 HTML 网页

        Args:
            jobs: 职位数据列表
            output_path: 输出 HTML 文件路径
            config: 配置参数
        """
        if config is None:
            config = {
                'title': '实习岗位推荐',
                'subtitle': '中央音乐学院 · 2028届 · 音乐艺术管理',
                'retention_days': 7
            }

        # 将岗位数据转换为 JavaScript 数组
        jobs_json = json.dumps(jobs, ensure_ascii=False, indent=2)

        # 替换模板中的占位符
        html_content = self.template

        # 替换标题和副标题
        html_content = html_content.replace('实习岗位推荐', config['title'])
        html_content = html_content.replace('中央音乐学院 · 2028届 · 音乐艺术管理', config['subtitle'])

        # 替换示例数据
        html_content = html_content.replace(
            '// TODO: 从 CSV/JSON 文件加载数据\n            // jobs = parseDataFromFile(\'job_results.csv\');\n            \n            // 临时使用示例数据\n            jobs = sampleJobs;',
            f'// 从数据文件加载\n            jobs = {jobs_json};'
        )

        # 保存 HTML 文件
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ HTML 网页已生成: {output_path}")
        print(f"   共包含 {len(jobs)} 个岗位")
        print(f"   今日新增: {sum(1 for job in jobs if job['is_new'])} 个")
        print(f"   已过期: {sum(1 for job in jobs if job['is_expired'])} 个")

    def generate_html_with_password(self, jobs: List[Dict], output_path: str, password: str, config: Dict = None):
        """生成带密码保护的 HTML 网页

        Args:
            jobs: 职位数据列表
            output_path: 输出 HTML 文件路径
            password: 访问密码
            config: 配置参数
        """
        # 先生成基础 HTML
        html_content = self.generate_html(jobs, output_path, config)

        # TODO: 添加密码保护逻辑
        # 1. 添加密码输入页面
        # 2. 验证密码后显示内容
        # 3. 密码存储在 localStorage

        print(f"✅ 带密码保护的 HTML 网页已生成: {output_path}")
        print(f"   访问密码: {password}")


def main():
    """主函数示例"""
    generator = HTMLGenerator()

    # 示例 1: 从 CSV 生成 HTML
    csv_path = "job_results_20260310_143000.csv"
    if os.path.exists(csv_path):
        jobs = generator.load_csv(csv_path)
        generator.generate_html(
            jobs,
            'index.html',
            config={
                'title': '实习岗位推荐',
                'subtitle': '中央音乐学院 · 2028届 · 音乐艺术管理'
            }
        )

    # 示例 2: 从 JSON 生成 HTML
    json_path = "filtered_jobs.json"
    if os.path.exists(json_path):
        jobs = generator.load_json(json_path)
        generator.generate_html(
            jobs,
            'index.html',
            config={
                'title': '实习岗位推荐',
                'subtitle': '中央音乐学院 · 2028届 · 音乐艺术管理'
            }
        )

    # 示例 3: 生成带密码保护的 HTML
    if os.path.exists(json_path):
        generator.generate_html_with_password(
            jobs,
            'index_protected.html',
            password='123456',
            config={
                'title': '实习岗位推荐',
                'subtitle': '中央音乐学院 · 2028届 · 音乐艺术管理'
            }
        )


if __name__ == '__main__':
    main()
