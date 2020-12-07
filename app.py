from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_mysqldb import MySQL
import json
import requests
import random

app = Flask(__name__)


app.config['MYSQL_HOST'] = "sql12.freemysqlhosting.net"
app.config['MYSQL_USER'] = "sql12379431"
app.config['MYSQL_PASSWORD'] = "IAiRrxwFW4"
app.config['MYSQL_DB'] = 'sql12379431'
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

        cur.execute(
            'INSERT INTO users(name, email, password) VALUES(%s, %s, %s)', (name, str(email), password))
        mysql.connection.commit()
        return redirect('/login')

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

        query = str('''select * from users where email = "''' +
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
        return render_template('dashboard.html')
    else:
        return redirect('/')


@app.route('/users', methods=['GET', 'POST'])
def getUsers():
    cur = mysql.connection.cursor()

    cur.execute("select * from users")
    mysql.connection.commit()

    results = cur.fetchall()

    return make_response(jsonify(results))


@app.route('/execute2307', methods=['GET', 'POST'])
def execute():
    # if you see this DO NOT VISIT THIS ROUTE
    cur = mysql.connection.cursor()
    cur.execute("show tables")
    mysql.connection.commit()

    results = cur.fetchall()

    return make_response(jsonify(results))


maindict = {}
answerlist = []
list1 = []
list2 = []


@app.route('/questions', methods=['GET', 'POST'])
def mcq():
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
    return maindict


if __name__ == "__main__":
    app.run(debug=True)
