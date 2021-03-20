def generate_api(json_data):
    function_strings = create_query_function(json_data)
    function_strings += create_get_data(json_data)
    full_api = get_full_api(json_data, function_strings)

    with open('./{}.py'.format(json_data["name"]),'w') as final_api:
        final_api.write(full_api)

def create_query_function(json_data):
    return ""

def create_get_data(json_data):
    return ""

def get_full_api(json_data, function_strings):
    return """
from flask import Flask, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/webforms/insert', methods=['GET','POST'])
def insert():
    status = insertData(request.form)
    return status

def insertData(form):
    queries = create_queries(form)
    db = mysql.connector.connect(
    host="{}",
    database="{}",
    user="{}",
    passwd="{}"
  )
    cursor = db.cursor()
    try:
        for query in queries:
            cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        return "ok",200
    except Exception as e :
        db.rollback()
        cursor.close()
        db.close()
        return "unsuccessful",400
{}
app.run()""".format(json_data['backendHost']
                    ,json_data['mysqlDB']
                    ,json_data['mysqlUserID']
                    ,json_data['mysqlPWD']
                    ,function_strings)