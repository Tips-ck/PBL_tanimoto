from flask import Flask, request, redirect, render_template, session, jsonify, make_response
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
from datetime import timedelta
import html
import secrets
import MySQLdb
from dicttoxml import dicttoxml
import json

def connect():
    con = MySQLdb.connect(
        host="localhost",
        user='root',
        passwd='aaa',
        db='user',
        use_unicode=True,
        charset="utf8")
    return con

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(minutes=60)

@app.route("/")
def root_page():
        return redirect("make")#make

@app.route("/home")
def home():
    if "name" in session:
        if session["admin"] == 1:
            return render_template("success.html",
                                    name=html.escape(session["name"]),
                                    email=html.escape(session["email"]),
                                    tel=html.escape(session["tel"]),
                                    admin="<a href=\"admin\">ユーザ情報一覧</a>")
        else:
            return render_template("success.html",
                                    name=html.escape(session["name"]),
                                    email=html.escape(session["email"]),
                                    tel=html.escape(session["tel"]))
            
    else:
        return redirect("login")

@app.route("/admin")
def admin():
    if "admin" in session:
        if session["admin"] == 1:
            con = connect()
            cur = con.cursor()
            cur.execute("""
                        SELECT name,email,tel
                        FROM pass
                        """)
            res=""
            for row in cur:
                res = res +"<table border=\"1\" align=\"center\">\n"
                res = res +"\t<tr><td align=\"right\">名前</td><td>"+html.escape(row[0])+"</td></tr>\n"
                res = res +"\t<tr><td align=\"right\">メールアドレス</td><td>"+html.escape(row[1])+"</td></tr>\n"
                res = res +"\t<tr><td align=\"right\">電話番号</td><td>"+html.escape(row[2])+"</td></tr>\n"
                res = res + "</table>"
            con.close()
            return render_template("res.html",res=res)
        else:
            return redirect("home")
    else:
        return redirect("login")

@app.route("/make", methods=["GET","POST"])
def make():
    if request.method == "GET":
        return render_template("make.html")
    elif request.method == "POST":
        email = request.form["email"]
        passwd = request.form["passwd"]
        name = request.form["name"]
        tel = request.form["tel"]
        hashpass = gph(passwd)
        con  = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT * FROM pass WHERE email=%(email)s
                    """,{"email":email})
        data=[]
        for row in cur:
            data.append(row)
        if len(data)!=0:
            return render_template("make.html", msg="既に存在するメールアドレスです")
        con.commit()
        con.close()
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    INSERT INTO pass
                    (email,passwd,tel,name)
                    VALUES (%(email)s,%(hashpass)s,%(tel)s,%(name)s)
                    """,{"email":email,"hashpass":hashpass,"tel":tel,"name":name})
        con.commit()
        con.close()
        return render_template("info.html", email=email, passwd=passwd, name=name, tel=tel)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        session.clear()
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form["email"]
        passwd = request.form["passwd"]
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT passwd,name,email,tel,admin
                    FROM pass
                    WHERE email=%(email)s
                    """,{"email":email})
        data=[]
        for row in cur:
            data.append([row[0],row[1],row[2],row[3],row[4]])
        if len(data)==0:
            con.close()
            return render_template("login.html", msg="IDが間違っています")
        if cph(data[0][0],passwd):
            session["name"] = data[0][1]
            session["email"] = data[0][2]
            session["tel"] = data[0][3]
            session["admin"] = 0 if data[0][4] is None else data[0][4]
            con.close()
            return redirect("home")
        else:
            con.close()
            return render_template("login.html", msg="パスワードが間違っています")

@app.route("/input",methods=["GET","POST"])
def input():
    if request.method == "GET":
        token = secrets.token_hex()
        session["home"] = token
        return render_template("input.html",token =token)
    elif request.method == "POST" and session["home"] == request.form["home"]:
        name_id = session["email"]
        lang = request.form["lang"]
        math = request.form["math"]
        engl = request.form["engl"]
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    INSERT INTO result
                    (name_id,lang,math,engl)
                    VALUES (%(name_id)s,%(lang)s,%(math)s,%(engl)s)
                    """,{"name_id":name_id, "lang":lang,"math":math,"engl":engl})
        con.commit()
        con.close()
        return render_template("info_input.html", lang=lang, math=math,engl=engl)

@app.route("/browse",methods=["GET","POST"])
def browse():
    if request.method == "GET":
        return render_template("which.html")
    elif request.method == "POST":
        if request.form["which"] == "own":
            return redirect("api_own")
        elif request.form["which"] == "others":
            return redirect("subject") 

@app.route("/api_own",methods=["GET","POST"])
def api_own():
    if request.method == "GET":
        return render_template("format.html")
    elif request.method == "POST":
        num = session["email"]
        name = session["name"]
        form = request.form["format"]

    con = connect()
    cur = con.cursor()
    cur.execute("""
                SELECT lang, math, engl
                FROM result
                WHERE name_id=%(id)s
                """,{"id":num})

    res = {}
    tmpa=[]
    for row in cur:
        dic={}
        dic["lang"] = row[0]
        dic["math"] = row[1]
        dic["engl"] = row[2]
        tmpa.append(dic)
    
    res["content"] = tmpa

    if form == "XML":
        xml = dicttoxml(res)
        resp = app.make_response(xml)
        resp.mimetype = "text/xml"
        return resp
    elif form == "JSON":
        res = json.dumps(res,indent=2,ensure_ascii=False)
        return render_template("api.html",res=res,msg=name+"さんの結果を"+form+"形式で表示")

@app.route("/subject",methods=["GET","POST"])
def subject():
    if request.method == "GET":
        return render_template("subject.html")
    elif request.method == "POST":
        session["subj"]=request.form["subj"]
        return redirect("rank") 

@app.route("/rank")
def api_json():
    subj=session["subj"]
    con = connect()
    cur = con.cursor()
    res ={}
    tmpa=[]
    sum = 0
    count = 0

    if  subj == "lang":
        cur.execute("""
                    SELECT lang
                    FROM result
                    ORDER BY lang DESC
                    """)
        for row in cur:
            dic={}
            dic["lang"] = row[0]
            sum += row[0]
            count += 1
            tmpa.append(dic)

    elif subj == "math":
        cur.execute("""
                    SELECT math
                    FROM result
                    ORDER BY math DESC
                    """)
        for row in cur:
            dic={}
            dic["math"] = row[0]
            sum += row[0]
            count += 1
            tmpa.append(dic)

    elif subj == "engl":
        cur.execute("""
                    SELECT engl
                    FROM result
                    ORDER BY engl DESC
                    """)
        for row in cur:
            dic={}
            dic["engl"] = row[0]
            sum += row[0]
            count += 1
            tmpa.append(dic)
    
    res["content"] = tmpa
    con.commit()
    con.close()

    if subj=="lang":
        subj="国語"
    elif subj=="math":
        subj="数学"
    elif subj=="engl":
        subj="英語"
    res_avg=round(sum/count,2)

    return render_template("api.html", res=res, msg=subj+"の得点が高い順", msg_avg=subj+"の平均点:", res_avg=res_avg)

@app.after_request
def apply_cachingg(response):
    response.headers["X-Frame-Optins"] = "SAMEORIGIN"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0")