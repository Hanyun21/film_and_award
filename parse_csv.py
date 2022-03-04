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
