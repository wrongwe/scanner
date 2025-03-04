MarkDown
# URL Scanner & Analyzer

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

一款智能URL扫描分析工具，可批量检测网站可访问性，自动统计页面文件类型分布，并生成结构化报告。

## ✨ 功能特性

- **智能URL检测**
  - 自动补全URL结尾的`/`
  - 支持HTTP状态码和异常检测
- **可视化进度**
  - 实时进度条显示
  - 动态失败计数器
- **深度分析**
  - 页面文件类型统计
  - 无扩展名文件识别
- **智能报告**
  - 相似结果自动归类
  - 支持多级展示模式
  - 生成Markdown格式报告
 
**使用方法**
准备URL列表文件 1.txt：

 https://example.com
http://test.site
运行扫描器：

Bash
python scanner.py
查看结果报告：
Bash
cat results.txt
📊 示例输出
控制台界面
Text
扫描进度: 100%|██████████| 15/15 [失败:3]
结果已保存至results.txt
报告文件节选
MarkDown
━━━━━━━━ 同类结果统计 ━━━━━━━━
模式 1（出现次数：8 次）
├─ 文件统计：
    .pdf: 5 个
    .zip: 3 个
└─ 全部URL：
    └─ https://example.com
    ├─ https://sample.org
    ├─ https://test.net

━━━━━━━━ 最终统计 ━━━━━━━━
总扫描URL数：15 个
成功数目：12 个
失败数目：3 个
