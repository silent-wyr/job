# 招聘数据结构定义

本文档定义了招聘信息的数据结构和字段格式规范。

## 数据层级结构

```
Job List (职位列表)
  └── Job (单个职位)
      ├── Company (公司信息)
      ├── Position (岗位信息)
      ├── Requirements (岗位要求)
      ├── Match Status (匹配状态)
      └── Application Info (投递信息)
```

## 完整数据结构

### Job (职位对象)

```json
{
  "job_id": "唯一标识符",
  "source": "数据来源",
  "source_url": "原始链接",
  "publish_date": "发布日期 (ISO 8601格式)",
  "company": {
    "name": "公司名称",
    "priority_level": "P0/P1/P2/P3",
    "industry": "行业分类",
    "location": "公司所在地",
    "business_lines": ["业务线1", "业务线2"]
  },
  "position": {
    "title": "岗位名称",
    "type": "岗位类型",
    "match_score": 0,
    "matched_keywords": ["关键词1", "关键词2"]
  },
  "requirements": {
    "location": "工作地点",
    "education": "学历要求",
    "graduation_year": "毕业年份",
    "min_work_days_per_week": 每周最少工作天数,
    "internship_duration": "实习时长",
    "daily_internship": true/false,
    "min_duration_months": 最少实习月数
  },
  "description": "岗位描述文本",
  "job_responsibilities": "工作职责（从岗位描述中提取的核心职责条目，换行分隔）",
  "skill_requirements": "技能要求（从岗位描述中提取的必备技能和资质，换行分隔）",
  "match_status": {
    "meets_basic_requirements": true/false,
    "missing_requirements": ["未满足的条件1", "未满足的条件2"]
  },
  "application_info": {
    "email": "投递邮箱",
    "deadline": "截止日期 (ISO 8601格式)",
    "application_method": "投递方式",
    "contact_person": "联系人",
    "contact_phone": "联系电话"
  }
}
```

## 字段详细说明

### 基础信息字段

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| job_id | String | 是 | 唯一标识符 | "job_20260310_tencent_001" |
| source | String | 是 | 数据来源 | "微信公众号", "BOSS直聘", "实习僧" |
| source_url | String | 否 | 原始链接 | "https://mp.weixin.qq.com/s/xxx" |
| publish_date | String | 是 | 发布日期 | "2026-03-10" 或 "2026-03-10T14:30:00+08:00" |

### Company (公司信息)

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| name | String | 是 | 公司名称 | "腾讯音乐" |
| priority_level | String | 是 | 优先级 | "P0", "P1", "P2", "P3" |
| industry | String | 否 | 行业分类 | "互联网", "音乐", "演出" |
| location | String | 否 | 公司所在地 | "北京海淀区" |
| business_lines | Array | 否 | 业务线 | ["音乐流媒体", "音乐版权"] |

### Position (岗位信息)

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| title | String | 是 | 岗位名称 | "音乐运营实习生" |
| type | String | 否 | 岗位类型 | "音乐运营", "演出策划", "经纪人" |
| match_score | Integer | 否 | 匹配分数 | 15 |
| matched_keywords | Array | 否 | 匹配的关键词 | ["音乐运营", "活动策划"] |

### Requirements (岗位要求)

| 字段名 | 类型 | 必填 | 说明 | 示例 | 可能的值 |
|--------|------|------|------|------|----------|
| location | String | 是 | 工作地点 | "北京" | "北京", "上海", "广州", "深圳" |
| education | String | 是 | 学历要求 | "本科及以上" | "本科", "本科及以上", "硕士", "不限" |
| graduation_year | String | 否 | 毕业年份 | "2028" | "2024", "2025", "2026", "2027", "2028", "不限" |
| min_work_days_per_week | Integer | 否 | 每周最少工作天数（岗位要求的最低出勤天数） | 3 | 1, 2, 3, 4, 5 |
| internship_duration | String | 否 | 实习时长 | "3个月" | "3个月", "6个月", "长期" |
| daily_internship | Boolean | 否 | 是否日常实习 | true | true, false |
| min_duration_months | Integer | 否 | 最少实习月数 | 3 | 3, 6 |

