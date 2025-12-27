from backend.routers.metro_metro import stations, inflow, outflow, weather

print('stations count sample:', len(stations(limit=5)['data']))
print('inflow sample count:', len(inflow(limit=3)['data']))
print('outflow sample count:', len(outflow(limit=3)['data']))
print('weather sample count:', len(weather(limit=3)['data']))
