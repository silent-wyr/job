# job-info-publisher Skill

## Metadata
name: job-info-publisher
description: This skill should be used when users need to publish job listings from CSV/JSON data files to a web page for mobile-friendly viewing. The skill generates responsive HTML pages with card-based layout, supports filtering and searching, and provides features like new job alerts, expiration management, and optional password protection. Output can be deployed locally or to GitHub Pages.
version: 1.0.0

## Skill Purpose

This skill transforms job listing data from job-info-scraper outputs into a responsive, mobile-friendly web page. It helps users:

1. Convert CSV/JSON job data into HTML web pages
2. Display job listings in card-based layout optimized for mobile viewing
3. Provide filtering, searching, and sorting capabilities
4. Highlight new jobs and manage expired listings
5. Support two deployment modes: local HTML (quick start) and GitHub Pages with password protection

## When to Use This Skill

Use this skill when:
- User has CSV/JSON job data from job-info-scraper and needs to display it on a web page
- User wants a mobile-friendly interface for browsing job listings
- User needs features like filtering, searching, and sorting
- User wants to highlight new jobs and manage expired listings
- User needs to deploy the web page locally or to GitHub Pages
- User wants optional password protection for the web page

## Workflow

### Step 1: Prepare Input Data

Obtain job data from job-info-scraper output:

**CSV Format** (preferred):
- `job_results_YYYYMMDD_HHMMSS.csv` - Filtered job listings with all required fields
- Columns: 公司名称, 优先级, 岗位名称, 岗位类型, 工作地点, 学历要求, 毕业年份, 每周最少工作天数, 实习类型, 实习时长, 工作职责, 技能要求, 匹配分数, 发布日期, 投递邮箱, 数据来源, 原始链接

**JSON Format**:
- `filtered_jobs.json` - Filtered job listings in JSON format
- Structure follows the schema defined in job-info-scraper's data_schema.md

### Step 2: Load Data

Load job data into the HTML generator:

```python
from scripts.generate_html import HTMLGenerator

generator = HTMLGenerator()

# Load from CSV
jobs = generator.load_csv('job_results_20260310_143000.csv')

# Or load from JSON
jobs = generator.load_json('filtered_jobs.json')
```

The data will be automatically parsed and processed:
- Extract and validate all required fields
- Parse 工作职责 and 技能要求 fields — split by "；" or newline into arrays for bullet-point rendering
- Calculate job age (new/expired status)
- Format dates and other values
- Prepare data for JavaScript rendering

### Step 3: Configure Web Page Settings

Customize the web page appearance and behavior:

```python
config = {
    'title': '实习岗位推荐',                          # Page title
    'subtitle': '中央音乐学院 · 2028届 · 音乐艺术管理',  # Page subtitle
    'retention_days': 7,                             # Job retention period
}
```

**Configuration Options**:
- `title`: Web page title displayed in header
- `subtitle`: Additional subtitle text below title
- `retention_days`: Number of days to keep jobs before marking as expired (default: 7)

### Step 4: Generate HTML

Generate the web page HTML file:

```python
generator.generate_html(
    jobs,
    output_path='index.html',
    config=config
)
```

**Output**:
- Single HTML file containing HTML, CSS, and JavaScript
- Mobile-responsive design with card-based layout
- Interactive features (filtering, searching, sorting)
- No external dependencies

### Step 5: Deploy Web Page

Choose deployment mode:

#### Mode A: Local HTML (Quick Start)

**Steps**:
1. Double-click the generated `index.html` file to open in browser
2. Or upload to cloud storage (Baidu Cloud, Nutstore, etc.)
3. Share the link with extraction code
4. View on mobile or desktop

**Advantages**:
- No account registration required
- Completely private (cloud storage extraction code)
- Quick setup (5 minutes)

**Use When**: Testing, temporary use, quick deployment

#### Mode B: GitHub Pages with Password Protection

**Steps**:
1. Register GitHub account (free)
2. Create a new repository
3. Upload the HTML file to the repository
4. Enable GitHub Pages in repository settings
5. Access via: `https://your-username.github.io/repository-name`
6. Enter password to view content

**Advantages**:
- Free deployment
- Global CDN acceleration
- Custom domain support
- HTTPS support
- Password protection

**Use When**: Long-term use, better performance, professional appearance

**Password Protection** (Optional):

```python
generator.generate_html_with_password(
    jobs,
    output_path='index_protected.html',
    password='123456',
    config=config
)
```

Features:
- Password prompt when opening web page
- Password stored in localStorage (client-side)
- Change password entry within the web page
- Forgot password reset method

