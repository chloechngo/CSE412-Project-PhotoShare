from flask import Flask, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'chloengo'
app.config['MYSQL_DATABASE_DB'] = 'CSE412Schema'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

@app.route('/test_db_connection')
def test_db_connection():
    cur = mysql.connection.cursor()
    cur.execute('SELECT 1')
    result = cur.fetchone()
    cur.close()
    return jsonify({'result': result[0]})


if __name__ == '__main__':
    app.run(port=5500)
