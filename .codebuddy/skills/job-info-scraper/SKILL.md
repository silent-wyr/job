# job-info-scraper Skill

## Metadata
name: job-info-scraper
description: This skill should be used when users need to scrape and filter internship job postings from WeChat official accounts and websites. The skill specializes in retrieving music industry internship positions (music operations, event planning, artist management, etc.) and filtering them based on specific criteria such as location, internship type, graduation year, education level, minimum work days per week, and company priority. The skill outputs filtered job listings in CSV/Excel format for further processing.
version: 1.0.0

## Skill Purpose

This skill provides an automated workflow for scraping internship job postings from music-related companies and platforms. It helps students find suitable internship opportunities by:

1. Retrieving internship postings from WeChat official accounts and recruitment websites
2. Extracting structured job information (position, requirements, company details)
3. Filtering positions based on customizable criteria (location, graduation year, work hours, etc.)
4. Ranking positions by company priority and match score
5. Outputting results in CSV/Excel format

## When to Use This Skill

Use this skill when:
- User needs to search for internship positions from WeChat official accounts and websites
- User needs to filter job postings based on specific student requirements (graduation year, location, work hours)
- User needs to prioritize jobs from specific companies (e.g., Tencent, ByteDance, NetEase Music)
- User needs to extract structured job data from unstructured text
- User wants to export filtered results to CSV/Excel format

## Workflow

### Step 1: Load Configuration

Load the filtering criteria and target companies from configuration files:

- `assets/config/filter_rules.json`: Defines basic filters (location, education, work days), required keywords, company priorities, and scoring rules
- `assets/config/target_companies.json`: Lists target companies with their WeChat accounts, websites, and priority levels

Read these files to understand the filtering logic and data sources.

### Step 2: Collect Job Data

Retrieve internship postings from multiple data sources:

**WeChat Official Accounts:**
- Target company recruitment accounts (e.g., "腾讯招聘", "字节跳动招聘", "网易云音乐招聘")
- Music industry accounts (e.g., "太合音乐集团", "摩登天空ModernSky")

**Recruitment Websites:**
- BOSS直聘: Search for positions matching keywords
- 实习僧: Filter by location and position type
- Other job boards as specified in configuration

**Data Collection Methods:**
- For WeChat: Use web search or API to fetch recent articles
- For websites: Scrape job listing pages and parse HTML
- For search: Use keyword-based queries to find relevant postings

### Step 3: Parse Job Information

For each job posting, extract structured information:

**Basic Fields:**
- Company name and priority level
- Position title
- Work location (check for "北京" or other cities)
- Education requirements
- Graduation year requirements (e.g., "2024届", "2025届", or "不限")
- Min work days per week (e.g., "每周至少4天", "每周不少于3天")
- Internship type (daily internship vs. summer internship)
- Internship duration (e.g., "3个月", "6个月")
- Job responsibilities (工作职责): Key duties extracted from job description
- Skill requirements (技能要求): Required skills and qualifications extracted from job description

**Position Keywords:**
- Match against required keyword list: 音乐活动策划, 经纪人, 经纪助理, 自媒体运营, 新媒体运营, 音乐运营, 演出策划, 演出执行, etc.

**Application Information:**
- Application email or link
- Application deadline
- Application method

Use regex patterns and NLP techniques to extract structured fields from unstructured text.

### Step 4: Apply Filters

Filter jobs based on hard requirements:

**Basic Filters (Must All Be True):**
1. ✅ Location contains "北京" (or specified location)
2. ✅ Internship type is "日常实习" or explicitly allows daily internship
3. ✅ Education level allows undergraduate students (本科 or higher)
4. ✅ Graduation year includes 2028届 or doesn't restrict graduation year
5. ✅ Work days per week ≥ min_work_days_per_week (default: 3), or not explicitly required — ensures the job offers enough working days to meet the student's minimum availability requirement
6. ✅ Job description contains at least one required keyword

Jobs failing any basic filter are excluded from results.

