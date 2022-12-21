import MySQLdb

user = "pass"
user = "result"

def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="happy0623",
        db="user",
        use_unicode=True,
        charset="utf8")
    return con

con = connect()
cur = con.cursor()

if user == "pass":
    cur.execute("""
                CREATE TABLE user.pass
                (id MEDIUMINT NOT NULL AUTO_INCREMENT,
                name VARCHAR(100),
                email VARCHAR(100),
                tel VARCHAR(100),
                passwd VARCHAR(255),
                PRIMARY KEY(id))
                """)

elif user == "result":
    cur.execute("""
                CREATE TABLE user.result
                (id MEDIUMINT NOT NULL AUTO_INCREMENT,
                name_id VARCHAR(100),
                lang mediumint,
                math mediumint,
                engl mediumint,
                PRIMARY KEY(id))
                """)

con.commit()
con.close()