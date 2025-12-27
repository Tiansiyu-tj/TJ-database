import requests
from datetime import date, datetime

API = 'http://127.0.0.1:8000/api/metro'

def fetch(url, params=None):
    r = requests.get(url, params=params, timeout=5)
    r.raise_for_status()
    return r.json().get('data', [])


def main():
    today = date.today().isoformat()
    print('today:', today)

    segs = fetch(f'{API}/timesegments', params={'recordDate': today, 'limit': 500})
    print('timeseg count:', len(segs))
    # filter 5:00-23:00
    def slot_hour(s):
        v = s.get('StartTime')
        if v is None:
            return None
        sv = str(v)
        if ':' in sv:
            try:
                return int(sv.split(':')[0])
            except:
                return None
        try:
            fv = float(sv)
            return int(fv / 3600)
        except:
            return None

    slots = [s for s in segs if slot_hour(s) is not None]
    slots = [s for s in slots if 5 <= slot_hour(s) <= 23]
    slots = sorted(slots, key=lambda s: s['StartTime'])
    print('usable slots (today):', len(slots))

    # 如果当天没有可用 slot，尝试使用数据库中最近的可用日期
    if not slots:
        all_segs = fetch(f'{API}/timesegments', params={'limit': 1000})
        dates = sorted({s.get('recordDate') for s in all_segs if s.get('recordDate')})
        latest = dates[-1] if dates else None
        print('latest available date:', latest)
        if latest:
            segs = [s for s in all_segs if s.get('recordDate') == latest]
            slots = [s for s in segs if slot_hour(s) is not None and 5 <= slot_hour(s) <= 23]
            slots = sorted(slots, key=lambda s: s['StartTime'])
            print('usable slots (latest):', len(slots))

    now = datetime.now()
    currentSlotIdx = -1
    for i, s in enumerate(slots):
        st = slot_hour(s)
        et = slot_hour({'StartTime': s.get('EndTime')})
        if et is None and st is not None:
            et = st + 1
        if st is None or et is None:
            continue
        ch = now.hour
        if ch >= st and ch < et:
            currentSlotIdx = i
            break
    useSlots = slots[:currentSlotIdx+1] if currentSlotIdx >= 0 else slots

    print('useSlots:', [s['Slot'] for s in useSlots][:10])

    inflowSeries = []
    outflowSeries = []
    inflowResults = []
    outflowResults = []
    for s in useSlots:
        inflows = fetch(f'{API}/inflow', params={'Slot': s['Slot'], 'limit': 10000})
        outflows = fetch(f'{API}/outflow', params={'Slot': s['Slot'], 'limit': 10000})
        inflowResults.append(inflows)
        outflowResults.append(outflows)
        inf_sum = sum(int(it.get('Tot_IF') or 0) for it in inflows)
        out_sum = sum(int(it.get('Tot_OF') or 0) for it in outflows)
        inflowSeries.append(inf_sum)
        outflowSeries.append(out_sum)

    print('hours:', [f"{slot_hour(s)}:00" for s in useSlots[:10]])
    print('inflowSeries sample:', inflowSeries[:10])
    print('outflowSeries sample:', outflowSeries[:10])

    if inflowResults:
        curr = inflowResults[-1]
        top = sorted([{'stationID': it.get('stationID'), 'Tot_IF': int(it.get('Tot_IF') or 0)} for it in curr], key=lambda x: x['Tot_IF'], reverse=True)[:10]
        print('top stations:', top[:5])

    # 使用实际用于时段选择的日期（若用 latest 则替换 today）
    used_date = today
    if (not fetch(f'{API}/timesegments', params={'recordDate': today, 'limit': 1})): 
        all_segs = fetch(f'{API}/timesegments', params={'limit': 1000})
        dates = sorted({s.get('recordDate') for s in all_segs if s.get('recordDate')})
        if dates:
            used_date = dates[-1]
    weather = fetch(f'{API}/weather', params={'recordDate': used_date, 'limit': 10})
    print('weather records:', len(weather))

    topod = fetch(f'{API}/top-od', params={'limit': 10})
    print('top od count:', len(topod))

if __name__ == '__main__':
    main()
