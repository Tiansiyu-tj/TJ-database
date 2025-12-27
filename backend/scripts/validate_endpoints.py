from backend.routers.metro_metro import stations, timesegments, inflow, outflow, weather, top_od

print('stations:', len(stations(limit=10)['data']))
print('timesegments:', len(timesegments(limit=10)['data']))
print('inflow slot 0:', len(inflow(Slot=0, limit=5)['data']))
print('outflow slot 0:', len(outflow(Slot=0, limit=5)['data']))
print('weather:', len(weather(limit=5)['data']))
print('top_od:', len(top_od(limit=5)['data']))
