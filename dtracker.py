from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import mysql.connector as mysql
import os

app = Flask(__name__)
api = Api(app)

recieved_args = reqparse.RequestParser()
recieved_args.add_argument("svc_name", type=str , help="missing svc_name")
recieved_args.add_argument("commit_id", type=int , help="missing commit_id")
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

def append_to_database(svc_name, commit_id, developer_name, commit_message):
    query = """insert into services (svc, commit, developer) values (%s, %s, %s)"""
    cursor.execute(query, (svc_name, commit_id, developer_name))
    db.commit()

class add(Resource):
    def post(self):
        args = recieved_args.parse_args()
        svc_name = args["svc_name"]
        commit_id = args["commit_id"]
        developer_name = args["developer_name"]
        append_to_database(svc_name,commit_id,developer_name,commit_message)
        return {"message": "added"}

class fetch(Resource):
    def get(self,svc_name):
        query = """select * from services where svc = '%s'""" %(svc_name)
        cursor.execute(query)
        records - cursor.fetchall()
        return records        

api.add_resource(add, "/")
api.add_resource(fetch, "/<string:svc_name>")

if __name__ == "__main__":
    app.run(debug=True)