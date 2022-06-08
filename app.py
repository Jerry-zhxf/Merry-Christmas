# -*- coding = utf-8 -*-

import pymysql
from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def index():
    db = pymysql.connect(host='localhost',  user='root',  password='123456', database='PowerGrid')
    c = db.cursor()

    sql =  "SELECT * FROM Articles ORDER BY article_time DESC;"
    c.execute(sql)
    data = c.fetchall()

    c.close()
    db.close()

    return render_template("index.html", articles = data)

if __name__ == '__main__':
    app.run(port=4000, debug=False)