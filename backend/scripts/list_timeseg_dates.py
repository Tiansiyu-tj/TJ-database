import urllib.request, json
url = 'http://127.0.0.1:8000/api/metro/timesegments?limit=500'
with urllib.request.urlopen(url, timeout=5) as r:
    j = json.load(r)
    data = j.get('data', [])
    print('rows', len(data))
    dates = sorted({d.get('recordDate') for d in data if d.get('recordDate')})
    print('sample dates:', dates[:20])
