from flask import Flask, jsonify, request, render_template
import os
from os import path
import csv
import psycopg2
import datetime as dt
import re

app = Flask(__name__)

conn = psycopg2.connect(
   database="tendermanagement", user='tendermanagement', password='tendermanagement123', host='3.19.40.8', port= '5435'
)
conn.autocommit = True
cursor = conn.cursor()

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

@app.route('/data/<string:mname>/<string:mphone>/<string:memail>/<string:mrevenue>/<string:name_1>/<string:position_1>/<string:email_1>/<string:phone_1>/<string:name_2>/<string:position_2>/<string:email_2>/<string:phone_2>/<string:name_3>/<string:position_3>/<string:email_3>/<string:phone_3>/<string:emp_name>/<string:maddress>')

def sqldata(mname,mphone,memail,mrevenue,name_1,position_1,email_1,phone_1,name_2,position_2,email_2,phone_2,name_3,position_3,email_3,phone_3,emp_name,maddress):
    if request.method == 'GET': 
        s1 = re.split(',', maddress)
        maddress = s1[-1].strip()
        cdate = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
        cursor.execute('INSERT INTO t2binfo(company_name, company_email, company_phone, company_revenue, te1_name, te1_position, te1_email, te1_phone, te2_name, te2_position, te2_email, te2_phone, te3_name, te3_position, te3_email, te3_phone, created_date, modified_by, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (mname, memail, mphone, mrevenue, name_1, position_1, email_1, phone_1, name_2, position_2, email_2, phone_2, name_3, position_3, email_3, phone_3, cdate, emp_name, maddress))
        conn.commit()
    return 'Data Transfered Successfully', 200
