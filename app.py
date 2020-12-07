from flask import Flask 
from flask_mysqldb import MySQL

app = Flask(__name__)
if __name__ == "__main__":
 app.run(debug=True)

app.config['MYSQL_USER'] = 'sql12379431'
app.config['MYSQL_PASSWORD'] = 'IAiRrxwFW4'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql12379431'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
username = input("Enter Name")
number = int(input("Enter ID"))
@app.route('/')
def index():
 cur = mysql.connection.cursor()
 #cur.execute('''CREATE TABLE example(id INTEGER, name VARCHAR(20))''')
 cur.execute("INSERT INTO example VALUES(%s,%s)",(number,username))
 mysql.connection.commit()
 
 cur.execute('''SELECT * FROM example''')
 results = cur.fetchall()
 print(results)


 return 'POGGGG!'

