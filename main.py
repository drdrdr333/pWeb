## IMPORTS
from __init__ import db
from flask import Flask, render_template, request, jsonify
from string import Template
from flask.json import JSONEncoder
import psycopg2
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_migrate import Migrate, migrate
import json, operator
import pandas as pd
from pandas.io.json import json_normalize
from apiclient.discovery import build
from sqlalchemy.orm import sessionmaker
import os




## INITIALIZE APP
DEBUG = True
app = Flask(__name__)

db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')
db_sock = os.environ.get('DB_SOCKET_DIR')
cloud_sql_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class BaseBall(db.Model):
    __tablename__ = 'baseballpitchers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    era = db.Column(db.Float())
    ip = db.Column(db.Float())
    sop9 = db.Column(db.Float())
    bbp9 = db.Column(db.Float())
    whip = db.Column(db.Float())

    def __init__(self, name, era, ip, sop9, bbp9, whip):
        self.name = name
        self.era = era
        self.ip = ip
        self.sop9 = sop9
        self.bbp9 = bbp9
        self.whip = whip

    def asdict(self):
        return {'name': self.name, 'era': self.era, 'ip': self.ip, 'sop9': self.sop9, 'bbp9': self.bbp9, 'whip': self.whip}
           

@app.route('/')
def home():
    return render_template('pubtemp/parent.html')  


@app.route('/Player_Selection', methods=["POST", "GET"])
def data():
    if request.method == 'GET':
        
        fname = ''
        fera = request.args.get("ERA")
        fip = request.args.get("IP")
        fsop9 = request.args.get("SOp9")
        fbbp9 = request.args.get("BBp9")
        fwhip = request.args.get("WHIP")

        sname = BaseBall.name != fname
        sera = BaseBall.era < fera
        sip = BaseBall.ip > fip
        ssop9 = BaseBall.sop9 > fsop9
        sbbp9 = BaseBall.bbp9 < fbbp9
        swhip = BaseBall.whip < fwhip
        
  
        var = BaseBall.query.filter(sname, sera, sip, ssop9, sbbp9, swhip).all()
        final = [p.asdict() for p in var]
        p1 = sorted(final, key=lambda i: i['name'])
        
    return jsonify(p1)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
