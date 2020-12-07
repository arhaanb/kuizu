from flask import Flask, render_template,request,jsonify, make_response
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = "sql12.freemysqlhosting.net"
app.config['MYSQL_USER'] = "sql12379431"
app.config['MYSQL_PASSWORD'] = "IAiRrxwFW4"
app.config['MYSQL_DB'] = 'sql12379431'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/setcookie', methods=['GET', 'POST'])
def index():
 if request.method == "POST":
  username = request.form['username']
  email = request.form['email']

  cur = mysql.connection.cursor()
  #cur.execute("CREATE TABLE users(name char(20), email char(20))")
  cur.execute('''INSERT INTO users(name,email) VALUES(%s,%s)''', (username,email))
  mysql.connection.commit()
  cur.execute(''' SELECT * FROM users''')
  results = cur.fetchall()
   
 # return jsonify(results)
  #return 'success'
 #return render_template('index.html')
 resp = make_response(render_template('index.html'))
 resp.set_cookie('userID', username)
   
 return resp
 


if __name__ == "__main__": 
 app.run(debug=True)

 


