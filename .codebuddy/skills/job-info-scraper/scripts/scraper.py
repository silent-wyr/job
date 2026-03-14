#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
job-info-scraper — 真实岗位搜索脚本

工作方式：
  由 WorkBuddy AI 调用 web_search / web_fetch 工具搜索真实招聘信息，
  AI 在搜索阶段直接按筛选条件过滤，只保留匹配岗位，
  最终将结果追加写入带时间戳的 CSV 文件（不覆盖历史）。

使用方式：
  直接在 WorkBuddy 对话框输入"更新实习岗位"或"更新本周实习岗位"，
  AI 会自动执行完整工作流，无需手动运行本脚本。

手动运行（仅用于测试 CSV 读写逻辑）：
  python scraper.py --mode today   # 今日新岗位
  python scraper.py --mode week    # 本周新岗位
  python scraper.py --demo         # 使用内置演示数据测试输出
"""

import os
import csv
import json
import argparse
from datetime import datetime

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # job-info-scraper/
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
CONFIG_PATH = os.path.join(BASE_DIR, 'assets', 'config', 'filter_rules.json')

# CSV 列定义（与 run_all.py 保持一致）
CSV_HEADERS = [
    '公司名称', '优先级', '岗位名称', '岗位类型', '工作地点',
    '学历要求', '毕业年份', '每周最少工作天数', '实习类型', '实习时长',
    '工作职责', '技能要求', '匹配分数', '发布日期', '投递邮箱',
    '数据来源', '原始链接'
]

# ─────────────────────────────────────────────
# AI 执行工作流时的搜索策略配置
# （供 AI 读取，了解应该搜索哪些关键词和平台）
# ─────────────────────────────────────────────
SEARCH_STRATEGY = {
    "description": "AI 执行搜索时的策略配置，所有搜索均需包含筛选条件",

    # 搜索关键词组合（每组独立搜索）
    "search_queries": {
        "today": [
            "音乐运营 实习生 北京 2026",
            "活动策划 实习 北京 音乐",
            "经纪助理 实习 北京",
            "新媒体运营 实习生 北京 音乐",
            "演出策划 实习 北京",
            "演出统筹 实习生 北京",
            "音乐内容运营 实习 北京 site:shixiseng.com OR site:zhipin.com",
        ],
        "week": [
            "音乐运营 实习生 北京 本周",
            "活动策划 实习 北京 音乐 近期",
            "经纪助理 实习 北京 招聘",
            "新媒体运营 实习生 北京 音乐公司",
            "演出策划 实习 北京 招聘",
            "腾讯音乐 实习生 招聘 北京",
            "字节跳动 音乐 实习生 北京",
            "网易云音乐 实习生 北京",
            "索尼音乐 实习生 北京",
            "环球音乐 实习生 北京",
            "摩登天空 实习生 北京",
            "太合音乐 实习生 北京",
        ]
    },

    # 精准筛选条件（AI 在整理每条结果时逐项核验）
    "filter_criteria": {
        "must_match": [
            "工作地点包含'北京'",
            "岗位类型为实习（非全职/社招/正职/应届生正职）",
            "岗位内容与音乐行业相关（运营/策划/经纪/宣传/演出/新媒体）",
        ],
        "should_match": [
            "学历要求为本科或不限",
            "毕业年份为2028届或不限",
            "每周工作天数>=3天",
        ],
        "must_exclude": [
            "全职", "社招", "正职", "正式员工", "校招全职",
            "暑期实习",  # 排除暑期岗位
        ]
    },

    # 目标公司优先级（P0最高，搜索时优先覆盖）
    "priority_companies": {
        "P0": ["腾讯音乐", "QQ音乐", "酷狗", "字节跳动", "抖音", "网易云音乐"],
        "P1": ["索尼音乐", "环球音乐", "华纳音乐"],
        "P2": ["太合音乐", "摩登天空", "风华秋实", "滚石唱片", "种梦音乐"],
        "P3": ["吴氏策划", "保利剧院", "无限星空音乐", "雨乐音乐", "九天星韵"]
    },

    # 数据来源平台（在搜索结果中注明）
    "platforms": ["实习僧", "BOSS直聘", "小红书", "微信公众号", "官网", "猎聘", "拉勾网"]
}

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def load_filter_rules():
    """加载筛选规则配置"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_company_priority(company_name: str, rules: dict) -> str:
    """根据公司名称返回优先级"""
    for pri, companies in rules.get('company_priorities', {}).items():
        if any(c in company_name for c in companies):
            return pri
    return 'P3'