### Step 5: Calculate Match Score

For jobs passing basic filters, calculate a match score:

**Scoring Rules:**
- P0 company (Tencent, ByteDance, NetEase Music): +10 points
- P1 company (Sony Music, Universal Music, Warner Music): +8 points
- P2 company (Taihe Music, Modern Sky, etc.): +5 points
- Explicitly recruiting 2028届 graduates: +5 points
- Work days per week exactly meets min_work_days_per_week: +3 points
- Music major preferred: +2 points
- Relevant experience required: +2 points

Sort results by match score in descending order.

### Step 6: Remove Duplicates

Identify and remove duplicate postings:

- Duplicate criteria: Same company + similar position title + >80% description similarity
- Keep the most recent posting (based on publish date)
- Track removed duplicates in log

### Step 7: Generate Output

Create CSV/Excel file with filtered and ranked results:

**Output Columns:**
- Company Name (公司名称)
- Priority Level (优先级 P0/P1/P2/P3)
- Position Title (岗位名称)
- Work Location (工作地点)
- Education Requirement (学历要求)
- Graduation Year (毕业年份要求)
- Min Work Days Per Week (每周最少工作天数)
- Internship Type (实习类型)
- Job Responsibilities (工作职责)
- Skill Requirements (技能要求)
- Match Score (匹配分数)
- Publish Date (发布日期)
- Application Email (投递邮箱)
- Source (数据来源)
- Original URL (原始链接)

**File Format:**
- Use UTF-8 encoding with BOM for Chinese character support
- Include header row
- Save as `job_results_[timestamp].csv` or `.xlsx`

### Step 8: Generate Summary Report

Create a summary of the scraping results:

- Total number of jobs found
- Number of jobs passing filters
- Distribution by company priority (P0/P1/P2/P3)
- Distribution by position type
- Top 10 recommended positions

Save summary as `job_summary_[timestamp].txt` or display to user.

## Bundled Resources

### Scripts Directory (`scripts/`)

Contains executable Python scripts for specific tasks:

- `scraper/wechat_scraper.py`: Fetch job postings from WeChat official accounts
- `scraper/website_scraper.py`: Scrape job listings from recruitment websites
- `parser/job_parser.py`: Extract structured job information from text
- `filter/job_filter.py`: Apply filtering rules and calculate match scores
- `export/csv_exporter.py`: Generate CSV/Excel output files

**How to Use Scripts:**

1. **WeChat Scraper**: 
   - Input: Company name, WeChat account name
   - Output: List of recent articles with job postings
   - Usage: `python scripts/scraper/wechat_scraper.py --account "腾讯招聘" --days 30`

2. **Website Scraper**:
   - Input: Website URL, search keywords
   - Output: Parsed job listings
   - Usage: `python scripts/scraper/website_scraper.py --url "https://www.zhipin.com" --keywords "音乐运营,演出策划"`

3. **Job Parser**:
   - Input: Raw job description text
   - Output: Structured JSON with extracted fields
   - Usage: `python scripts/parser/job_parser.py --input job_text.txt --output parsed.json`

4. **Job Filter**:
   - Input: Parsed job data JSON, filter rules JSON
   - Output: Filtered and ranked job list
   - Usage: `python scripts/filter/job_filter.py --input parsed.json --rules filter_rules.json --output filtered.json`

5. **CSV Exporter**:
   - Input: Filtered job data JSON
   - Output: CSV/Excel file
   - Usage: `python scripts/export/csv_exporter.py --input filtered.json --output job_results.csv`

### References Directory (`references/`)

Contains reference documentation for understanding filtering logic and domain knowledge:

- `company_list.md`: Complete list of target companies with detailed information (priority levels, business areas, contact info)
- `keyword_mapping.md`: Mapping of job types to keywords and synonyms
- `filter_logic.md`: Detailed explanation of filtering rules and scoring algorithm
- `data_schema.md`: Definition of job data structure and field formats
- `scrape_strategies.md`: Data source strategies and scraping techniques

