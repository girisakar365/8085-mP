import sqlite3 as sl


class DB:
    
    def create_table(tbname: str):
        conn = sl.connect("database.db")
        c = conn.cursor()
        c.execute(f"""CREATE TABLE IF NOT EXISTS {tbname} (
                      tbheader text 
                  )""")
        conn.commit()
        conn.close()
    
    def insert_data(tbname: str, data: str):
        conn = sl.connect("database.db")
        c = conn.cursor()
        c.execute(f"INSERT INTO {tbname} VALUES (?)", (data,))
        conn.commit()
        conn.close()
    
    def fetch_data(tbname: str):
        conn = sl.connect("database.db")
        c = conn.cursor()
        c.execute(f"SELECT * FROM {tbname}")
        data = c.fetchall()
        conn.close()
        return data
