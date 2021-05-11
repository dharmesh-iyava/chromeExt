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
        maddress = s1[-1]
        #print(mname, memail, mphone, mrevenue, name_1, position_1, email_1, phone_1, name_2, position_2, email_2, phone_2, name_3, position_3, email_3, phone_3)
        femail, fphone, ffname, flname , fposition = '', '', '', '', ''
        try:
            if email_1 == ' ' or email_2 == ' ' or email_3 == ' ' or email_1 == 'NA' or email_2 == 'NA' or email_3 == 'NA':
                email_1 = email_1.replace(' ', '')
                email_2 = email_2.replace(' ', '')
                email_3 = email_3.replace(' ', '')
                email_1 = email_1.replace('NA', '')
                email_2 = email_2.replace('NA', '')
                email_3 = email_3.replace('NA', '')
            if email_1 == '' and email_2 == '':
                femail = email_3
                fposition = position_3
                s1 = re.split(' ', name_3)
                ffname = s1[0]
                flname = s1[1]
            elif email_3 == '' and email_2 == '':
                femail = email_1
                fposition = position_1
                s1 = re.split(' ', name_1)
                ffname = s1[0]
                flname = s1[1]
            elif email_1 == '' and email_3 == '':
                femail = email_2
                fposition = position_2
                s1 = re.split(' ', name_2)
                ffname = s1[0]
                flname = s1[1]
            elif email_1 == '' and email_2 == '' and email_3 == '':
                return 'You have not clicked any top executive'
        except:
            pass

        try:
            if phone_1 == 'B' or phone_2 == 'B' or phone_3 == 'B':
                phone_1 = phone_1.replace('B', '')
                phone_2 = phone_2.replace('B', '')
                phone_3 = phone_3.replace('B', '')
                phone_1 = phone_1.replace('NA', '')
                phone_2 = phone_2.replace('NA', '')
                phone_3 = phone_3.replace('NA', '')
            if phone_1 == '' and phone_2 == '':
                fphone = phone_3
            elif phone_3 == '' and phone_2 == '':
                fphone = phone_1
            elif phone_1 == '' and phone_3 == '':
                fphone = phone_2
        except:
            pass
        #print(ffname, flname, fposition, femail, fphone)

        femail = femail.replace('(Business)', '').replace('(Supplemental)', '').replace('(HQ)', '').replace('(Mobile)', '').replace('(Direct)', '')
        fphone = fphone.replace('(Business)', '').replace('(Supplemental)', '').replace('(HQ)', '').replace('(Mobile)', '').replace('(Direct)', '')
        if '(' in femail:
            fphone = femail
            femail = 'NA'
        cdate = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
        if femail == '' or femail == ' ':
            return '<h2 style="font-weight:bold;background-color:red;color:white;text-align:center;padding:10px;">You Have not Clicked Any Top Executive</h2>'
        else:
            cursor.execute('INSERT INTO t2bzoominfo(company_name, company_email, company_phone, company_revenue, te_fname, te_lname, te_position, te_email, te_phone, created_date, modified_by, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (mname, memail, mphone, mrevenue, ffname, flname, fposition, femail, fphone, cdate, emp_name, maddress))
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
                        <td>{fposition}</td>
                        <td>{femail}</td>
                        <td>{fphone}</td>
                        <td>{maddress}</td>
                    </tr>
                    </table>

                    </body>
                    </html>

                    """
