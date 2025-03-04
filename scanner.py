import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
from collections import defaultdict


def format_stats(file_stats):
    """将文件统计转换为易读格式"""
    if not file_stats:
        return "    未找到文件"
    return "\n".join([f"    .{ext}: {count} 个" if ext != "无扩展名" else f"    {ext}: {count} 个"
                      for ext, count in file_stats.items()])


def check_url(url):
    """检测URL并返回状态码和统计结果"""
    try:
        formatted_url = url if url.endswith('/') else url + '/'
        response = requests.get(formatted_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return (200, process_links(soup))
        return (response.status_code, None)
    except Exception as e:
        return (str(e), None)


def process_links(soup):
    """解析页面链接"""
    links = soup.find_all('a')
    file_stats = defaultdict(int)
    for link in links:
        href = link.get('href')
        if href and not href.endswith('/'):
            ext = href.split('.')[-1].lower() if '.' in href else "无扩展名"
            file_stats[ext] += 1
    return dict(file_stats)


if __name__ == "__main__":
    # 读取URL列表
    with open('1.txt') as f:
        urls = [line.strip() for line in f if line.strip()]

    total = len(urls)
    failed = 0
    success_data = []
    pattern_counter = defaultdict(lambda: {'count': 0, 'urls': []})

    # 进度条配置（仅显示失败数）
    with tqdm(total=total, desc="扫描进度", unit="URL",
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [失败:{postfix}]",
              postfix=0) as pbar:

        for url in urls:
            status_code, file_stats = check_url(url)

            if status_code == 200:
                stats_str = format_stats(file_stats)
                pattern_key = hash(stats_str)  # 使用哈希值作为特征标识
                pattern_counter[pattern_key]['count'] += 1
                pattern_counter[pattern_key]['urls'].append(url)
                pattern_counter[pattern_key]['stats'] = stats_str
                success_data.append(f"[有效] {url}\n{stats_str}")
            else:
                failed += 1
                pbar.postfix = failed  # 动态更新失败数

            pbar.update(1)
            time.sleep(0.01)

    # 生成归类报告
    report = []
    # 按模式出现次数排序
    sorted_patterns = sorted(pattern_counter.values(), key=lambda x: x['count'], reverse=True)

    report = []
    report.append("━━━━━━━━ 同类结果统计 ━━━━━━━━")
    for idx, pattern in enumerate(sorted_patterns, 1):
        # 显示全部URL
        url_list = "\n".join([f"    ├─ {url}" for url in pattern['urls']])
        url_list = url_list.replace("    ├─", "└─", 1) if url_list else ""  # 首行替换为└─

        report.append(f"模式 {idx}（出现次数：{pattern['count']} 次）")
        report.append(f"├─ 文件统计：\n{pattern['stats']}")
        report.append(f"└─ 全部URL：\n{url_list}\n")
    # 写入文件
    with open('results.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        f.write(f"\n\n━━━━━━━━ 最终统计 ━━━━━━━━\n总URL数：{total} 个\n失败数目：{failed} 个")

    print(f"\n结果已保存至results.txt，失败URL仅统计数量")