import sqlite3

creation_table_str = """
    CREATE TABLE IF NOT EXISTS TEMPERATURE (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id TEXT,
        temperature REAL,
        datetime TEXT,
        location TEXTc
    );
"""

check_if_table = """
    SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?;
"""

insertion_sample_data = """
    INSERT INTO TEMPERATURE VALUES (null, ?, ?, ?, ?);
"""

if __name__ == "__main__":
    conn = sqlite3.connect('database_sql.db')
    cur = conn.cursor()
    cur.execute(check_if_table, ("TEMPERATURE",))
    if cur.fetchone()[0] == 1:
        print('TEMPERATURE table already exists.')
    else:
        cur.execute(creation_table_str)
        conn.commit()
        print("TEMPERATURE table created successfully.")

    data_samples = [
        ('t1', 32.4, '2019-10-01 08:18:00', '1st Floor, 4th Engineering Building, KoreaTech'),
        ('t2', 34.9, '2019-10-01 08:20:00', '3st Floor, 2th Engineering Building, KoreaTech')
    ]
    cur.executemany(insertion_sample_data, data_samples)
    conn.commit()
    conn.close()