def calc_match_score(job: dict, rules: dict) -> int:
    """计算匹配分数"""
    score = 0
    sr = rules.get('scoring_rules', {})
    bf = rules.get('basic_filters', {})

    # 公司优先级加分
    priority = job.get('priority', 'P3')
    score += sr.get(f'{priority}_company', 0)

    # 明确2028届
    if '2028' in str(job.get('graduation_year', '')):
        score += sr.get('explicit_2028', 0)

    # 工作天数打分：公司要求天数越少越友好，分越高
    # 自己每周最多能实习3天，公司要求越少越容易满足
    wd = job.get('min_work_days_per_week')
    if wd is not None:
        if wd <= 3:
            score += sr.get('work_days_3_or_less', 5)   # 3天及以下：最友好
        elif wd == 4:
            score += sr.get('work_days_4', 2)            # 4天：勉强可以协商
        else:
            score += sr.get('work_days_5_or_more', 0)   # 5天及以上：无法满足，不加分

    # 描述关键词加分
    desc = (job.get('description', '') + job.get('job_responsibilities', '') +
            job.get('skill_requirements', ''))
    if '音乐专业' in desc or '音乐相关' in desc:
        score += sr.get('music_major_preferred', 0)
    exp_kw = ['活动策划', '演出', '宣传', '舞台监督', '音乐节']
    if any(k in desc for k in exp_kw):
        score += sr.get('relevant_experience', 0)

    return score


def normalize_job(raw: dict, rules: dict) -> dict:
    """
    将 AI 整理的原始字段标准化为 CSV 列格式。
    AI 输出的字段名可能不统一，这里做兼容映射。
    """
    company_name = raw.get('company_name') or raw.get('company') or ''
    priority = get_company_priority(company_name, rules)

    job = {
        'company_name': company_name,
        'priority': priority,
        'position_title': raw.get('position_title') or raw.get('title') or '',
        'position_type': raw.get('position_type') or raw.get('type') or '其他',
        'location': raw.get('location') or '北京',
        'education': raw.get('education') or '不限',
        'graduation_year': str(raw.get('graduation_year') or '不限'),
        'min_work_days_per_week': raw.get('min_work_days_per_week') or raw.get('work_days') or 3,
        'internship_type': raw.get('internship_type') or '日常实习',
        'internship_duration': raw.get('internship_duration') or raw.get('duration') or '',
        'job_responsibilities': raw.get('job_responsibilities') or raw.get('responsibilities') or '',
        'skill_requirements': raw.get('skill_requirements') or raw.get('requirements') or '',
        'publish_date': raw.get('publish_date') or datetime.now().strftime('%Y-%m-%d'),
        'application_email': raw.get('application_email') or raw.get('email') or '',
        'source': raw.get('source') or raw.get('platform') or '',
        'source_url': raw.get('source_url') or raw.get('url') or '',
        'description': raw.get('description') or '',
    }

    job['match_score'] = calc_match_score(job, rules)
    return job


def is_duplicate(job: dict, existing_jobs: list) -> bool:
    """
    去重检查：同公司 + 相似岗位名 视为重复
    （宽松匹配，只要公司相同且职位名有50%以上字符重叠即认为重复）
    """
    from difflib import SequenceMatcher
    for e in existing_jobs:
        if e.get('公司名称') != job.get('company_name'):
            continue
        ratio = SequenceMatcher(
            None,
            e.get('岗位名称', ''),
            job.get('position_title', '')
        ).ratio()
        if ratio > 0.5:
            return True
    return False