### Step 6: Update Data (Regular Updates)

When new job data is available:

1. Run job-info-scraper to get updated CSV/JSON
2. Run this skill to regenerate HTML
3. Upload/replace the HTML file
4. The web page will automatically highlight new jobs

**Update Process**:
```bash
# Step 1: Get new job data
python scripts/scraper_example.py
python scripts/parser_example.py
python scripts/filter_example.py

# Step 2: Generate updated HTML
python scripts/generate_html.py

# Step 3: Deploy (replace existing file)
# Upload new index.html to GitHub Pages or cloud storage
```

### Step 7: Use Web Page

Open the web page and use its features:

**View Jobs**:
- Jobs displayed as cards
- Click to expand/collapse details
- Expanded view shows 工作职责 (job responsibilities) and 技能要求 (skill requirements) as structured bullet lists
- Color-coded priority badges (P0=red, P1=orange, P2=yellow, P3=gray)

**Filter Jobs**:
- Filter by priority (P0/P1/P2/P3)
- Filter by job type (Music Operations, Event Planning, etc.)
- Filter by time (Today, Yesterday, This Week, Expired)

**Search Jobs**:
- Real-time search by job title, company, or keywords
- Results update instantly as you type

**Quick Actions**:
- Copy email address to clipboard
- Open email application directly
- View original job posting link

**New Job Alerts**:
- Top banner shows "X new jobs" when new postings are available
- New jobs marked with "新" badge
- Click banner to scroll to today's jobs

**Expired Jobs**:
- Jobs older than 7 days marked as expired
- Expired jobs displayed in gray with "已过期" badge
- Option to hide expired jobs

**Responsive Design**:
- Mobile-optimized single-column layout
- Tablet: two-column layout
- Desktop: three-column layout

## Bundled Resources

### Scripts Directory (`scripts/`)

Contains executable Python scripts for generating HTML:

- `generate_html.py`: Main script for converting CSV/JSON data to HTML

**How to Use Scripts**:

1. **Load Data**:
   ```python
   from scripts.generate_html import HTMLGenerator
   generator = HTMLGenerator()
   jobs = generator.load_csv('job_results.csv')
   ```

2. **Generate HTML**:
   ```python
   generator.generate_html(jobs, 'index.html', config={...})
   ```

3. **Generate Password-Protected HTML**:
   ```python
   generator.generate_html_with_password(jobs, 'index.html', password='123456')
   ```

### Assets Directory (`assets/`)

Contains templates and configuration:

- `templates/job_portal.html`: HTML template with inline CSS and JavaScript
  - Card-based layout
  - Mobile-responsive design
  - Filtering and searching functionality
  - New job alerts
  - Expired job management
  - Single-file delivery (HTML + CSS + JS)

## Web Page Features

### Card Layout

Each job is displayed as a card with:

**Collapsed View** (Default):
- Company name and job title
- Priority badge (color-coded)
- Location and publish date
- Match score
- Basic info (min work days/week, education, internship type)
- Action buttons (Expand Details, Copy Email, View Original)

**Expanded View** (Click "展开详情"):
- Job responsibilities (工作职责): bullet-point list of key duties
- Skill requirements (技能要求): bullet-point list of required skills and qualifications
- Complete job description
- Application requirements
- Email address and contact info
- Original posting link
- Deadline date

### Priority Badges

| Priority | Color | Badge |
|----------|-------|-------|
| P0 | Red | `[P0]` or `🔥` |
| P1 | Orange | `[P1]` |
| P2 | Yellow | `[P2]` |
| P3 | Gray | `[P3]` |

### Time Grouping

Jobs are grouped by time:
- **今日新增**: Jobs published today (with count badge)
- **昨日更新**: Jobs published yesterday
- **本周更新**: Jobs published earlier this week
- **更早**: Jobs from the last 7 days
- **已过期**: Jobs older than 7 days (grayed out)

### Filtering and Searching

**Filters**:
- By priority (P0/P1/P2/P3)
- By job type (Music Operations, Event Planning, Artist Management, etc.)
- By time (Today, Yesterday, This Week, Earlier, Expired)

**Search**:
- Full-text search by job title, company name, or description
- Real-time results (instant update as you type)

**Sorting**:
- By match score (high to low)
- By publish date (new to old)
- By priority (P0 → P1 → P2 → P3)

### New Job Alerts

- Top banner shows "有 X 个新岗位" when new jobs are available
- New jobs marked with "新" badge
- Click banner to scroll to today's jobs
- Badge count updates automatically

### Expired Job Management

