# job-info-publisher

实习岗位网页发布 Skill

## 简介

这个 Skill 将 job-info-scraper 输出的 CSV/JSON 招聘数据，生成为可在浏览器中访问的 HTML 网页，特别适合手机查看和筛选岗位。

### 主要功能

1. **数据转换**：从 CSV/JSON 转换为响应式 HTML 网页
2. **卡片式布局**：移动优先，每个岗位一张卡片
3. **交互功能**：筛选、搜索、排序、展开详情
4. **智能提示**：新岗位提醒、过期岗位管理
5. **双模式部署**：本地 HTML（快速体验）+ GitHub Pages（密码保护）

## 适用场景

- 将 job-info-scraper 输出可视化展示
- 手机端浏览和筛选实习岗位
- 快速查看岗位详情和投递方式
- 自动标记新岗位和过期岗位

## 快速开始

### 方式一：从 CSV 生成网页

```bash
python scripts/generate_html.py
```

脚本会自动查找 `job_results.csv` 或 `filtered_jobs.json` 文件，生成 `index.html`。

### 方式二：手动调用脚本

```python
from scripts.generate_html import HTMLGenerator

generator = HTMLGenerator()

# 从 CSV 加载数据
jobs = generator.load_csv('job_results_20260310_143000.csv')

# 生成 HTML
generator.generate_html(
    jobs,
    output_path='index.html',
    config={
        'title': '实习岗位推荐',
        'subtitle': '中央音乐学院 · 2028届 · 音乐艺术管理'
    }
)
```

### 查看网页

双击生成的 `index.html` 文件，在浏览器中打开即可查看。

## 部署方式

### 方案 A：本地 HTML（立即使用）

**操作流程**：

1. 运行脚本生成 HTML
   ```bash
   python scripts/generate_html.py
   ```

2. 直接在浏览器打开
   ```
   双击 index.html
   ```

3. 或上传到云盘分享
   - 上传到百度云/坚果云
   - 分享链接 + 提取码
   - 手机打开链接查看

**优点**：
- ✅ 无需注册账号
- ✅ 5分钟快速体验
- ✅ 完全私密

---

### 方案 B：GitHub Pages（稳定后）

**准备工作**：

1. 注册 GitHub 账号
   - 访问 https://github.com
   - 用邮箱注册（免费）

2. 创建仓库
   - 点击 "New repository"
   - 仓库名：`my-job-portal`
   - 设置为 Public
   - 点击 "Create repository"

3. 上传 HTML 文件
   - 点击 "Upload files"
   - 拖拽 `index.html` 文件
   - 填写提交信息
   - 点击 "Commit changes"

4. 开启 GitHub Pages
   - 进入仓库设置（Settings）
   - 找到 "Pages"
   - 在 "Source" 中选择分支 `main`
   - 点击 "Save"
   - 等待几分钟后访问：`https://你的用户名.github.io/my-job-portal`

**密码保护**（可选）：

```python
generator.generate_html_with_password(
    jobs,
    output_path='index_protected.html',
    password='123456',
    config={...}
)
```

**优点**：
- ✅ 免费部署
- ✅ 全球 CDN 加速
- ✅ 自定义网址
- ✅ HTTPS 支持
- ✅ 密码保护

## 网页功能

### 卡片式展示

每个岗位以卡片形式展示，包含：

**默认折叠状态**：
- 公司名称和岗位名称
- 优先级标签（P0-P4，颜色区分）
- 工作地点和发布日期
- 匹配分数
- 基本信息（每周天数、学历、实习类型）
- 操作按钮（展开详情、复制邮箱、查看原文）

**展开后显示**：
- 完整岗位描述
- 任职要求
- 投递邮箱和方式
- 原文链接
- 截止日期

### 筛选功能

- **按优先级**：P0/P1/P2/P3
- **按岗位类型**：音乐运营、演出策划、经纪人、新媒体运营等
- **按时间**：今日新增、昨日更新、本周、更早、已过期

### 搜索功能

- 实时搜索岗位名称、公司名称、岗位描述
- 输入即搜索，无需点击按钮

### 排序功能

- 按匹配分数（从高到低）
- 按发布日期（从新到旧）
- 按优先级（P0 → P1 → P2 → P3）

### 新岗位提醒

- 顶部红色提示条显示"有 X 个新岗位"
- 新岗位标记"新"徽章
- 点击提示条快速定位到今日新增

### 过期岗位管理

- 超过 7 天的岗位自动标记为"已过期"
- 过期岗位灰色显示
- 可选择隐藏过期岗位

