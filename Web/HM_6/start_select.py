import sqlite3


def execute_query(db: str, script:str) -> list:
    with open(script, 'r') as sql_file:
        sql_code = sql_file.read()
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(sql_code)
        return cur.fetchall()


database_name = 'new_sql_hm.sqlite'
sql_script = r'selects\query_12.sql'

print(execute_query(database_name, sql_script))
