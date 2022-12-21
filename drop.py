import MySQLdb

user = "pass"
user = "result"

def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="aaa",
        db="user",
        use_unicode=True,
        charset="utf8")
    return con

con = connect()
cur = con.cursor()

if user == "pass":
    cur.execute("""
                DROP TABLE user.pass
                """)

elif user == "result":
    cur.execute("""
                DROP TABLE user.result
                """)

con.commit()
con.close()