from src import create_sql

def generate_api(json_data):
    function_strings = create_query_function(json_data)
    function_strings += create_get_data(json_data)
    full_api = get_full_api(json_data, function_strings)

    with open('./{}.py'.format(json_data["name"]),'w') as final_api:
        final_api.write(full_api)

def create_query_function(json_data):
    enames = []
    for element in json_data["elements"]:
        if element["etype"] in ['textbox','selectlist','radiobutton']:
            enames.append(element["ename"])
    
    main_placeholders = ["'{}'"]*len(enames)
    main_placeholders = ','.join(main_placeholders)
    
    main_values = []
    for name in enames:
        main_values.append("form['{}']".format(name))
    main_values = ','.join(main_values)

    main_query = """
    \"""insert into {}
    values({})\""".format({})
    """.format(json_data["name"], main_placeholders, main_values)

    other_queries = ""
    primary_key = create_sql.get_primarykey(json_data)
    for element in json_data["elements"]:
        if element["etype"] in ['checkbox','multiselectlist']:
            placeholders = ["'{}'"]*(len(primary_key)+1)
            placeholders = ",".join(placeholders)
            values_list = []
            for i in primary_key:
                values_list.append("form['{}']".format(i["ename"]))
            values_list = ",".join(values_list)
            other_queries += """
    row_list = []
    for i in form.getlist("{}"):
        row_list.append(\"""({})\""".format({},i))
    query_list.append(\"""
                    insert into {}_{}
                    values
                            {{}}\""".format(",".join(row_list)))
            """.format(element["ename"],placeholders,values_list,element["ename"],json_data["name"])

    main_function = """
def create_queries(form):
    query_list = []
    query_list.append({})
    {}
    return query_list
""".format(main_query, other_queries)

    return main_function

def create_get_data(json_data):
    tables_dict = dict()
    
    # table col names
    primary_key_cols = []
    primary_key = create_sql.get_primarykey(json_data)
    for keyElement in primary_key:
        primary_key_cols.append(keyElement["ename"])

    main_cols = []
    for element in json_data["elements"]:
        if element["etype"] in ['textbox','selectlist','radiobutton']:
            main_cols.append(element["ename"])
        if element["etype"] in ['checkbox','multiselectlist']:
            tables_dict['{}_{}'.format(element["ename"], json_data['name'])] = primary_key_cols + [element["ename"]]
    tables_dict[json_data["name"]] = main_cols

    table_list = list(tables_dict.keys())
    tables = ",".join([ "'{}'".format(table) for table in table_list])
    get_api_string = """
@app.route('/webforms/display', methods=['GET'])
def display():
    db = mysql.connector.connect(
        host="{}",
        database="{}",
        user="{}",
        passwd="{}
    )
    print(request)
    cursor = db.cursor()
    data = dict()
    tables_list = [{}]
    for table in tables_list:
        cursor.execute("select * from {{}}".format(table))
        records = cursor.fetchall()
        rows = []
        for record in records:
            rows.append(prepare_dict(table, record))
        data[table]=rows
    cursor.close()
    db.close()
    return jsonify(data)

def prepare_dict(table_name, record):
""".format(json_data['backendHost']
    ,json_data["mysqlDB"]
    ,json_data["mysqlUserID"]
    ,json_data["mysqlPWD"]
    ,tables)

    for table in table_list:
        get_api_string += prepare_get_data(table, tables_dict[table])

    return get_api_string

def prepare_get_data(tablename, col_names):
    formated_col_names = []
    for col_index in range(len(col_names)):
        formated_col_names.append("""'{}': record[{}]""".format(col_names[col_index], col_index))
    
    formated_col_names = ','.join(formated_col_names)
    final_string = """
    if table_name == '{}':
        return {{{}}}    
""".format(tablename, formated_col_names)
    return final_string

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