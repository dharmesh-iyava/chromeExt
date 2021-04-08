# app.py
from flask import Flask, jsonify, request, render_template
import os
from os import path
import csv

app = Flask(__name__)

def createFolder(sourceFolder, folderName):
    try:
        folderName = folderName.replace(":", "-").replace("\\", "-").replace("/", "-")
        print(sourceFolder + "/" + folderName)
        os.makedirs(sourceFolder + "/" + folderName, mode=0o777, exist_ok=False)
    except OSError as error:
        print(error)
        print("Error creating folder " + folderName)

@app.route('/')
def home():
    return '<h1 style="color:#007780;display: flex;justify-content: center;margin-top:250px;font-size:4rem;text-decoration:underline;">Welcome to Tenders2bidInfo</h1>'

@app.route('/data/<string:mname>/<string:mphone>/<string:memail>/<string:mrevenue>/<string:name_1>/<string:position_1>/<string:email_1>/<string:phone_1>/<string:name_2>/<string:position_2>/<string:email_2>/<string:phone_2>/<string:name_3>/<string:position_3>/<string:email_3>/<string:phone_3>')
def info(mname,mphone,memail,mrevenue,name_1,position_1,email_1,phone_1,name_2,position_2,email_2,phone_2,name_3,position_3,email_3,phone_3):

    if mname != "":

        currTime = "T2B Info"

        mainPath = "D:/"

        # everyday create a new path with latest date
        createFolder(mainPath, currTime)
        mainPath = mainPath + "/" + currTime

        if not path.exists(mainPath + "/T2binfo.csv"):
            with open(mainPath + "/T2binfo.csv", 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['c_name','c_email','c_phone','c_revenue','top_executive_name_1','top_executive_position_1','top_executive_email_1','top_executive_phone_1','top_executive_name_2','top_executive_position_2','top_executive_email_2','top_executive_phone_2','top_executive_name_3','top_executive_position_3','top_executive_email_3','top_executive_phone_3']

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writerow({'c_name':'c_name','c_email':'c_email','c_phone':'c_phone','c_revenue':'c_revenue',
                                'top_executive_name_1':'top_executive_name_1','top_executive_position_1':'top_executive_position_1','top_executive_email_1':'top_executive_email_1','top_executive_phone_1':'top_executive_phone_1',
                                'top_executive_name_2':'top_executive_name_2','top_executive_position_2':'top_executive_position_2','top_executive_email_2':'top_executive_email_2','top_executive_phone_2':'top_executive_phone_2',
                                'top_executive_name_3':'top_executive_name_3','top_executive_position_3':'top_executive_position_3','top_executive_email_3':'top_executive_email_3','top_executive_phone_3':'top_executive_phone_3'})

        # write csv
        with open(mainPath + "/T2binfo.csv", 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['c_name','c_email','c_phone','c_revenue','top_executive_name_1','top_executive_position_1','top_executive_email_1','top_executive_phone_1','top_executive_name_2','top_executive_position_2','top_executive_email_2','top_executive_phone_2','top_executive_name_3','top_executive_position_3','top_executive_email_3','top_executive_phone_3']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow({'c_name': mname ,'c_email': memail ,'c_phone': mphone ,'c_revenue': mrevenue,
                            'top_executive_name_1': name_1 ,'top_executive_position_1': position_1 ,'top_executive_email_1': email_1 ,'top_executive_phone_1': phone_1,
                            'top_executive_name_2': name_2 ,'top_executive_position_2': position_2 ,'top_executive_email_2': email_2 ,'top_executive_phone_2': phone_2,
                            'top_executive_name_3': name_3 ,'top_executive_position_3': position_3 ,'top_executive_email_3': email_3 ,'top_executive_phone_3': phone_3})

        return 'Data Transfered Successfully', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
    
if __name__ == "__main__":
        app.run(debug=True)
