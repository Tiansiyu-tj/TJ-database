from backend.database import engine_metro
from sqlalchemy import text
with engine_metro.connect() as conn:
    cols = conn.execute(text('DESCRIBE `weather`')).fetchall()
    print('weather columns:')
    for c in cols:
        print(c)
