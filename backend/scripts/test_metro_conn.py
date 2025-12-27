from backend.database import engine_metro
from sqlalchemy import text

try:
    with engine_metro.connect() as conn:
        print('Connected to shanghai_metro OK')
        res = conn.execute(text('SHOW TABLES')).fetchall()
        print('Tables:', [r[0] for r in res])
        for tbl in ['Station','station','metro_station','Inflow','inflow']:
            try:
                cnt = conn.execute(text(f'SELECT COUNT(*) FROM `{tbl}`')).fetchone()
                print(f'COUNT {tbl}:', cnt[0])
                sample = conn.execute(text(f'SELECT * FROM `{tbl}` LIMIT 3')).fetchall()
                print(f'SAMPLE {tbl}:', sample)
            except Exception as e:
                print(f'No table {tbl} or error: {e}')
except Exception as e:
    print('Connection failed:', e)
