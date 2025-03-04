import requests
import certifi
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from bs4 import BeautifulSoup
from collections import defaultdict

# 禁用SSL警告（生产环境慎用）
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 全局Session配置
SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
})
SESSION.verify = certifi.where()  # 启用证书验证

def normalize_url(raw_url):
    """智能URL标准化"""
    url = raw_url.strip()
    # 协议补全
    if not url.startswith(('http://', 'https://')):
        url = f'http://{url}'  # 默认HTTP协议
    # 端口检测与补全
    if '://' in url:
        protocol, rest = url.split('://', 1)
        host_part = rest.split('/')[0]
        if ':' not in host_part:
            port = 443 if protocol == 'https' else 80
            url = f"{protocol}://{host_part}:{port}/{rest.split('/', 1)[1] if '/' in rest else ''}"
    return url

def process_links(soup):
    links = soup.select('a[href]')
    file_stats = defaultdict(int)
    for link in links:
        href = link['href']
        if not href.endswith('/'):
            ext = href.split('.')[-1].lower() if '.' in href else "无扩展名"
            file_stats[ext] += 1
    return dict(file_stats)


def check_url(url):
    try:
        response = SESSION.get(url, timeout=(3, 5), allow_redirects=True, verify=False)
        if response.status_code == 200:
            if 'html' in response.headers.get('Content-Type', ''):
                soup = BeautifulSoup(response.text, 'lxml')
                stats = process_links(soup)
                return (200, stats, url)
            return (200, {'无扩展名': 0}, url)  # 非HTML内容处理
        return (response.status_code, None, url)
    except Exception as e:
        return (str(e), None, url)


if __name__ == "__main__":
    with open('1.txt') as f:
        raw_urls = [line.strip() for line in f if line.strip()]

    urls = [normalize_url(url) for url in raw_urls]
    total = len(urls)
    failed = 0
    pattern_counter = defaultdict(lambda: {'count': 0, 'urls': [], 'stats': None})

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_url, url): url for url in urls}

        with tqdm(total=total, desc="扫描进度", unit="URL",
                  bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [失败:{postfix}]",
                  postfix=0) as pbar:

            for future in as_completed(futures):
                status_code, file_stats, url = future.result()

                if status_code == 200:
                    stats_str = "\n".join(
                        f"    .{ext}: {count} 个" if ext != "无扩展名"
                        else f"    {ext}: {count} 个"
                        for ext, count in file_stats.items()
                    ) if file_stats else "    未找到文件"

                    pattern_counter[stats_str]['count'] += 1
                    pattern_counter[stats_str]['urls'].append(url)
                    pattern_counter[stats_str]['stats'] = stats_str
                else:
                    failed += 1
                    pbar.postfix = failed

                pbar.update(1)

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