import sys
import os
import json
from src import create_html
from src import create_js

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
    # Step 4: Restful API ( 2 endpoints)
    # Step 5: Create HTML from displaying the data
        # Write the json and send to generate_html function  and file name


main()