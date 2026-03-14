@echo off
REM 一键运行完整工作流
REM 用法：双击 run_workflow.bat

echo ========================================
echo   实习招聘信息工作流 - 自动执行
echo ========================================
echo.

echo [1/2] 爬取和筛选招聘信息...
cd "%~dp0.codebuddy\skills\job-info-scraper"
python scripts/scraper_example.py
python scripts/parser_example.py
python scripts/filter_example.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 爬取失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo [2/2] 生成岗位门户网页...
cd "..\..\..\codebuddy\skills\job-info-publisher"
python scripts/generate_html.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 网页生成失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 工作流执行完成！
echo ========================================
echo.
echo 输出文件位置：
echo - 岗位数据：.codebuddy\skills\job-info-scraper\output\
echo - 网页文件：.codebuddy\skills\job-info-publisher\index.html
echo.
echo 提示：
echo 1. 双击 index.html 在浏览器中查看
echo 2. 或上传到云盘分享给手机
echo.

pause
