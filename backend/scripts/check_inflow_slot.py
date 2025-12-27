from backend.database import engine_metro
from sqlalchemy import text
with engine_metro.connect() as conn:
    rows = conn.execute(text('SELECT * FROM `inflow` WHERE `Slot` = 0 LIMIT 5')).fetchall()
    print('rows:', len(rows))
    for r in rows:
        print(dict(r._mapping))
