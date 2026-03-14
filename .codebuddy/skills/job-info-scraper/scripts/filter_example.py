#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job Filter - 招聘信息筛选脚本

这个脚本根据预设规则筛选和排序招聘信息：
1. 应用硬性筛选条件
2. 计算匹配分数
3. 去重
4. 排序输出
"""

import json
import re
from typing import List, Dict, Optional
from difflib import SequenceMatcher


class JobFilter:
    """招聘信息筛选器"""

    def __init__(self, filter_rules_path: str = "assets/config/filter_rules.json"):
        """初始化筛选器

        Args:
            filter_rules_path: 筛选规则配置文件路径
        """
        with open(filter_rules_path, 'r', encoding='utf-8') as f:
            self.rules = json.load(f)

    def filter_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """筛选职位列表

        Args:
            jobs: 职位列表

        Returns:
            筛选后的职位列表
        """
        filtered = []

        for job in jobs:
            # 应用硬性筛选
            if not self._check_basic_filters(job):
                continue

            # 计算匹配分数
            job['match_score'] = self._calculate_match_score(job)
            job['matched_keywords'] = self._get_matched_keywords(job['description'])
            job['meets_basic_requirements'] = True

            filtered.append(job)

        # 去重
        filtered = self._deduplicate(filtered)

        # 按分数排序
        filtered.sort(key=lambda x: x['match_score'], reverse=True)

        return filtered

    def _check_basic_filters(self, job: Dict) -> bool:
        """检查基本筛选条件

        Args:
            job: 职位信息

        Returns:
            是否满足所有基本条件
        """
        # 1. 检查工作地点
        location = job.get('location', '')
        if not any(loc in location for loc in self.rules['basic_filters']['location']):
            return False

        # 2. 检查实习类型
        internship_type = job.get('internship_type', '')
        if internship_type == "暑期实习":
            return False

        # 3. 检查学历要求
        education = job.get('education', '')
        allowed_education = self.rules['basic_filters']['education']
        if not any(edu in education for edu in allowed_education):
            return False

        # 4. 检查毕业年份
        grad_year = job.get('graduation_year')
        allowed_years = self.rules['basic_filters']['graduation_year']
        if grad_year and not any(year in str(grad_year) for year in allowed_years):
            return False

        # 5. 检查工作天数（岗位要求的最少工作天数需满足学生可投入的天数）
        work_days = job.get('min_work_days_per_week')
        min_days = self.rules['basic_filters']['min_work_days_per_week']
        if work_days and work_days < min_days:
            return False

        # 6. 检查岗位关键词
        description = job.get('description', '')
        required_keywords = self.rules['keywords']['required']
        if not any(keyword in description for keyword in required_keywords):
            return False

        # 7. 排除全职等关键词
        exclude_keywords = self.rules.get('exclude_keywords', [])
        if any(keyword in description for keyword in exclude_keywords):
            return False

        return True

    def _calculate_match_score(self, job: Dict) -> int:
        """计算匹配分数

        Args:
            job: 职位信息

        Returns:
            匹配分数
        """
        score = 0
        company_info = job.get('company', {})
        company_name = company_info.get('name', '')

        # 公司优先级得分
        priorities = self.rules['company_priorities']
        for priority, companies in priorities.items():
            if any(company in company_name for company in companies):
                score += self.rules['scoring_rules'].get(f'{priority}_company', 0)
                break

        # 明确招收2028届
        grad_year = str(job.get('graduation_year', ''))
        if '2028' in grad_year:
            score += self.rules['scoring_rules']['explicit_2028']

        # 每周工作天数满足最少要求
        work_days = job.get('min_work_days_per_week')
        min_days = self.rules['basic_filters']['min_work_days_per_week']
        if work_days and work_days >= min_days:
            score += self.rules['scoring_rules']['work_days_meets_min']

        # 音乐专业优先
        description = job.get('description', '')
        if '音乐专业' in description or '音乐相关' in description:
            score += self.rules['scoring_rules']['music_major_preferred']

        # 相关经验
        experience_keywords = ['活动策划', '演出', '宣传', '舞台监督', '音乐节']
        if any(keyword in description for keyword in experience_keywords):
            score += self.rules['scoring_rules']['relevant_experience']

        return score

    def _get_matched_keywords(self, description: str) -> List[str]:
        """获取匹配的关键词

        Args:
            description: 岗位描述

        Returns:
            匹配的关键词列表
        """
        matched = []
        required_keywords = self.rules['keywords']['required']
        optional_keywords = self.rules['keywords']['optional']

        for keyword in required_keywords:
            if keyword in description:
                matched.append(keyword)

        for keyword in optional_keywords:
            if keyword in description and keyword not in matched:
                matched.append(keyword)

        return matched

    def _deduplicate(self, jobs: List[Dict]) -> List[Dict]:
        """去重

        Args:
            jobs: 职位列表

        Returns:
            去重后的职位列表
        """
        seen = []
        unique_jobs = []

        for job in jobs:
            # 检查是否重复
            is_duplicate = False
            for seen_job in seen:
                if self._is_duplicate(job, seen_job):
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_jobs.append(job)
                seen.append(job)

        return unique_jobs

    def _is_duplicate(self, job1: Dict, job2: Dict) -> bool:
        """判断是否重复

        Args:
            job1: 职位1
            job2: 职位2

        Returns:
            是否重复
        """
        # 同一公司
        if job1.get('company', {}).get('name') != job2.get('company', {}).get('name'):
            return False

        # 相似岗位名称
        title1 = job1.get('position_title', '')
        title2 = job2.get('position_title', '')
        title_similarity = SequenceMatcher(None, title1, title2).ratio()

        # 描述相似度
        desc1 = job1.get('description', '')
        desc2 = job2.get('description', '')
        desc_similarity = SequenceMatcher(None, desc1, desc2).ratio()

        # 判断标准：同一公司 + 岗位相似度>0.7 + 描述相似度>0.8
        if title_similarity > 0.7 and desc_similarity > 0.8:
            return True

        return False

    def generate_summary(self, filtered_jobs: List[Dict]) -> str:
        """生成筛选结果摘要

        Args:
            filtered_jobs: 筛选后的职位列表

        Returns:
            摘要文本
        """
        summary = f"筛选结果摘要\n"
        summary += f"{'='*50}\n"
        summary += f"总计匹配岗位: {len(filtered_jobs)} 个\n\n"

        # 按优先级统计
        priority_count = {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0}
        for job in filtered_jobs:
            priority = job.get('company', {}).get('priority', 'P3')
            priority_count[priority] += 1

        summary += "优先级分布:\n"
        for priority, count in priority_count.items():
            if count > 0:
                summary += f"  {priority}: {count} 个\n"

        summary += f"\n\nTop 10 推荐岗位:\n"
        summary += f"{'-'*50}\n"

        for i, job in enumerate(filtered_jobs[:10], 1):
            company = job.get('company', {}).get('name', '未知')
            position = job.get('position_title', '未知')
            score = job.get('match_score', 0)
            location = job.get('location', '')

            summary += f"{i}. [{company}] {position} (分数: {score})\n"
            summary += f"   地点: {location}\n\n"

        return summary


def main():
    """主函数示例"""
    # 创建筛选器
    filter = JobFilter()

    # 示例职位数据
    sample_jobs = [
        {
            'company': {'name': '腾讯音乐', 'priority': 'P0'},
            'position_title': '音乐运营实习生',
            'location': '北京',
            'education': '本科及以上',
            'graduation_year': '2028',
            'min_work_days_per_week': 3,
            'internship_type': '日常实习',
            'description': '招聘音乐运营实习生，负责音乐内容运营和活动策划，需要音乐相关专业优先',
            'job_responsibilities': '协助音乐内容运营；挖掘优质内容；参与活动策划',
            'skill_requirements': '热爱音乐；音乐相关专业优先；良好沟通能力'
        },
        {
            'company': {'name': '索尼音乐', 'priority': 'P1'},
            'position_title': '演出策划实习生',
            'location': '上海',
            'education': '本科及以上',
            'graduation_year': '2028',
            'min_work_days_per_week': 4,
            'internship_type': '日常实习',
            'description': '招聘演出策划实习生，负责演出活动策划和执行',
            'job_responsibilities': '协助演出项目策划；对接场地及供应商；参与现场执行',
            'skill_requirements': '有活动策划经验优先；较强执行力；良好沟通能力'
        },
        {
            'company': {'name': '太合音乐', 'priority': 'P2'},
            'position_title': '音乐活动策划',
            'location': '北京',
            'education': '本科',
            'graduation_year': '2028',
            'min_work_days_per_week': 3,
            'internship_type': '日常实习',
            'description': '招聘音乐活动策划实习生，负责音乐节活动策划，需要音乐相关专业，有活动策划经验优先'
        }
    ]

    # 筛选职位
    filtered = filter.filter_jobs(sample_jobs)

    # 输出结果
    print(f"筛选后: {len(filtered)} 个职位\n")

    # 生成摘要
    summary = filter.generate_summary(filtered)
    print(summary)

    # 保存结果
    with open('filtered_jobs.json', 'w', encoding='utf-8') as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
