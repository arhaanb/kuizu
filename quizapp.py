from flask import Flask 
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'sql12379431'
app.config['MYSQL_PASSWORD'] = ' IAiRrxwFW4'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql12379431'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
 cur = mysql.connection.cursor()
 cur,execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')
 return 'Done!'