### Match Status (匹配状态)

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| meets_basic_requirements | Boolean | 是 | 是否满足基本条件 | true |
| missing_requirements | Array | 否 | 未满足的条件列表 | ["工作地点不是北京"] |

### Application Info (投递信息)

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| email | String | 否 | 投递邮箱 | "hr@company.com" |
| deadline | String | 否 | 截止日期 | "2026-04-01" |
| application_method | String | 否 | 投递方式 | "发送邮件至xxx" |
| contact_person | String | 否 | 联系人 | "张女士" |
| contact_phone | String | 否 | 联系电话 | "138xxxx1234" |

## CSV 输出格式

### 列顺序和命名

| 列名 | 说明 | 示例 |
|------|------|------|
| 公司名称 | 公司名称 | 腾讯音乐 |
| 优先级 | P0/P1/P2/P3 | P0 |
| 岗位名称 | 岗位名称 | 音乐运营实习生 |
| 岗位类型 | 岗位类型 | 音乐运营 |
| 工作地点 | 工作地点 | 北京 |
| 学历要求 | 学历要求 | 本科及以上 |
| 毕业年份 | 毕业年份要求 | 2028 |
| 每周最少工作天数 | 岗位要求的每周最少出勤天数 | 3 |
| 实习类型 | 实习类型 | 日常实习 |
| 实习时长 | 实习时长 | 3个月 |
| 工作职责 | 岗位核心职责（提炼自岗位描述） | 协助内容运营；参与活动策划 |
| 技能要求 | 必备技能和资质（提炼自岗位描述） | 熟悉音乐产业；良好沟通能力 |
| 匹配分数 | 匹配分数 | 15 |
| 发布日期 | 发布日期 | 2026-03-10 |
| 投递邮箱 | 投递邮箱 | hr@tencent.com |
| 数据来源 | 数据来源 | 微信公众号 |
| 原始链接 | 原始链接 | https://mp.weixin.qq.com/s/xxx |

### CSV 示例

```csv
公司名称,优先级,岗位名称,岗位类型,工作地点,学历要求,毕业年份,每周最少工作天数,实习类型,实习时长,工作职责,技能要求,匹配分数,发布日期,投递邮箱,数据来源,原始链接
腾讯音乐,P0,音乐运营实习生,音乐运营,北京,本科及以上,2028,3,日常实习,3个月,协助内容运营；挖掘优质音乐；参与活动策划,热爱音乐；音乐相关专业优先；良好沟通能力,15,2026-03-10,hr@tencent.com,微信公众号,https://mp.weixin.qq.com/s/xxx
网易云音乐,P0,工作室运营实习生,音乐运营,北京,本科,不限,3,日常实习,6个月,参与音乐人运营支持；协助内容制作,熟悉音乐产业生态；数据分析能力,13,2026-03-09,hr@163.com,微信公众号,https://mp.weixin.qq.com/s/yyy
太合音乐,P2,音乐节策划执行,演出策划执行,北京,本科,不限,4,日常实习,3个月,协助音乐节现场执行；对接场地及供应商,活动策划经验；较强执行力,8,2026-03-08,zhang@taihe.com,微信公众号,https://mp.weixin.qq.com/s/zzz
```

## JSON 示例

### 完整示例

