from backend.database import engine_metro
from sqlalchemy import text
with engine_metro.connect() as conn:
    print('COUNT inflow', conn.execute(text('SELECT COUNT(*) FROM `inflow`')).fetchone()[0])
    print('COUNT outflow', conn.execute(text('SELECT COUNT(*) FROM `outflow`')).fetchone()[0])
    print('Sample inflow rows:')
    sample = conn.execute(text('SELECT * FROM `inflow` LIMIT 5')).fetchall()
    for r in sample:
        print(r._mapping)
