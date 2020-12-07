from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_mysqldb import MySQL
import json
import requests

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
list1= []
list2 = []
@app.route('/questions', methods=['GET', 'POST'])
def mcq():
    maindict = {"Question1" : [] , "Question2" : [], "Question3" : [], "Question4" : [], "Question5" : []}
    uri = "https://opentdb.com/api.php?amount=5&category=18&difficulty=easy&type=multiple"
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    #print(data.get('results')[0]) 
    #for items in data:
    for i in range(0,1):
        for x in (data.get('results')):
            #print(x)
            list1 = []
            a = x.get('correct_answer')
            #print(a)
            list1.append(a)
            b = (x.get('incorrect_answers'))
            for y in b:
                #print(y)
                list1.append(y)
                
            
            answerlist.append(list1)

                
        
            #for a in x.get('correct_answer'):
             #   return i
    print(answerlist[0])
    return 'success'

if __name__ == "__main__":
    app.run(debug=True)
