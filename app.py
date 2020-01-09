import sqlite3
from flask import Flask, render_template, g, request
#conn = sqlite3.connect("D:\Chris\Downloads\\flowers2019.db")

app = Flask(__name__)

DATABASE ='D:\Chris\Downloads\\flowers2019 (1).db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = get_db().cursor()
    if request.method== 'POST':
        flowersName = request.form['search2']

    return render_template('home.html')

@app.route('/flowers', methods=['GET', 'POST'])
def flowers():
    con=sqlite3.connect(DATABASE)
    cur = con.cursor()
    if request.method== 'POST':
        flowersName = request.form['search2']
        t = (flowersName,)
        cur.execute("select sighted, location, person from sightings where name = ? order by sighted desc limit 10", t)
        return render_template('flowers.html', flowerT=cur.fetchall())
    con.commit()
    con.close()
    return render_template('flowers.html')

@app.route('/NewSighting', methods=['GET', 'POST'])
def newSighting():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if request.method == 'POST':
        name = request.form['name']
        person = request.form['person']
        location = request.form['location']
        date = request.form['date']
        t = [name, person, location, date,]
        cur.execute('insert into sightings values(?, ?, ?, ?)', t)
    con.commit()
    con.close()
    return render_template('Insert.html')

@app.route('/UpdateFlower', methods=['GET', 'POST'])
def updateFlower():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if request.method == 'POST':
        OC = request.form['OC']
        NC = request.form['NC']
        NG = request.form['NG']
        NS = request.form['NS']
        t = [NG, NS, NC, OC,]
        t2 = [NC, OC,]
        cur.execute('update flowers set genus= ?, species=?, comname=? where comname = ?', t)
        cur.execute('update sightings set name = ? where name = ?', t2)
    con.commit()
    con.close()
    return render_template('Update.html')

@app.route('/Delete', methods=['GET', 'POST'])
def Delete():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if request.method == 'POST':
        name = request.form['name']
        person = request.form['person']
        location = request.form['location']
        date = request.form['date']
        t = [name, person, location, date,]
        cur.execute('delete from sightings where name = ? and person = ? and location = ? and sighted = ?', t)
    con.commit()
    con.close()
    return render_template('delete.html')


if __name__== '__main__':
    app.run()
