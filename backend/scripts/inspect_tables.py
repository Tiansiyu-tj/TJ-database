from backend.database import engine_metro
from sqlalchemy import text

try:
    with engine_metro.connect() as conn:
        r = conn.execute(text('SELECT * FROM `inflow` LIMIT 1')).first()
        print('inflow row:', r)
        if r is not None:
            try:
                print('inflow keys:', list(r._mapping.keys()))
            except Exception:
                pass
        r2 = conn.execute(text('SELECT * FROM `station` LIMIT 1')).first()
        print('station row:', r2)
        if r2 is not None:
            try:
                print('station keys:', list(r2._mapping.keys()))
            except Exception:
                pass
except Exception as e:
    print('ERR', e)
