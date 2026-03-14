#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实习岗位工作流 — HTML 生成脚本

职责：读取 job-info-scraper 输出的最新 CSV → 生成 index.html

数据来源：
  .codebuddy/skills/job-info-scraper/output/job_results_*.csv（最新文件）

使用方式：
  - 推荐：在 WorkBuddy 对话框输入"更新实习岗位"，AI 自动完成搜索+写CSV+执行本脚本
  - 手动：python run_all.py
  - 指定 CSV：python run_all.py --csv path/to/file.csv
"""

import os
import csv
import sys
import json
import argparse
import subprocess
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRAPER_DIR = os.path.join(BASE_DIR, '.codebuddy', 'skills', 'job-info-scraper')
PUBLISHER_DIR = os.path.join(BASE_DIR, '.codebuddy', 'skills', 'job-info-publisher')
TEMPLATE_PATH = os.path.join(PUBLISHER_DIR, 'assets', 'templates', 'job_portal.html')
OUTPUT_DIR = os.path.join(SCRAPER_DIR, 'output')
HTML_OUTPUT = os.path.join(PUBLISHER_DIR, 'index.html')

# 过期天数（超过此天数的岗位标记为过期，灰色显示）
EXPIRY_DAYS = 15


# ─────────────────────────────────────────────
# CSV 读取
# ─────────────────────────────────────────────

def get_latest_csv() -> str:
    """返回 output 目录下最新的 CSV 文件路径"""
    if not os.path.exists(OUTPUT_DIR):
        return None
    files = [f for f in os.listdir(OUTPUT_DIR)
             if f.startswith('job_results_') and f.endswith('.csv')]
    if not files:
        return None
    files.sort(reverse=True)  # 文件名含时间戳，倒序即最新在前
    return os.path.join(OUTPUT_DIR, files[0])


def load_csv(csv_path: str) -> list:
    """读取 CSV，返回字典列表"""
    jobs = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            jobs.append(row)
    return jobs


def csv_row_to_job(row: dict) -> dict:
    """将 CSV 行转换为统一的岗位字典格式"""
    return {
        'company': {'name': row.get('公司名称', ''), 'priority': row.get('优先级', 'P3')},
        'position_title': row.get('岗位名称', ''),
        'position_type': row.get('岗位类型', '其他'),
        'location': row.get('工作地点', ''),
        'education': row.get('学历要求', ''),
        'graduation_year': row.get('毕业年份', ''),
        'min_work_days_per_week': _safe_int(row.get('每周最少工作天数'), 3),
        'internship_type': row.get('实习类型', ''),
        'internship_duration': row.get('实习时长', ''),
        'job_responsibilities': row.get('工作职责', ''),
        'skill_requirements': row.get('技能要求', ''),
        'match_score': _safe_int(row.get('匹配分数'), 0),
        'publish_date': row.get('发布日期', ''),
        'application_email': row.get('投递邮箱', ''),
        'source': row.get('数据来源', ''),
        'source_url': row.get('原始链接', ''),
        'description': row.get('工作职责', '') + ' ' + row.get('技能要求', ''),
    }


def _safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# ─────────────────────────────────────────────
# 时效判断
# ─────────────────────────────────────────────

def is_new(date_str: str) -> bool:
    """今日发布"""
    try:
        return (datetime.now() - datetime.strptime(date_str, '%Y-%m-%d')).days == 0
    except Exception:
        return False


def is_expired(date_str: str) -> bool:
    """超过 EXPIRY_DAYS 天视为过期"""
    try:
        return (datetime.now() - datetime.strptime(date_str, '%Y-%m-%d')).days > EXPIRY_DAYS
    except Exception:
        return False


# ─────────────────────────────────────────────
# HTML 生成
# ─────────────────────────────────────────────

def jobs_to_js_objects(jobs: list) -> list:
    result = []
    for i, job in enumerate(jobs):
        company = job.get('company', {})
        result.append({
            'id': f"job_{i+1:03d}",
            'company': company.get('name', ''),
            'priority': company.get('priority', 'P3'),
            'position_title': job.get('position_title', ''),
            'position_type': job.get('position_type', '其他'),
            'location': job.get('location', ''),
            'education': job.get('education', ''),
            'graduation_year': str(job.get('graduation_year', '')),
            'work_days_per_week': job.get('min_work_days_per_week', 0),
            'internship_type': job.get('internship_type', ''),
            'internship_duration': job.get('internship_duration', ''),
            'job_responsibilities': job.get('job_responsibilities', ''),
            'skill_requirements': job.get('skill_requirements', ''),
            'match_score': job.get('match_score', 0),
            'publish_date': job.get('publish_date', ''),
            'application_email': job.get('application_email', ''),
            'application_method': (
                f"发送简历至 {job.get('application_email', '')}"
                if job.get('application_email')
                else '请点击查看原文获取投递方式'
            ),
            'description': job.get('description', ''),
            'source_url': job.get('source_url', ''),
            'source': job.get('source', ''),
            'is_new': is_new(job.get('publish_date', '')),
            'is_expired': is_expired(job.get('publish_date', '')),
        })
    return result


def generate_html(jobs: list, template_path: str, output_path: str,
                  title: str = '实习岗位推荐',
                  subtitle: str = '中央音乐学院 · 2028届 · 音乐艺术管理'):
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    js_jobs = jobs_to_js_objects(jobs)
    jobs_json = json.dumps(js_jobs, ensure_ascii=False, indent=2)

    # 替换页面标题 / 副标题
    html = html.replace('实习岗位推荐', title, 2)
    html = html.replace('中央音乐学院 · 2028届 · 音乐艺术管理', subtitle, 1)

    # 将示例数据替换为真实数据
    html = html.replace(
        '// TODO: 从 CSV/JSON 文件加载数据\n            // jobs = parseDataFromFile(\'job_results.csv\');\n            \n            // 临时使用示例数据\n            jobs = sampleJobs;',
        f'// 数据已由 run_all.py 注入\n            jobs = {jobs_json};'
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path


# ─────────────────────────────────────────────
# Git 自动推送
# ─────────────────────────────────────────────

def git_push(repo_dir: str, html_src: str) -> bool:
    """
    将生成的 index.html 复制到仓库根目录，然后 git add / commit / push。
    返回 True 表示推送成功，False 表示跳过或失败。
    """
    import shutil

    dest_html = os.path.join(repo_dir, 'index.html')

    # 复制 index.html 到仓库根目录（GitHub Pages 读取根目录的 index.html）
    shutil.copy2(html_src, dest_html)

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    commit_msg = f'update: 实习岗位更新 {now_str}'

    try:
        # 检查是否有变动
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=repo_dir, capture_output=True, text=True
        )
        if not result.stdout.strip():
            print("      [SKIP] 内容无变化，无需推送")
            return True

        cmds = [
            ['git', 'add', 'index.html'],
            ['git', 'commit', '-m', commit_msg],
            ['git', 'push', 'origin', 'main'],
        ]
        for cmd in cmds:
            r = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"      [ERROR] {' '.join(cmd)} 失败:")
                print(f"              {r.stderr.strip()}")
                return False

        print(f"      [OK] 已推送到 GitHub，页面将在 1~2 分钟内更新")
        return True

    except FileNotFoundError:
        print("      [WARN] 未找到 git 命令，跳过自动推送")
        print("             请确认 Git 已安装并加入 PATH")
        return False
    except Exception as e:
        print(f"      [ERROR] 推送失败: {e}")
        return False


# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='实习岗位 HTML 生成工具')
    parser.add_argument('--csv', type=str, default=None,
                        help='指定 CSV 文件路径（默认使用最新文件）')
    parser.add_argument('--no-push', action='store_true',
                        help='跳过 git push（仅本地生成 HTML）')
    args = parser.parse_args()

    print("=" * 52)
    print("  实习岗位工作流 — HTML 生成")
    print("=" * 52)

    # 1. 定位 CSV 文件
    csv_path = args.csv or get_latest_csv()
    if not csv_path or not os.path.exists(csv_path):
        print("\n[ERROR] 未找到 CSV 文件！")
        print(f"  请先在 WorkBuddy 对话框输入'更新实习岗位'生成数据")
        print(f"  或手动运行: python scraper.py --demo")
        sys.exit(1)

    print(f"\n[1/3] 读取岗位数据...")
    print(f"      CSV: {csv_path}")
    rows = load_csv(csv_path)
    jobs = [csv_row_to_job(r) for r in rows]
    print(f"      [OK] 共 {len(jobs)} 条岗位")

    # 2. 统计
    new_jobs = [j for j in jobs if is_new(j.get('publish_date', ''))]
    expired_jobs = [j for j in jobs if is_expired(j.get('publish_date', ''))]
    active_jobs = [j for j in jobs if not is_expired(j.get('publish_date', ''))]

    print(f"\n[2/3] 生成网页...")
    print(f"      今日新增: {len(new_jobs)} 条")
    print(f"      有效岗位: {len(active_jobs)} 条（{EXPIRY_DAYS}天内）")
    print(f"      已过期:   {len(expired_jobs)} 条（超过{EXPIRY_DAYS}天，页面灰色显示）")

    # 3. 生成 HTML（传入全部岗位，过期状态由前端控制显示）
    generate_html(
        jobs,
        TEMPLATE_PATH,
        HTML_OUTPUT,
        title='实习岗位推荐',
        subtitle='中央音乐学院 · 2028届 · 音乐艺术管理'
    )
    print(f"      [OK] 网页已生成: {HTML_OUTPUT}")

    # 4. 自动 git push（可用 --no-push 跳过）
    if not args.no_push:
        print(f"\n[3/3] 推送到 GitHub Pages...")
        git_push(BASE_DIR, HTML_OUTPUT)
    else:
        print(f"\n[3/3] 已跳过 git push（--no-push 模式）")

    print("\n" + "=" * 52)
    print("  生成完成！")
    print(f"  数据来源:   {os.path.basename(csv_path)}")
    print(f"  总岗位数:   {len(jobs)} 条")
    print(f"  今日新增:   {len(new_jobs)} 条")
    print(f"  网页路径:   {HTML_OUTPUT}")
    if not args.no_push:
        print(f"  在线地址:   https://silent-wyr.github.io/job/")
    print("=" * 52)


if __name__ == '__main__':
    main()
