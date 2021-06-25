from flask import Flask, redirect, url_for, render_template, request, flash, session
import sqlite3
import requests
import pprint
import os
import time
app = Flask(__name__)

conn = sqlite3.connect('site.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
     USERNAME VARCHAR,
     PASSWORD VARCHAR
)''')

@app.route('/')
def home():
    return render_template('randomimage.html')

@app.route('/main')
def main():
    return render_template('secretmain.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/aboutsecret')
def aboutsecret():
    return render_template('aboutsecret.html')



@app.route('/random')
def random():
    resp = requests.get('https://api.imovies.cc/api/v1/movies/top?type=movie&period=month&page=2&per_page=30')
    pprint.pprint(resp.json())
    return render_template('random.html', movies=[
        {"cover": movie['cover']['large'] or movie['covers']['data']['1050'], "name": movie['secondaryName'],
         "imdb": movie['imdbUrl']} for movie
        in resp.json()['data']])

@app.route('/series')
def series():
    resp = requests.get('https://api.imovies.cc/api/v1/movies/top?type=series&period=week&page=1&per_page=30')
    pprint.pprint(resp.json())
    return render_template('series.html', movies=[
        {"cover": movie['cover']['large'] or movie['covers']['data']['1050'], "name": movie['secondaryName'],
         "imdb": movie['imdbUrl']} for movie
        in resp.json()['data']])
@app.route('/seriessecret')
def seriessecret():
    resp = requests.get('https://api.imovies.cc/api/v1/movies/top?type=series&period=week&page=1&per_page=30')
    pprint.pprint(resp.json())
    return render_template('seriessecret.html', movies=[
        {"cover": movie['cover']['large'] or movie['covers']['data']['1050'], "name": movie['secondaryName'],
         "imdb": movie['imdbUrl']} for movie
        in resp.json()['data']])

@app.route('/randomsecret')
def randomsecret():
    resp = requests.get('https://api.imovies.cc/api/v1/movies/top?type=movie&period=month&page=2&per_page=30')
    pprint.pprint(resp.json())
    return render_template('randomsecret.html', movies=[
        {"cover": movie['cover']['large'] or movie['covers']['data']['1050'], "name": movie['secondaryName'],
         "imdb": movie['imdbUrl']} for movie
        in resp.json()['data']])

@app.route('/login', methods=["GET","POST"] )
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        conn = sqlite3.connect('site.sqlite')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
             USERNAME VARCHAR NOT NULL ,
             PASSWORD VARCHAR NOT NULL 
        )''')
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        cursor.execute('''SELECT * FROM users WHERE PASSWORD == ? and USERNAME == ?''',(password, name,))
        a = cursor.fetchone()


        if a is None:
            flash('ასეთი აქაუნთი არ არსებობს. ')
            return redirect('/register')
        else:
            return redirect('/main')

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        conn = sqlite3.connect('site.sqlite')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
             USERNAME VARCHAR NOT NULL ,
             PASSWORD VARCHAR NOT NULL 
        )''')
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        if len(name) == 0 or len(password) == 0:
            a = 'არასწორი მონაცემი'
            flash(a)
            return redirect('/register')
        else:
            cursor.execute('''SELECT * FROM users WHERE USERNAME == ?''', (name,))
            a = cursor.fetchone()
            if a is None:
                cursor.execute("INSERT INTO users (USERNAME, PASSWORD) VALUES (?,?)",(name,password))
                conn.commit()
            else:
                flash('ასეთი იუზერი უკვე არსებობს')
                return redirect('/register')

        return redirect('/main')
if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
