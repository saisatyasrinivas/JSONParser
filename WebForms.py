import sys
import os
import json
from src import create_html

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
    create_html.generate_html(json_data, "interests.html")
    # Step 2: Javascript 2 validations and 2 functions (submitdata,Displaydata)
    # Step 3: MYSQL Script (creating the table)
    # Step 4: Restful API ( 2 endpoints)


main()