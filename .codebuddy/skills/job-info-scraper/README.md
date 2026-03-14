# job-info-scraper

实习招聘信息爬取和筛选 Skill

## 简介

这个 Skill 专门用于从微信公众号和招聘网站爬取实习招聘信息，并根据预设的筛选条件进行过滤和排序，最终输出 CSV/Excel 格式的结果文件。

### 主要功能

1. **数据采集**: 从微信公众号、招聘网站等渠道获取招聘信息
2. **内容解析**: 从非结构化文本中提取结构化的职位信息
3. **智能筛选**: 根据工作地点、学历要求、毕业年份等条件筛选岗位
4. **优先级排序**: 根据公司优先级和匹配分数对岗位排序
5. **结果导出**: 生成 CSV/Excel 格式的结果文件

## 适用场景

- 为特定学生寻找合适的实习岗位
- 监控特定公司的招聘信息
- 批量筛选和整理招聘信息
- 生成职位推荐报告

## 快速开始

### 1. 配置筛选条件

编辑 `assets/config/filter_rules.json` 文件，配置您的筛选条件：

```json
{
  "basic_filters": {
    "location": ["北京"],
    "education": ["本科", "本科及以上"],
    "graduation_year": ["2028"],
    "min_work_days_per_week": 3
  }
}
```

### 2. 添加目标公司

编辑 `assets/config/target_companies.json` 文件，添加您关注的公司：

```json
{
  "companies": [
    {
      "name": "腾讯音乐",
      "priority": "P0",
      "wechat_accounts": ["QQ音乐招聘"],
      "website": "https://jobs.tencent.com"
    }
  ]
}
```

### 3. 运行爬虫

```bash
# 爬取微信公众号
python scripts/scraper_example.py

# 解析招聘信息
python scripts/parser_example.py

# 筛选和排序
python scripts/filter_example.py
```

### 4. 查看结果

生成的 CSV 文件位于当前目录：
- `job_results_YYYYMMDD_HHMMSS.csv` - 筛选后的职位列表
- `job_summary_YYYYMMDD_HHMMSS.txt` - 筛选结果摘要

## 目录结构

```
job-info-scraper/
├── SKILL.md                    # Skill 核心指导文档
├── README.md                   # 本文件
├── assets/                     # 资源文件
│   └── config/                 # 配置文件
│       ├── filter_rules.json   # 筛选规则配置
│       └── target_companies.json # 目标公司配置
├── scripts/                    # 脚本文件
│   ├── scraper_example.py     # 爬虫脚本示例
│   ├── parser_example.py      # 解析脚本示例
│   └── filter_example.py      # 筛选脚本示例
└── references/                 # 参考文档
    ├── company_list.md         # 目标公司清单
    ├── keyword_mapping.md     # 岗位关键词映射
    └── data_schema.md          # 数据结构定义
```

## 配置说明

### 筛选规则 (filter_rules.json)

#### basic_filters (基本筛选条件)

| 字段 | 说明 | 示例 |
|------|------|------|
| location | 工作地点 | ["北京", "上海"] |
| education | 学历要求 | ["本科", "本科及以上"] |
| graduation_year | 毕业年份 | ["2028", "不限"] |
| min_work_days_per_week | 每周最少工作天数 | 3 |
| internship_type | 实习类型 | ["日常实习"] |

#### keywords (关键词)

- `required`: 必须包含的关键词
- `optional`: 可选关键词（辅助判断）

#### company_priorities (公司优先级)

- `P0`: 最高优先级（如腾讯、字节跳动）
- `P1`: 高优先级（如索尼音乐、环球音乐）
- `P2`: 中优先级（如太合音乐、摩登天空）
- `P3`: 普通优先级（其他公司）

#### scoring_rules (评分规则)

| 规则 | 分数 | 说明 |
|------|------|------|
| P0_company | 10 | P0公司加10分 |
| P1_company | 8 | P1公司加8分 |
| P2_company | 5 | P2公司加5分 |
| explicit_2028 | 5 | 明确招收2028届加5分 |
| work_days_meets_min | 3 | 每周天数满足最少要求加3分 |
| music_major_preferred | 2 | 音乐专业优先加2分 |

### 目标公司 (target_companies.json)

每个公司包含以下字段：

| 字段 | 说明 | 必填 |
|------|------|------|
| name | 公司名称 | 是 |
| aliases | 别名列表 | 否 |
| priority | 优先级 (P0/P1/P2/P3) | 是 |
| wechat_accounts | 微信公众号列表 | 否 |
| website | 招聘网站URL | 否 |
| industries | 行业分类 | 否 |
| location | 公司所在地 | 否 |
| business_lines | 业务线列表 | 否 |

