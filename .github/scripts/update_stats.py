#!/usr/bin/env python3
import json
import re
import urllib.request
from datetime import datetime

# Zenodo 记录 ID 映射
RECORDS = {
    "v1.5.0": "21859450",
    "v1.4.0": "21443737",
    "v1.3.0": "21030804",
    "v1.2.0": "20726229",
    "v1.1.1": "20421174",
    "v1.1.0": "20406615",
    "v1.0.0": "20271957",
    "v1.1": "22974921",
    "v1.0": "22962538",
    "v1": "20085612",
}

def fetch_stats(record_id):
    url = f"https://zenodo.org/api/records/{record_id}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("views", 0), data.get("downloads", 0)
    except:
        return "-", "-"

def update_stats():
    today = datetime.now().strftime("%Y-%m-%d")
    
    with open("stats.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    for version, record_id in RECORDS.items():
        views, downloads = fetch_stats(record_id)
        # 更新表格行
        pattern = rf"(<td>{version}</td>\s*<td>.*?</td>\s*<td>)[^<]+(</td>\s*<td>)[^<]+(</td>\s*<td>)[^<]+(</td>)"
        replacement = rf"\g<1>{views}\g<2>{downloads}\g<3>{today}\g<4>"
        content = re.sub(pattern, replacement, content)
    
    with open("stats.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ 统计数据已更新")

if __name__ == "__main__":
    update_stats()
