import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    conn = sqlite3.connect('film_and_award_data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql = "select distinct f.*, a.eventName, a.awardName,a.Category from films f join awards a on f.Title = a.Title"
    condition = ""
    if request.method == "POST":
        film_name = request.form["condition"]
        condition = " where f.Title like " + "'%" + film_name + "%'"
    cur.execute(sql + condition)
    rows_films = cur.fetchall()
    conn.close()
    return render_template('index.html', rows_films = rows_films)
