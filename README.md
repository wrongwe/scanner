```markdown
# URL Scanner & Analyzer

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Open Source](https://img.shields.io/badge/Open%20Source-💖-lightgrey.svg)

一款智能URL扫描分析工具，可批量检测网站可访问性，自动统计页面文件类型分布，并生成结构化报告。

---

## ✨ 核心功能

### 🎯 智能URL检测
- 自动补全URL结尾的 `/`
- 支持HTTP状态码和异常检测
- 多线程并发处理

### 📊 可视化分析
- 实时进度条显示（基于 `tqdm`）
- 动态失败计数器
- 页面文件类型统计（`.pdf`, `.zip` 等）
- 无扩展名文件识别

### 📂 智能报告
- 相似结果自动聚类
- 多层级展示模式
- Markdown格式结构化输出

---

## 🚀 快速开始

### 准备工作
1. 创建 `1.txt` 文件并添加待检测URL：
```text
https://example.com
http://test.site
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

### 运行扫描器
```bash
python scanner.py
```

### 查看结果
```bash
cat results.txt
```

---

## 📝 输出示例

### 控制台界面
```text
扫描进度: 100%|██████████| 15/15 [失败:3]
结果已保存至 results.txt
```

### 报告文件节选
```markdown
━━━━━━━━ 同类结果统计 ━━━━━━━━
🔍 模式 1（出现次数：8 次）
├─ 文件统计：
│    ▫️ .pdf: 5 个
│    ▫️ .zip: 3 个
└─ 全部URL：
     ▸ https://example.com
     ▸ https://sample.org
     ▸ https://test.net

━━━━━━━━ 最终统计 ━━━━━━━━
✅ 总扫描URL数：15 个
🟢 成功数目：12 个
🔴 失败数目：3 个
```

