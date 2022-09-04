def get_users():
    cur = connection.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    print(rows)
    return rows
