from backend.database import engine_metro
from sqlalchemy import text

with engine_metro.connect() as conn:
    for t in ['station','inflow','timesegment','weather','odflow','outflow','dateinfo','neighbour']:
        try:
            print('\n---',t)
            rows = conn.execute(text(f"DESCRIBE `{t}`")).fetchall()
            for r in rows:
                print(r)
        except Exception as e:
            print('ERR',t,e)
