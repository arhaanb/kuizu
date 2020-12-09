from flask import Flask, render_template, request, jsonify, make_response, redirect, session
from flask_mysqldb import MySQL
import json
import requests
import random
import os

app = Flask(__name__)
app.secret_key = 'lolsecretkey'

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    email = request.cookies.get('email')
    if email:
        return redirect('/dashboard')
    cur = mysql.connection.cursor()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            cur.execute('INSERT INTO new_users(name, email, password) VALUES(%s, %s, %s)',
                        (name, str(email), password))
            mysql.connection.commit()
            return redirect('/login')
        except:
            message = 'Email is already in use.'
            return render_template('register.html', msg=message)

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = mysql.connection.cursor()
    email = request.cookies.get('email')
    if email:
        return redirect('/dashboard')

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        query = str('''select * from new_users where email = "''' +
                    email + '" and password = "' + password + '"')

        cur.execute(query)
        mysql.connection.commit()

        results = cur.fetchone()

        if results:
            resp = make_response(redirect('/dashboard'))
            resp.set_cookie('email', email)

            return resp
        else:
            msg = "wrong email or password"
            return render_template('login.html', value=msg)

    return render_template('login.html')


@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('email')

    return resp


@app.route('/dashboard')
def dashboard():
    email = request.cookies.get('email')
    if email:
        cur = mysql.connection.cursor()
        # cur.execute('''CREATE TABLE new_users(name varchar(255),
        #   email varchar(255) PRIMARY KEY, password varchar(255)) ''')
        query = str("select * from new_users where email =" +
                    '"' + email + '"')
        cur.execute(query)
        mysql.connection.commit()
        results = cur.fetchone()

        return render_template('dashboard.html', data=results)
    else:
        return redirect('/')


@app.route('/users', methods=['GET', 'POST'])
def getUsers():
    cur = mysql.connection.cursor()

    cur.execute("select * from new_users")
    mysql.connection.commit()

    results = cur.fetchall()

    return make_response(jsonify(results))


@app.route('/execute2307', methods=['GET', 'POST'])
def execute():
    # if you see this DO NOT VISIT THIS ROUTE
    cur = mysql.connection.cursor()
    # cur.execute('''
    #  CREATE TABLE new_users(
    #   name varchar(255),
    #  email varchar(255),
    # password varchar(255)
    # )
    # ''')
    cur.execute('select * from new_users')

    mysql.connection.commit()

    results = cur.fetchall()

    return make_response(jsonify(results))


maindict = {}
answerlist = []
list1 = []
list2 = []


@app.route('/questions', methods=['GET', 'POST'])
def mcq():
    email = request.cookies.get('email')
    if email:
        maindict = {}
        finalq = []
        uri = "https://opentdb.com/api.php?amount=5&category=18&difficulty=easy&type=multiple"
        try:
            uResponse = requests.get(uri)
        except requests.ConnectionError:
            return "Connection Error"
        Jresponse = uResponse.text
        data = json.loads(Jresponse)
        questions = data.get('results')

        for ques in questions:
            qdict = {}
            anslist = []
            anslist.append(ques['correct_answer'])
            for ans in ques['incorrect_answers']:
                anslist.append(ans)
            random.shuffle(anslist)
            correctIndex = anslist.index(ques['correct_answer'])
            qdict["question"] = ques['question']
            qdict["answers"] = anslist
            qdict["correctIndex"] = correctIndex
            finalq.append(qdict)
        maindict["questions"] = finalq

        session['quiz'] = maindict

        return render_template('quiz.html', questions=maindict)
    else:
        return redirect('/')


@app.route('/check', methods=['POST'])
def check():
    if request.method == "POST":
        data = request.form.to_dict()
        quizdict = session['quiz']
        quizqs = quizdict.get('questions')
        attempts = []
        for key, value in data.items():
            attempts.append(value)
        score = 0
        for q in quizqs:
            anslist = q.get('answers')
            ind = quizqs.index(q)
            userans = anslist.index(attempts[ind])
            q["userans"] = userans
            if userans == q.get('correctIndex'):
                score = score+1
        quizdict["score"] = score

        return render_template('results.html', response=quizdict)


@app.route('/test', methods=['GET', 'POST'])
def test():

    username = {"haaaa": "nooooo", "poop": 'peeep'}
    # username = session['username']
    session['username'] = username

    # return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    return "hi"


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(405)
def error1(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def error2(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
