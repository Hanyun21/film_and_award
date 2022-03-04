# film_and_award
This web application is based on Pyhotn and Flask to parse use IMBD films and their awards data.

Firstly, I created a main folder called 'films', and input ls in the terminal to check where I am. Next, I cd into the folder and excute the following command
     pyenv local 3.7.0
     python3 -m venv .venv
     source .venv/bin/activate
     pip install --upgrade pip

Then, I installed the Flask with
     pip install flask

Secondly, in order to parse my csv files, I created a new folder called film_data and uploaded my files into the folder -- 'IMDB_Film.csv' and 'award.csv'. Before I imported my
data, I should create my database first
     touch polar_bear_data.db

So I chould create a Python file called 'parse.py' and put the following code in it to import my data
     import csv
     import sqlite3

     # open the connection to the database
     conn = sqlite3.connect('film_and_award_data.db')
     cur = conn.cursor()

     # drop the data from the table so that if we rerun the file, we don't repeat values
     conn.execute('DROP TABLE IF EXISTS films')
     print("films table dropped successfully");
     conn.execute('DROP TABLE IF EXISTS awards')
     print("awards table dropped successfully");

     # create table again
     conn.execute('CREATE TABLE films (Title TEXT, Year INTEGER, Grading TEXT, Duration INTEGER, Score REAL, Genre1 TEXT, Genre2 TEXT, Genre3 TEXT, Gross Real)')
     print("films table created successfully");
     conn.execute('CREATE TABLE awards (eventName TEXT, awardName TEXT, Title TEXT, Year INTEGER, Category Text)')
     print("status table created successfully");

     # open the file to read it into the database
     with open('film_data/IMDB_Films.csv', newline='') as f:
     reader = csv.reader(f, delimiter=",")
     next(reader) # skip the header line
     for row in reader:
          print(row)
          if row[0]: 
               try:
                    Title = row[0]
                    Year = int(row[1])
                    Grading = row[2]
                    Duration = int(row[3])
                    Score = float(row[4])
                    Genre1 = row[6]
                    Genre2 = row[7]
                    Genre3 = row[8]
                    Gross = float(row[9])
                    cur.execute('INSERT INTO films VALUES (?,?,?,?,?,?,?,?,?)', (Title, Year, Grading, Duration, Score, Genre1, Genre2, Genre3, Gross))
                    
               except:
                    continue
          else:
               break
     print("data parsed successfully");
     with open('film_data/awards.csv', newline='') as f:
     reader = csv.reader(f, delimiter=",")
     next(reader) # skip the header line
     for row in reader:
          if row[0]: 
               print(row)
               try:
                    eventName = row[1]
                    awardName = row[2]
                    Title = row[8]
                    Year = int(row[3])
                    Category = row[6]
                    cur.execute('INSERT INTO awards VALUES (?,?,?,?,?)', (eventName, awardName, Title, Year, Category))
               except:
                    continue  
          else:
               break
     print("data parsed successfully");
     conn.commit()
     conn.close()

The next, I put the following code in the terminal to import my data, and it took some time
     python3 parse_csv.py

Furthermore, I created a index.html file in a new folder called 'templates', and put the following code in it, so that I could display my data on the web page with a search function
<!--      <html>
          <head>
               <title>Films and Their Award Details</title>
          </head>
               <style>
                    table th{width:50px;height:50px;background:blue;}
               </style>
          <body>
               <h1 align="center">IMDB Films Details and Their Awards</h1>
               <form action="/" method="post">
                    <h2>Search for a film:
                         <input type="text" name='condition' style="width:500px;height:40px;"/>
                         <input type="submit" value="Search" style="height:40px;">
                    </h2>
               </form>
               <table>
                    <tr>
                         <th style="width:500px" align="center">Title</th>
                         <th style="width:100px" align="center">Year</th>
                         <th style="width:100px" align="center">Grading</th>
                         <th style="width:100px" align="center">Duration</th>
                         <th style="width:100px" align="center">Score</th>
                         <th style="width:100px" align="center">Genre1</th>
                         <th style="width:100px" align="center">Genre2</th>
                         <th style="width:100px" align="center">Genre3</th>
                         <th style="width:100px" align="center">Gross</th>
                         <th style="width:100px" align="center">Event</th>
                         <th style="width:100px" align="center">Award</th>
                         <th style="width:100px" align="center">Category</th>
                    </tr>
                    {% for row in rows_films %}
                    <tr>
                         <td align="center">{{row["Title"]}}</td>
                         <td align="center">{{row["Year"]}}</td>
                         <td align="center">{{row["Grading"]}}</td>
                         <td align="center">{{row["Duration"]}}</td>
                         <td align="center">{{row["Score"]}}</td>
                         <td align="center">{{row["Genre1"]}}</td>
                         <td align="center">{{row["Genre2"]}}</td>
                         <td align="center">{{row["Genre3"]}}</td>
                         <td align="center">{{row["Gross"]}}</td>
                         <td align="center">{{row["eventName"]}}</td>
                         <td align="center">{{row["awardName"]}}</td>
                         <td align="center">{{row["Category"]}}</td>
                    </tr>
                    {% endfor %}
               </table>  
          </body>
          </html> -->
     
Next step, in order to let the index.html page work, I created a film_and_award.py file, and put the following code in it
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

At last, I input the following code in the terminal, and boxed my url by changing the port to the same port I used to display my data
     export FLASK_APP=film_and_award.py
     export FLASK_ENV=development
     python3 -m flask run --host=0.0.0.0 --port=5566
