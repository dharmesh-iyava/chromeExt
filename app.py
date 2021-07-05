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

@app.route('/data/<string:mname>/<string:mphone>/<string:memail>/<string:mrevenue>/<string:name_1>/<string:position_1>/<string:email_1>/<string:phone_1>/<string:emp_name>/<string:maddress>')

def sqldata(mname,mphone,memail,mrevenue,name_1,position_1,email_1,phone_1,emp_name,maddress):
    if request.method == 'GET': 
        s1 = re.split(',', maddress)
        maddress = s1[-1]
        #print(phone_1)
        s2 = re.split(' ', name_1)
        ffname = s2[0].strip()
        flname = s2[1].strip()
        #email_1 = email_1.replace('(Business)', '').replace('(Supplemental)', '').replace('(HQ)', '').replace('(Mobile)', '').replace('(Direct)', '')
        #phone_1 = phone_1.replace('(Business)', '').replace('(Supplemental)', '').replace('(HQ)', '').replace('(Mobile)', '').replace('(Direct)', '')
        email_1 = email_1.replace('__', ',')
        if ',' in email_1:
            s1 = re.split(',', email_1)
            email_1 = email_1.replace(s1[0]+',', '')
        phone_1 = phone_1.replace('__', ',').replace(', ,', ',')
        cdate = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
        if email_1 == '' or phone_1 == ' ':
            return '<h2 style="font-weight:bold;background-color:red;color:white;text-align:center;padding:10px;">You Have not Clicked Any Top Executive</h2>'
        else:
            cursor.execute('INSERT INTO t2bzoominfo(company_name, company_email, company_phone, company_revenue, te_fname, te_lname, te_position, te_email, te_phone, created_date, modified_by, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (mname, memail, mphone, mrevenue, ffname, flname, position_1, email_1, phone_1, cdate, emp_name, maddress))
            conn.commit()
        # return '<h2 style="font-weight:bold;background-color:green;color:white;text-align:center;padding:10px;">Data Transfered Successfully</h2>', 200
        return r"""
                <html>
                    <head>
                    <style>
                        *{
                            margin-top:20px;
                        }
                        table {
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                        }

                        td, th {
                        border: 1px solid #007780;
                        text-align: left;
                        padding: 8px;
                        }
                        h2
                        {
                            font-weight:bold;
                            background-color:#007780;
                            color:white;
                            text-align:center;
                            padding:10px;
                        }
                        th, td{
                            text-align:center;
                        }
                    </style>
                    </head>
                    <body>
                    <h2>Data Transfered Successfully</h2>

                    <table>
                    <tr>
                        <th>Company Name</th>
                        <th>Company Email</th>
                        <th>Company Phone</th>
                        <th>Company Revenue</th>
                        <th>Top Executive First Name</th>
                        <th>Top Executive Last Name</th>
                        <th>Top Executive Position</th>
                        <th>Top Executive Email</th>
                        <th>Top Executive Phone</th>
                        <th>Country</th>
                    </tr>
                    <tr>"""f"""
                        <td>{mname}</td>
                        <td>{memail}</td>
                        <td>{mphone}</td>
                        <td>{mrevenue}</td>
                        <td>{ffname}</td>
                        <td>{flname}</td>
                        <td>{position_1}</td>
                        <td>{email_1}</td>
                        <td>{phone_1}</td>
                        <td>{maddress}</td>
                    </tr>
                    </table>

                    </body>
                    </html>

                    """
