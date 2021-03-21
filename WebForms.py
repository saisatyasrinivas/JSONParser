import sys
import os
import json
from src import create_html
from src import create_js
from src import create_sql
from src import create_API

def main():
    if len(sys.argv) != 2:
        print("Please enter the filename")
        print("Usage: python WebForms.py [filename]")
        os._exit(-1)
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print("exit the project")
        exit()
    
    with open(filename,'r') as f:
        json_data = json.load(f)
    
    # Step 1: Create the HTML
    create_html.generate_html(json_data)
    # Step 2: Javascript 2 validations and 2 functions (submitdata,Displaydata)
    create_js.generate_jscript(json_data)
    # Step 3: MYSQL Script (creating the table)
    create_sql.generate_sql(json_data)
    # Step 4: Restful API ( 2 endpoints)
    create_API.generate_api(json_data)
    # Step 5: Create HTML from displaying the data
    json_data_display = {
        'name': json_data["name"],
        'backendURL' : json_data['backendURL'],
        'caption': '{} form data'.format(json_data["name"]),
        'elements':[
            {
            "etype": "submit",
            "ename": "submit",
            "caption": "Get data from database"
            }
        ]
    }
    create_html.generate_html(json_data_display, True)
    create_js.generate_additional_js(json_data_display)
        # Write the json and send to generate_html function  and file name


main()