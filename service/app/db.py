# service/app/db.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DSN = os.getenv('DATABASE_URL')

_conn = None

def get_db():
    global _conn
    if _conn is None:
        if not DSN:
            raise RuntimeError('DATABASE_URL is not set')
        _conn = psycopg2.connect(DSN)
        _conn.autocommit = False
    return _conn

# простая инициализация таблицы
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id serial PRIMARY KEY,
        name text NOT NULL
    );
    ''')
    conn.commit()
    cur.close()