**When to Load References:**

- Load `company_list.md` when you need to understand target company priorities and identify companies from job postings
- Load `keyword_mapping.md` when parsing job descriptions to identify position types
- Load `filter_logic.md` when implementing or modifying filtering logic
- Load `data_schema.md` when parsing jobs or generating output

### Assets Directory (`assets/`)

Contains configuration files and templates:

- `config/filter_rules.json`: Pre-configured filtering rules (location, education, keywords, company priorities, scoring)
- `config/target_companies.json`: List of target companies with their details
- `templates/job_template.json`: JSON template for job data structure
- `templates/csv_header.csv`: Header row template for CSV output

**Configuration Files:**

These files define the default filtering criteria. Users can modify them to customize the filtering logic without changing code.

## Configuration Customization

Users can customize the skill by modifying configuration files:

**To Change Filtering Criteria:**
1. Edit `assets/config/filter_rules.json`
2. Modify `basic_filters` section to change location, education, min work days requirements
3. Add or remove keywords in `keywords.required` and `keywords.optional` lists
4. Adjust `company_priorities` to reclassify companies
5. Update `scoring_rules` to change match score calculation

**To Add New Target Companies:**
1. Edit `assets/config/target_companies.json`
2. Add new company entry with name, priority, WeChat accounts, and website
3. Save the file

**Example Configuration Update:**

To target Shanghai instead of Beijing:
```json
{
  "basic_filters": {
    "location": ["上海"],
    ...
  }
}
```

To add a new P1 company:
```json
{
  "company_priorities": {
    "P1": ["索尼音乐", "环球音乐", "华纳音乐", "新音乐公司"]
  }
}
```

## Best Practices

1. **Start with Configuration**: Always load and review configuration files before beginning scraping to understand the filtering criteria
2. **Incremental Processing**: Process jobs in batches (e.g., by data source or company) to manage memory usage
3. **Logging**: Log scraping progress, filter results, and any errors for debugging
4. **Data Validation**: Validate extracted fields before proceeding (e.g., ensure company name is not empty)
5. **Rate Limiting**: Implement delays between requests to avoid being blocked by websites
6. **Error Handling**: Handle network errors, missing fields, and malformed data gracefully
7. **Update Configuration**: Review and update configuration files regularly based on user feedback and new requirements

## Common Issues and Solutions

**Issue: No jobs found after filtering**
- Solution: Check filter rules - they may be too strict. Relax some requirements or expand keyword list.

**Issue: Cannot extract graduation year from job description**
- Solution: The description may not mention graduation year explicitly. Assume it's not restricted (matches 2028届 by default).

**Issue: Duplicate jobs in results**
- Solution: Check the deduplication logic. Adjust similarity threshold or add more fields for comparison.

**Issue: WeChat scraping fails**
- Solution: WeChat articles may require authentication. Use alternative data sources or ask user for specific articles.

**Issue: Min work days extraction incorrect**
- Solution: Job descriptions vary in format. Add more regex patterns to handle different phrasings (e.g., "每周至少X天", "每周不少于X天", "每周X天以上").

## Integration with Other Skills

This skill outputs CSV/Excel files that can be used by other skills:

- **job-info-publisher**: Consumes the CSV output to generate web pages displaying job listings
- **email-sender**: Sends filtered job recommendations via email
- **data-analysis**: Analyzes job market trends from scraped data

## Limitations

1. WeChat official account scraping may be limited due to anti-scraping measures
2. Some job postings may not have structured information, requiring manual review
3. Company names may vary (e.g., "腾讯音乐" vs "QQ音乐"), requiring alias mapping
4. Job descriptions may be in various formats, requiring robust parsing logic
5. Real-time updates depend on data source availability

## Future Enhancements

- Add support for more data sources (LinkedIn, Indeed)
- Implement machine learning for better job description parsing
- Add user feedback mechanism to improve filtering accuracy
- Support for automatic scheduling and periodic scraping
- Integration with job application tracking systems
