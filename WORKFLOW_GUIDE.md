# 实习招聘信息工作流使用指南

## 🚀 快速开始（推荐）

### Windows 用户

双击运行 `run_workflow.bat` 即可一键完成所有步骤。

### Linux/Mac 用户

```bash
chmod +x run_workflow.sh
./run_workflow.sh
```

---

## 📋 手动执行步骤

### 第一步：爬取和筛选招聘信息

```bash
cd .codebuddy/skills/job-info-scraper

# 1. 爬取数据
python scripts/scraper_example.py

# 2. 解析数据
python scripts/parser_example.py

# 3. 筛选数据
python scripts/filter_example.py
```

**输出文件**：
- `output/job_results_YYYYMMDD_HHMMSS.csv` - 筛选后的岗位列表
- `output/job_summary_YYYYMMDD_HHMMSS.txt` - 筛选结果摘要

---

### 第二步：生成岗位门户网页

```bash
cd ../job-info-publisher

# 生成网页
python scripts/generate_html.py
```

**输出文件**：
- `index.html` - 完整的岗位门户网页

---

### 第三步：查看和部署

#### 方式 A：本地查看

1. 双击 `index.html` 在浏览器中打开
2. 或右键 → 打开方式 → 选择浏览器

#### 方式 B：上传云盘（推荐）

1. 打开百度云/坚果云
2. 上传 `index.html` 文件
3. 创建分享链接，设置提取码
4. 在手机上打开链接，输入提取码查看

#### 方式 C：部署到 GitHub Pages（稳定后）

1. 注册 GitHub 账号
2. 创建仓库，上传 `index.html`
3. 开启 GitHub Pages
4. 获得自定义网址访问

---

## ⚙️ 配置调整

### 调整筛选条件

编辑 `.codebuddy/skills/job-info-scraper/assets/config/filter_rules.json`：

```json
{
  "basic_filters": {
    "location": ["北京"],
    "education": ["本科"],
    "graduation_year": ["2028"],
    "max_work_days_per_week": 4,
    "internship_type": ["日常实习"]
  }
}
```

### 调整目标公司

编辑 `.codebuddy/skills/job-info-scraper/assets/config/target_companies.json`：

```json
{
  "companies": [
    {
      "name": "新公司名称",
      "priority": "P1",
      "wechat_accounts": ["公众号名"],
      "website": "招聘网站URL"
    }
  ]
}
```

### 调整网页样式

编辑 `.codebuddy/skills/job-info-publisher/assets/config/publisher_config.json`：

```json
{
  "theme": "light",
  "retention_days": 7,
  "show_expired": true
}
```

---

## 📅 定期执行建议

### 每日自动执行

**Windows 定时任务**：
1. 打开"任务计划程序"
2. 创建基本任务 → 设置触发器（每天固定时间）
3. 操作 → 启动程序 → 选择 `run_workflow.bat`

**Linux Cron 任务**：
```bash
crontab -e
# 添加以下行（每天早上9点执行）
0 9 * * * cd /path/to/project && ./run_workflow.sh
```

### 手动执行

建议每天或每两天执行一次，保持岗位信息最新。

---

## 📁 文件结构

```
工作目录/
├── run_workflow.bat          # Windows 一键运行脚本
├── run_workflow.sh            # Linux/Mac 一键运行脚本
├── .codebuddy/skills/
│   ├── job-info-scraper/      # 爬取和筛选 Skill
│   │   ├── scripts/          # 脚本文件
│   │   ├── assets/config/    # 配置文件
│   │   └── output/           # 输出数据（CSV）
│   └── job-info-publisher/   # 网页发布 Skill
│       ├── scripts/          # 脚本文件
│       ├── assets/config/    # 配置文件
│       ├── assets/templates/ # HTML 模板
│       └── index.html        # 生成的网页
└── WORKFLOW_GUIDE.md         # 本文档
```

---

## 🔍 常见问题

### Q: 提示找不到 python 命令？

**A**: 请确保 Python 已安装并添加到系统 PATH。检查方式：
```bash
python --version
```

### Q: 爬取没有数据？

**A**: 检查以下几点：
1. 目标网站是否可访问
2. 网站结构是否变化
3. 查看控制台错误信息

### Q: 筛选结果为空？

**A**: 调整筛选条件：
- 放宽地点限制（如增加"上海"）
- 增加关键词范围
- 降低学历要求
- 增加毕业年份选项

### Q: 网页无法打开？

**A**: 确认以下几点：
1. `index.html` 文件存在
2. 浏览器支持 JavaScript（建议使用 Chrome/Edge）
3. CSV/JSON 数据格式正确

### Q: 如何更换到其他城市？

**A**: 编辑 `filter_rules.json`：
```json
{
  "basic_filters": {
    "location": ["上海", "北京"]
  }
}
```

---

## 📞 需要帮助？

如果遇到问题，请检查：
1. 日志文件（如果有）
2. 控制台错误信息
3. 配置文件格式是否正确

---

## 🎯 下一步

1. 首次运行：双击 `run_workflow.bat`
2. 查看效果：打开生成的 `index.html`
3. 调整配置：根据实际需求修改配置文件
4. 部署上线：上传云盘或 GitHub Pages
5. 定期更新：每天/每两天执行一次

**祝您找到理想的实习岗位！** 🎉