- Jobs older than 7 days automatically marked as expired
- Expired jobs displayed in gray with "⚠️ 已过期" badge
- Option to hide expired jobs via time tab
- Configurable retention period

### Responsive Design

**Mobile** (Primary):
- Single column layout
- 100% width cards with 16px padding
- Bottom navigation for filters/search/settings

**Tablet**:
- Two column layout
- 50% width cards

**Desktop**:
- Three column layout
- 33.33% width cards
- Optional sidebar filters

### Quick Actions

- **Expand Details**: Toggle full job description
- **Copy Email**: Copy email address to clipboard
- **Open Email**: Open email application directly
- **View Original**: Open original job posting link in new tab

## Password Protection (Mode B Only)

When generating password-protected HTML:

**Features**:
- Password prompt when opening web page
- Password validation before loading job data
- Change password entry within the web page
- Password stored in localStorage (encrypted)
- Forgot password reset method (clear localStorage)

**Security**:
- Password not stored in HTML file
- Client-side validation only
- Suitable for personal use, not high-security scenarios

**User Experience**:
```
┌─────────────────────────────┐
│                             │
│   🔐 请输入访问密码         │
│                             │
│   [  密码输入框    ]        │
│                             │
│      [  查看岗位  ]          │
│                             │
└─────────────────────────────┘
```

## Configuration Customization

Users can customize the web page by:

**Step 1**: Modify config parameters in `generate_html()` call:

```python
config = {
    'title': '我的实习岗位',           # Change page title
    'subtitle': '2028届本科',          # Change subtitle
    'retention_days': 14,              # Change job retention to 14 days
}
```

**Step 2**: Modify HTML template directly if needed:
- Edit `assets/templates/job_portal.html`
- Change colors, fonts, layout
- Add/remove features
- Modify CSS styles

**Step 3**: Update retention period:
- Jobs older than retention_days are marked expired
- Default: 7 days
- Can be adjusted based on preferences

## Best Practices

1. **Regular Updates**: Update job data daily or weekly for best results
2. **Data Validation**: Ensure CSV/JSON data contains all required fields
3. **Test Locally**: Open HTML file in browser before deploying
4. **Backup Data**: Keep copies of CSV/JSON source files
5. **Mobile Testing**: Test on mobile devices before final deployment
6. **Password Security**: Use strong passwords for protected pages
7. **Clean Expired Jobs**: Periodically remove old data to improve performance

## Common Issues and Solutions

**Issue: HTML file not displaying jobs**

Solution:
- Check if CSV/JSON file path is correct
- Verify data format matches expected schema
- Ensure required fields are present (company, title, location, etc.)
- Note: 工作职责 and 技能要求 are optional — if absent, the expanded view will skip those sections gracefully

**Issue: Web page not responsive on mobile**

Solution:
- Ensure viewport meta tag is present
- Test on actual mobile devices
- Check CSS media queries in template

**Issue: Search not working**

Solution:
- Ensure JavaScript is enabled in browser
- Check browser console for errors
- Verify data is loaded correctly

**Issue: New job alert not showing**

Solution:
- Check publish_date format (should be YYYY-MM-DD)
- Verify browser localStorage is enabled
- Clear browser cache if needed

**Issue: Password not working**

Solution:
- Check password parameter in generate_html_with_password()
- Ensure localStorage is enabled in browser
- Clear localStorage and try again

## Integration with job-info-scraper

This skill is designed to work seamlessly with job-info-scraper:

1. job-info-scraper outputs CSV/JSON job data
2. This skill loads the output and generates HTML
3. Users can view the filtered job listings in a mobile-friendly web page

**Workflow**:
```
job-info-scraper → CSV/JSON → job-info-publisher → HTML → Web Browser
```

**Data Flow**:
- job-info-scraper: Scrape, parse, filter jobs → Export to CSV/JSON
- job-info-publisher: Load CSV/JSON → Generate HTML → Deploy
- End User: Open web page → Browse/Filter/Search jobs

## Limitations

1. **Browser Compatibility**: Requires modern browsers (Chrome 90+, Safari 14+, Firefox 88+, Edge 90+)
2. **Password Protection**: Client-side only, not suitable for high-security scenarios
3. **Data Size**: Large datasets may affect performance
4. **Offline Mode**: Requires internet connection for external links
5. **Real-time Updates**: Requires manual HTML regeneration for data updates

## Future Enhancements

- Email subscription notifications
- Browser push notifications
- Dark mode toggle
- Job bookmarking/favoriting
- Export to Excel functionality
- Data analytics dashboard
- AI-powered job recommendations
- Multi-language support
- Custom domain configuration
- Backend API for real-time updates