## 输出格式

### CSV 文件

生成的 CSV 文件包含以下列：

| 列名 | 说明 |
|------|------|
| 公司名称 | 公司名称 |
| 优先级 | P0/P1/P2/P3 |
| 岗位名称 | 岗位名称 |
| 岗位类型 | 岗位类型（音乐运营、演出策划等）|
| 工作地点 | 工作地点 |
| 学历要求 | 学历要求 |
| 毕业年份 | 毕业年份要求 |
| 每周最少工作天数 | 岗位要求的每周最少出勤天数 |
| 实习类型 | 实习类型（日常实习/暑期实习）|
| 实习时长 | 实习时长 |
| 工作职责 | 核心岗位职责（提炼自岗位描述）|
| 技能要求 | 必备技能和资质（提炼自岗位描述）|
| 匹配分数 | 匹配分数 |
| 发布日期 | 发布日期 |
| 投递邮箱 | 投递邮箱 |
| 数据来源 | 数据来源（微信公众号/招聘网站）|
| 原始链接 | 原始链接 |

### 摘要报告

摘要报告包含以下内容：

- 总计匹配岗位数
- 按优先级分布统计
- Top 10 推荐岗位列表

## 使用示例

### 示例 1: 为中央音乐学院学生寻找实习

**需求**: 北京地区、2028届本科生、每周至少3天、音乐相关岗位

**配置**:
```json
{
  "basic_filters": {
    "location": ["北京"],
    "education": ["本科", "本科及以上"],
    "graduation_year": ["2028"],
    "min_work_days_per_week": 3
  },
  "keywords": {
    "required": [
      "音乐活动策划",
      "经纪人",
      "自媒体运营",
      "音乐运营",
      "演出策划"
    ]
  }
}
```

**运行**:
```bash
python scripts/scraper_example.py
python scripts/parser_example.py
python scripts/filter_example.py
```

**结果**: 生成 `job_results_20260310_143000.csv`

### 示例 2: 监控特定公司招聘

**需求**: 监控腾讯音乐、网易云音乐的最新招聘信息

**配置**:
```json
{
  "companies": [
    {
      "name": "腾讯音乐",
      "priority": "P0",
      "wechat_accounts": ["QQ音乐招聘"]
    },
    {
      "name": "网易云音乐",
      "priority": "P0",
      "wechat_accounts": ["网易云音乐招聘"]
    }
  ]
}
```

**运行**:
```bash
python scripts/scraper_example.py
```

## 注意事项

1. **微信公众号爬取**: 微信公众号爬取可能受到限制，建议使用官方API或第三方服务
2. **反爬措施**: 招聘网站可能有反爬机制，请合理设置请求间隔
3. **数据准确性**: 自动解析可能存在误差，建议人工复核关键信息
4. **配置更新**: 定期更新目标公司列表和关键词映射

## 限制和未来改进

### 当前限制

1. 微信公众号爬取需要认证或使用第三方服务
2. 部分招聘网站结构复杂，解析难度较大
3. 岗位描述格式多样，解析准确率有待提高
4. 不支持实时更新和定时任务

### 未来改进

1. 支持更多招聘平台（LinkedIn、Indeed等）
2. 引入机器学习提高解析准确率
3. 增加定时任务和自动更新功能
4. 支持多地区、多岗位类型的并发搜索
5. 集成邮件通知或推送功能

## 相关文档

- `SKILL.md` - Skill 使用指南
- `references/company_list.md` - 目标公司清单
- `references/keyword_mapping.md` - 岗位关键词映射
- `references/data_schema.md` - 数据结构定义

## 常见问题

**Q: 如何添加新的数据源？**

A: 编辑 `filter_rules.json` 中的 `data_sources` 部分，添加新的微信公众号或网站URL。

**Q: 筛选条件如何自定义？**

A: 修改 `filter_rules.json` 中的 `basic_filters`、`keywords` 和 `company_priorities`。

**Q: 如何提高匹配准确率？**

A: 1. 完善 `target_companies.json` 中的公司别名
   2. 补充 `keyword_mapping.md` 中的关键词列表
   3. 调整 `scoring_rules` 中的评分权重

**Q: 输出的 CSV 文件乱码怎么办？**

A: CSV 文件使用 UTF-8 编码，Excel 打开时选择正确的编码格式，或使用支持 UTF-8 的编辑器。

## 技术支持

如有问题或建议，请查看相关文档或联系技术支持。

## 更新日志

- **v1.0.0** (2026-03-10)
  - 初始版本发布
  - 支持微信公众号和招聘网站爬取
  - 支持基本筛选和排序功能
  - 支持 CSV/Excel 输出
