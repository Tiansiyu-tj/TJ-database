#!/usr/bin/env python3
"""Simple script to query time endpoints and print counts and small samples."""
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

BASE = 'http://127.0.0.1:8000/api/time'

def fetch(path):
    url = f"{BASE}/{path}"
    try:
        with urlopen(Request(url, headers={'User-Agent': 'check-time'}), timeout=10) as r:
            return json.load(r)
    except (HTTPError, URLError) as e:
        print(f"ERROR fetching {url}: {e}")
        return None

if __name__ == '__main__':
    for p in ['dateinfo?recordDate=2017-05-10', 'weather?recordDate=2017-05-10', 'segments?recordDate=2017-05-10']:
        data = fetch(p)
        if data is None:
            print(p, '=> NO DATA')
            continue
        cnt = len(data) if hasattr(data, '__len__') else 'unknown'
        print('\n', p, 'COUNT=', cnt)
        if isinstance(data, list):
            print(json.dumps(data[:3], ensure_ascii=False, indent=2))
        elif isinstance(data, dict):
            print('keys=', list(data.keys())[:10])
            for k, v in data.items():
                if isinstance(v, list) and len(v) > 0:
                    print(f'sample for {k}:', json.dumps(v[:3], ensure_ascii=False, indent=2))
                    break
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