### 响应式设计

- **移动端**：单列布局（优先）
- **平板端**：双列布局
- **PC 端**：三列布局

## 配置说明

编辑 `assets/config/publisher_config.json` 自定义网页：

```json
{
  "page": {
    "title": "实习岗位推荐",
    "subtitle": "中央音乐学院 · 2028届 · 音乐艺术管理"
  },
  "data": {
    "retention_days": 7
  },
  "ui": {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2"
  }
}
```

### 主要配置项

| 字段 | 说明 | 示例 |
|------|------|------|
| page.title | 网页标题 | "我的实习岗位" |
| page.subtitle | 网页副标题 | "2028届本科" |
| data.retention_days | 岗位保留天数 | 7 |
| ui.primary_color | 主题色 | "#667eea" |
| password.enabled | 启用密码保护 | true/false |

## 使用示例

### 示例 1：生成基本网页

```python
from scripts.generate_html import HTMLGenerator

generator = HTMLGenerator()

# 加载数据
jobs = generator.load_csv('job_results.csv')

# 生成网页
generator.generate_html(jobs, 'index.html')

# 查看
# 在浏览器中打开 index.html
```

### 示例 2：自定义标题和保留期

```python
config = {
    'title': '音乐类实习岗位',
    'subtitle': '2027-2028届',
    'retention_days': 14
}

generator.generate_html(jobs, 'index.html', config=config)
```

### 示例 3：生成带密码保护的网页

```python
generator.generate_html_with_password(
    jobs,
    output_path='index_protected.html',
    password='my_secret_password',
    config={...}
)
```

## 更新流程

当有新的岗位数据时：

```bash
# 1. 获取最新岗位数据
cd ..  # 回到技能目录
python job-info-scraper/scripts/scraper_example.py
python job-info-scraper/scripts/parser_example.py
python job-info-scraper/scripts/filter_example.py

# 2. 生成更新后的网页
cd job-info-publisher
python scripts/generate_html.py

# 3. 部署
# 本地：直接打开 index.html
# 云盘：重新上传 index.html
# GitHub：提交新的 index.html
```

## 目录结构

```
job-info-publisher/
├── SKILL.md                        # Skill 核心指导文档
├── README.md                       # 本文件
├── assets/
│   ├── config/
│   │   └── publisher_config.json    # 配置文件
│   └── templates/
│       └── job_portal.html         # HTML 模板
└── scripts/
    └── generate_html.py             # HTML 生成脚本
```

## 浏览器兼容性

- ✅ Chrome 90+
- ✅ Safari 14+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ 微信内置浏览器
- ✅ 手机浏览器（iOS Safari、Chrome Mobile）

不支持 IE 11 及以下。

## 注意事项

1. **数据格式**：确保 CSV/JSON 数据包含所有必需字段
2. **日期格式**：发布日期应为 YYYY-MM-DD 格式
3. **密码安全**：密码保存在浏览器 localStorage，清除数据后会丢失
4. **隐私保护**：本地 HTML 模式无需密码，云盘模式使用提取码
5. **更新频率**：建议每日或每周更新一次

## 常见问题

**Q: HTML 文件太大怎么办？**

A: 可以通过以下方式优化：
- 减少 `retention_days`（如从 7 天改为 3 天）
- 删除不需要的历史数据
- 在 job-info-scraper 阶段增加筛选条件

**Q: 如何修改网页颜色？**

A: 编辑 `assets/config/publisher_config.json` 中的颜色配置，或直接修改 `assets/templates/job_portal.html` 的 CSS。

**Q: 密码忘记了怎么办？**

A: 清除浏览器的 localStorage：
```javascript
localStorage.clear()
```
然后重新设置密码。

**Q: 网页在手机上显示不正常？**

A: 检查：
- 确保使用了 HTML5 模板
- 检查 viewport meta 标签是否存在
- 在实际手机设备上测试（而非桌面浏览器）

**Q: 如何添加自定义功能？**

A: 编辑 `assets/templates/job_portal.html`，添加或修改 JavaScript 功能。

## 技术支持

如有问题或建议，请查看相关文档或联系技术支持。

## 更新日志

- **v1.0.0** (2026-03-10)
  - 初始版本发布
  - 支持 CSV/JSON 转 HTML
  - 卡片式布局
  - 筛选、搜索、排序功能
  - 新岗位提醒和过期岗位管理
  - 双模式部署（本地 + GitHub Pages）
  - 密码保护功能