```json
{
  "job_id": "job_20260310_tencent_001",
  "source": "微信公众号",
  "source_url": "https://mp.weixin.qq.com/s/xxxxxxxxxxxx",
  "publish_date": "2026-03-10",
  "company": {
    "name": "腾讯音乐",
    "priority_level": "P0",
    "industry": "互联网",
    "location": "北京海淀区",
    "business_lines": ["音乐流媒体", "音乐版权", "音乐社交"]
  },
  "position": {
    "title": "音乐运营实习生",
    "type": "音乐运营",
    "match_score": 15,
    "matched_keywords": ["音乐运营", "活动策划"]
  },
  "requirements": {
    "location": "北京",
    "education": "本科及以上",
    "graduation_year": "2028",
    "min_work_days_per_week": 3,
    "internship_duration": "3个月",
    "daily_internship": true,
    "min_duration_months": 3
  },
  "description": "岗位职责：\n1. 协助团队进行音乐内容运营\n2. 挖掘优质音乐内容\n3. 参与活动策划和执行\n\n任职要求：\n1. 热爱音乐，对音乐有敏锐度\n2. 本科在读，音乐相关专业优先\n3. 每周可实习至少3天，持续3个月以上",
  "job_responsibilities": "协助团队进行音乐内容运营；挖掘优质音乐内容；参与活动策划和执行",
  "skill_requirements": "热爱音乐，对音乐有敏锐度；本科在读，音乐相关专业优先；良好的沟通与协作能力",
  "match_status": {
    "meets_basic_requirements": true,
    "missing_requirements": []
  },
  "application_info": {
    "email": "hr@tencent.com",
    "deadline": "2026-04-01",
    "application_method": "发送简历至hr@tencent.com",
    "contact_person": "张女士",
    "contact_phone": "13812345678"
  }
}
```

## 数据验证规则

### 必填字段验证

以下字段必须有值，否则数据无效：
- `job_id`
- `source`
- `publish_date`
- `company.name`
- `company.priority_level`
- `position.title`
- `requirements.location`
- `requirements.education`
- `match_status.meets_basic_requirements`

### 字段格式验证

| 字段 | 格式要求 | 验证规则 |
|------|----------|----------|
| job_id | String | 不能为空，唯一 |
| publish_date | ISO 8601 | YYYY-MM-DD 或 YYYY-MM-DDTHH:MM:SS+TZ |
| priority_level | String | 必须是 P0, P1, P2, P3 之一 |
| min_work_days_per_week | Integer | 1-5 之间 |
| match_score | Integer | >= 0 |
| education | String | 必须包含"本科", "硕士", "博士", "不限"之一 |
| graduation_year | String | 4位数字或"不限" |

### 枚举值定义

#### priority_level (优先级)
- `P0`: 最高优先级
- `P1`: 高优先级
- `P2`: 中优先级
- `P3`: 普通优先级

#### education (学历要求)
- `本科`
- `本科及以上`
- `硕士`
- `硕士及以上`
- `博士`
- `不限`

#### location (工作地点)
- `北京`
- `上海`
- `广州`
- `深圳`
- `杭州`
- `成都`
- `武汉`
- 其他城市

#### internship_type (实习类型)
- `日常实习`
- `暑期实习`
- `长期实习`

## 数据转换示例

### 从原始文本到结构化数据

**原始文本:**
```
【腾讯音乐-音乐运营实习生】
工作地点：北京
学历要求：本科及以上
毕业年份：2028届
每周工作：至少3天
实习时长：3个月
实习类型：日常实习

岗位职责：协助音乐内容运营、挖掘优质音乐内容、参与活动策划
技能要求：热爱音乐、音乐相关专业优先、良好沟通能力

投递邮箱：hr@tencent.com
联系人：张女士
```

**转换后:**
```json
{
  "company": {
    "name": "腾讯音乐",
    "priority_level": "P0"
  },
  "position": {
    "title": "音乐运营实习生",
    "type": "音乐运营"
  },
  "requirements": {
    "location": "北京",
    "education": "本科及以上",
    "graduation_year": "2028",
    "min_work_days_per_week": 3,
    "internship_duration": "3个月",
    "daily_internship": true
  },
  "job_responsibilities": "协助音乐内容运营；挖掘优质音乐内容；参与活动策划",
  "skill_requirements": "热爱音乐；音乐相关专业优先；良好沟通能力",
  "application_info": {
    "email": "hr@tencent.com",
    "contact_person": "张女士"
  }
}
```

## 数据质量指标

### 完整性
- 必填字段完整率: 100%
- 所有字段完整率: >90%

### 准确性
- 公司名称识别准确率: >95%
- 岗位类型识别准确率: >90%
- 工作地点识别准确率: >98%

### 一致性
- 同一公司名称一致
- 日期格式统一
- 枚举值使用正确
