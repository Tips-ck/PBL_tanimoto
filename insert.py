import MySQLdb
from werkzeug.security import generate_password_hash as gph

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
    pass_tani = gph("happy")
    pass_yuki = gph("yuki")
    pass_kazu = gph("kazu")
    pass_megu = gph("megu")
    pass_saki = gph("saki")

    list=[
          ["たに","tani@gmail.com","000123456",pass_tani],
          ["ゆうき","yuki@gmail.com","010123456",pass_yuki],
          ["かず","kazu@gmail.com","020123456",pass_kazu],
          ["めぐ","megu@gmail.com","030123456",pass_megu],
          ["さき","saki@gmail.com","040123456",pass_saki],
         ]

    for i in range(len(list)):
        cur.execute("""
                    INSERT INTO user.pass
                    (name, email, tel, passwd)
                    VALUES (%(name)s, %(email)s, %(tel)s, %(passwd)s)
                    """,
                    {"name":list[i][0], "email":list[i][1], "tel":list[i][2], "passwd":list[i][3]})

elif user == "result":
    list=[
      ["tani@gmail.com",93,95,92],
      ["yuki@gmail.com",95,91,93],
      ["megu@gmail.com",75,72,73],
      ["kazu@gmail.com",87,77,65],
      ["saki@gmail.com",83,77,91],
      ["yuki@gmail.com",63,45,35],
      ["kazu@gmail.com",35,73,54],
      ["saki@gmail.com",68,79,97],
      ["tani@gmail.com",100,100,100],
      ["megu@gmail.com",46,47,67],
      ["kazu@gmail.com",37,47,47],
      ["yuki@gmail.com",78,46,78],
      ["megu@gmail.com",45,73,76],
      ["kazu@gmail.com",54,27,82],
      ["saki@gmail.com",25,82,99],
      ["tani@gmail.com",45,35,53],
      ["yuki@gmail.com",86,86,45],
      ["megu@gmail.com",45,33,95],
      ["kazu@gmail.com",75,45,67],
      ["saki@gmail.com",35,63,56],
      ["yuki@gmail.com",56,63,36],
      ["kazu@gmail.com",77,37,86],
      ["saki@gmail.com",59,95,85],
      ["tani@gmail.com",99,59,95],
      ["megu@gmail.com",85,58,95],
      ["kazu@gmail.com",58,87,67],
      ["yuki@gmail.com",85,85,85],
      ["megu@gmail.com",85,58,87],
      ["kazu@gmail.com",85,57,87],
      ["saki@gmail.com",98,98,89]
     ]

    for i in range(len(list)):
        cur.execute("""
                    INSERT INTO user.result
                    (name_id, lang, math, engl)
                    VALUES (%(name_id)s, %(lang)s, %(math)s, %(engl)s)
                    """,
                    {"name_id":list[i][0], "lang":list[i][1], "math":list[i][2], "engl":list[i][3]})
con.commit()
con.close()