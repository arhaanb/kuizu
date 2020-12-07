from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_mysqldb import MySQL
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

        #print(query)

        cur.execute(query)
        mysql.connection.commit ()

        results = cur.fetchone()

        if results:
            resp = make_response(redirect('/dashboard'))
            resp.set_cookie('email', email)

            return resp
            # return make_response(results)
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
    # if request.method == "POST":
    # username = request.form['username']
    # email = request.form['email']

    # cur.execute(
    # "CREATE TABLE users(name varchar(255), email varchar(255), password varchar(255))")
    cur.execute("show tables")
    # cur.execute(
    # '''INSERT INTO users(name,email) VALUES(%s,%s)''', (username, email))
    mysql.connection.commit()

    # cur.execute(''' SELECT * FROM users''')
    results = cur.fetchall()

    return make_response(jsonify(results))
    # return 'query executed successfully.'
    # return render_template('login.html')
    # resp = make_response(render_template('index.html'))
    # resp.set_cookie('userID', username)

    # return resp

@app.route('/questions', methods = ['GET','POST'])
def mcq():
 import requests
 x = requests.get('https://opentdb.com/api.php?amount=5&category=18&difficulty=easy&type=multiple')
 return make_response(x.json())
 print(x)
 return 'success'


if __name__ == "__main__":
    app.run(debug=True)