def load_existing_csv(csv_path: str) -> list:
    """读取已有 CSV，返回行列表（用于去重判断）"""
    if not os.path.exists(csv_path):
        return []
    rows = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def append_to_csv(jobs: list, csv_path: str) -> tuple:
    """
    将新岗位追加到 CSV（如文件不存在则新建）。
    返回 (写入数量, 跳过数量)
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    existing = load_existing_csv(csv_path)

    written = 0
    skipped = 0
    file_exists = os.path.exists(csv_path)

    with open(csv_path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()

        for job in jobs:
            if is_duplicate(job, existing):
                skipped += 1
                continue
            writer.writerow({
                '公司名称': job['company_name'],
                '优先级': job['priority'],
                '岗位名称': job['position_title'],
                '岗位类型': job['position_type'],
                '工作地点': job['location'],
                '学历要求': job['education'],
                '毕业年份': job['graduation_year'],
                '每周最少工作天数': job['min_work_days_per_week'],
                '实习类型': job['internship_type'],
                '实习时长': job['internship_duration'],
                '工作职责': job['job_responsibilities'],
                '技能要求': job['skill_requirements'],
                '匹配分数': job['match_score'],
                '发布日期': job['publish_date'],
                '投递邮箱': job['application_email'],
                '数据来源': job['source'],
                '原始链接': job['source_url'],
            })
            # 同步加入 existing 列表，防止同批次数据内部重复
            existing.append({
                '公司名称': job['company_name'],
                '岗位名称': job['position_title'],
            })
            written += 1

    return written, skipped


def write_new_csv(jobs: list) -> str:
    """
    将本次搜索结果写入新的带时间戳 CSV 文件（不覆盖历史）。
    文件名格式：job_results_YYYYMMDD_HHMMSS.csv
    """
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_path = os.path.join(OUTPUT_DIR, f'job_results_{ts}.csv')
    written, skipped = append_to_csv(jobs, csv_path)
    return csv_path, written, skipped


def get_latest_csv() -> str:
    """返回 output 目录下最新的 CSV 文件路径，不存在则返回 None"""
    if not os.path.exists(OUTPUT_DIR):
        return None
    files = [f for f in os.listdir(OUTPUT_DIR)
             if f.startswith('job_results_') and f.endswith('.csv')]
    if not files:
        return None
    files.sort(reverse=True)  # 按文件名倒序，最新的在前
    return os.path.join(OUTPUT_DIR, files[0])


# ─────────────────────────────────────────────
# AI 调用入口（由 WorkBuddy AI 在工作流中调用）
# ─────────────────────────────────────────────

def process_ai_results(raw_jobs: list) -> str:
    """
    接收 AI 整理好的岗位列表，标准化后写入新 CSV。

    参数：
        raw_jobs: AI 整理的岗位字典列表，字段见 normalize_job() 中的映射

    返回：
        生成的 CSV 文件路径
    """
    rules = load_filter_rules()
    normalized = [normalize_job(job, rules) for job in raw_jobs]
    csv_path, written, skipped = write_new_csv(normalized)

    print(f"[scraper] 本次处理: {len(raw_jobs)} 条")
    print(f"[scraper] 写入CSV: {written} 条  跳过重复: {skipped} 条")
    print(f"[scraper] 输出文件: {csv_path}")

    return csv_path


# ─────────────────────────────────────────────
# 演示模式（手动测试用）
# ─────────────────────────────────────────────

DEMO_JOBS = [
    {
        'company_name': '腾讯音乐',
        'position_title': '音乐运营实习生',
        'position_type': '音乐运营',
        'location': '北京',
        'education': '本科及以上',
        'graduation_year': '2028',
        'min_work_days_per_week': 3,
        'internship_type': '日常实习',
        'internship_duration': '3个月以上',
        'job_responsibilities': '协助团队进行音乐内容运营；挖掘优质音乐内容；参与活动策划和执行',
        'skill_requirements': '热爱音乐；本科在读，音乐相关专业优先；每周可实习至少3天',
        'publish_date': datetime.now().strftime('%Y-%m-%d'),
        'application_email': 'hr@tencent.com',
        'source': '实习僧',
        'source_url': 'https://www.shixiseng.com/intern/xxx',
        'description': '负责音乐内容运营，活动策划，需要音乐相关专业优先',
    },
    {
        'company_name': '摩登天空',
        'position_title': '演出项目助理实习生',
        'position_type': '演出策划',
        'location': '北京',
        'education': '本科',
        'graduation_year': '不限',
        'min_work_days_per_week': 4,
        'internship_type': '日常实习',
        'internship_duration': '6个月',
        'job_responsibilities': '协助项目经理进行演出项目管理；跟进演出合同及资料整理',
        'skill_requirements': '有活动/演出执行经验优先；善于沟通协调',
        'publish_date': datetime.now().strftime('%Y-%m-%d'),
        'application_email': '',
        'source': 'BOSS直聘',
        'source_url': 'https://www.zhipin.com/job/xxx',
        'description': '协助演出策划执行，演出运营，项目助理',
    },
]


def main():
    parser = argparse.ArgumentParser(description='job-info-scraper 手动测试工具')
    parser.add_argument('--demo', action='store_true', help='使用演示数据测试输出')
    parser.add_argument('--mode', choices=['today', 'week'], default='today',
                        help='搜索模式：today=今日，week=本周')
    parser.add_argument('--show-strategy', action='store_true',
                        help='打印搜索策略配置（供 AI 参考）')
    args = parser.parse_args()

    if args.show_strategy:
        print(json.dumps(SEARCH_STRATEGY, ensure_ascii=False, indent=2))
        return

    if args.demo:
        print("[demo] 使用演示数据测试 CSV 输出...")
        csv_path = process_ai_results(DEMO_JOBS)
        print(f"[demo] 测试完成，请检查文件: {csv_path}")
        return

    # 非演示模式：打印搜索策略，提示 AI 执行
    print(f"[scraper] 搜索模式: {args.mode}")
    print("[scraper] 本脚本由 WorkBuddy AI 调用，请在对话框输入'更新实习岗位'触发完整工作流")
    print("[scraper] 如需查看搜索策略配置，运行: python scraper.py --show-strategy")


if __name__ == '__main__':
    main()
