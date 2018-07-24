import os
import cx_Oracle
from flask import Flask

db_user = "k"
db_password = "Pr0_K_MIS"
db_connect = "192.168.2.5:1521/KRDPDUAT"
service_port = port=os.environ.get('PORT', '8080')

app = Flask(__name__)

@app.route('/')
def index():
    connection = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = connection.cursor()
    cur.execute("select * from sttm_customer")
    col = cur.fetchone()[0]
    data = cur.fetchone()
    cur.close()
    connection.close()
    return data

if __name__ == '__main__':
      app.run(host='0.0.0.0', port= int(service_port) )