from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import mysql.connector as mysql
import os
from datetime import datetime

now = datetime.now()
time = now.strftime("%d/%m/%Y %H:%M:%S")

app = Flask(__name__)
api = Api(app)

recieved_args = reqparse.RequestParser()
recieved_args.add_argument("svc_name", type=str , help="missing svc_name")
recieved_args.add_argument("commit_id", type=str , help="missing commit_id")
recieved_args.add_argument("developer_name", type=str , help="missing developer_name ")
recieved_args.add_argument("commit_message", type=str , help="missing commit_message")

mysql_hostname = os.environ['MYSQL_HOSTNAME']
mysql_username = os.environ['MYSQL_USERNAME']
mysql_password = os.environ['MYSQL_PASSWORD']
mysql_database = os.environ['MYSQL_DATABASE']

db = mysql.connect(
    host = mysql_hostname,
    user = mysql_username,
    passwd = mysql_password,
    database =  mysql_database

)
cursor = db.cursor()

# add table if not exist
def add_table_if_not_exist():
    create_table ='''CREATE TABLE IF NOT EXISTS services(
           svc varchar(20),
           developer varchar(20),
           commit varchar(250),
           message varchar(250),
           time varchar(500)
    )'''
    cursor.execute(create_table)

def append_to_database(svc_name, commit_id, developer_name, commit_message):
    add_table_if_not_exist()
    query = """insert into services (svc, commit, developer, message, time) values (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (svc_name, commit_id, developer_name, commit_message, time))
    db.commit()

class add(Resource):
    def post(self):
        try:
            args = recieved_args.parse_args()
            svc_name = args["svc_name"]
            commit_id = args["commit_id"]
            developer_name = args["developer_name"]
            commit_message = args["commit_message"]
            append_to_database(svc_name,commit_id,developer_name,commit_message)
            return {"message": "added"}
        except:
            return {"message": "cant add to database"}

class fetch_by_service(Resource):
    def get(self,svc_name):
        try:
            add_table_if_not_exist()
            query = """select * from services where svc = '%s'""" %(svc_name)
            cursor.execute(query)
            records = cursor.fetchall()
            listrecords = []
            columnNames = [column[0] for column in cursor.description]
            for record in records:
                listrecords.append(dict(zip(columnNames , record)))
            return listrecords
        except:
           print ("cant connect to database")

class fetch_by_developer(Resource):
    def get(self,developer_name):
        try:
            add_table_if_not_exist()
            query = """select * from services where developer = '%s'""" %(developer_name)
            cursor.execute(query)
            records = cursor.fetchall()
            listrecords = []
            columnNames = [column[0] for column in cursor.description]
            for record in records:
                listrecords.append(dict(zip(columnNames , record)))
            return listrecords
        except:
           print ("cant connect to database")

class fetch_by_both(Resource):
    def get(self, both):
        try:
            developer_name = both.split(",")[0]
            svc_name = both.split(",")[1]
            add_table_if_not_exist()
            query = """select * from services where developer = '%s' and svc = '%s' """ %(developer_name, svc_name)
            cursor.execute(query)
            records = cursor.fetchall()
            listrecords = []
            columnNames = [column[0] for column in cursor.description]
            for record in records:
                listrecords.append(dict(zip(columnNames , record)))
            return listrecords
        except:
           print ("cant connect to database")


api.add_resource(add, "/")
api.add_resource(fetch_by_service, "/svc/<string:svc_name>")
api.add_resource(fetch_by_developer, "/developer/<string:developer_name>")
api.add_resource(fetch_by_both, "/both/<string:both>")


if __name__ == "__main__":
    app.run(debug=True)