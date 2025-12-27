from backend.database import engine_metro
from sqlalchemy import text

with engine_metro.connect() as conn:
    cols = conn.execute(text('DESCRIBE `station`')).fetchall()
    print('station columns:')
    for c in cols:
        print(c)

    cols = conn.execute(text('DESCRIBE `inflow`')).fetchall()
    print('\ninflow columns:')
    for c in cols:
        print(c)

    cols = conn.execute(text('DESCRIBE `timesegment`')).fetchall()
    print('\ntimesegment columns:')
    for c in cols:
        print(c)
