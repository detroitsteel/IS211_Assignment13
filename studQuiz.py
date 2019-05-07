#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Controller for Website Todo List with Form"""

import re
import logging
from logging import FileHandler
import traceback
import sqlite3 as lite
from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)
file_handler = FileHandler("./logfile.log")
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
con = None
stulist = {}
qzlist = {}
qzscrlist = {}
uname = ''
pp = ''
loggy = False
loginerror = 'Username and Password Incorrect, Please try again'

def credvalid(uname, pp):
    loggy = False
    if uname == 'admin' and pp == 'password':
        global loggy
        loggy = True
        return loggy
    else:
        global loggy
        loggy = False
        return loggy
    
def stuload():
    with lite.connect('hw13.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                stulist[row[0]] = [row[1], row[2]]
    return

def qzload():
    with lite.connect('hw13.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM quiz")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                qzlist[row[0]] = [row[1], row[2], row[3]]

    return

def qzscrload(stuid):
    print type(stuid)
    qzscrlist.clear()
    rwct = 0
    with lite.connect('hw13.db') as con:
        cur = con.cursor()
        cur.execute("SELECT s.id, s.first_name, s.last_name, q.subject, "
                     "q.q_date, qs.score FROM students s left join "
                     "quizScore qs on qs.stu_id = s.id left join quiz q "
                     "on q.id = qs.q_id where s.id = ?", (stuid))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                qzscrlist[rwct] = [row[0], row[1], row[2], row[3],
                row[4], row[5]]
                rwct += 1
    return 

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def logincheck():
    global uname
    uname = request.form['Username']
    global pp
    pp = request.form['Password']
    credvalid(uname, pp)
    if loggy:
        return render_template('dashboard.html', stulist = stulist, qzlist = qzlist)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)
    
@app.route('/addstu')
def stuurlink():
    if loggy:
        return render_template('./student/add.html', stulist = stulist)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/addstu', methods = ['POST'])
def addstu():
    if loggy:    
        fname = request.form['FirstName']
        lname = request.form['LastName']
        try:
            if fname == '' or lname == '':
                InErr = 'Incorrect Value Enterd, Try Again'
                app.logger.error(InErr)
                raise Exception(InErr)
            else:
                with lite.connect('hw13.db') as con1:
                    cur1 = con1.cursor()
                    cur1.execute("INSERT INTO students(first_name, last_name) VALUES(?, ?);"
                                 , (fname, lname))
                stuload()
                return render_template('./student/add.html', stulist = stulist)
        except(Exception) as e:
            stuload()
            error = 'SQL Insert Error, Please Try Again.'
            return render_template('./student/add.html', stulist = stulist, error = e)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/addqz')
def qzurlink():
    if loggy:
        return render_template('./quiz/addqz.html', qzlist = qzlist)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/addqz', methods = ['POST'])
def addqz():
    if loggy:
        try:
            QzSub = request.form['QzSubj']
            QCnt = int(request.form['QCnt'])
            QzDte = request.form['QzDte']
            with lite.connect('hw13.db') as con1:
                cur1 = con1.cursor()
                cur1.execute("INSERT INTO quiz(subject, q_cnt, q_date) VALUES(?, ?, ?);"
                             , (QzSub, QCnt, QzDte))
            qzload()
            return render_template('./quiz/addqz.html', qzlist = qzlist)
        except Exception as e:
            qzload()
            app.logger.error(traceback.format_exc())
            err = 'Invalid Entry, Please Try Again'
            return render_template('./quiz/addqz.html', qzlist = qzlist,
                                   error = err)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)
    
@app.route('/viewstu', methods = ['GET'])
def stuqzurlink():
    if loggy:
        stuid = request.args.get('stuid')
        qzscrload(stuid)
        return render_template('./student/viewstu.html', stuvwlist = qzscrlist)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/addstuqz')
def stuqzuraddlink():
    if loggy:
        stuidlist = stulist.keys()
        qzidlist = qzlist.keys()
        return render_template('./results/addstuqz.html', stulist = stulist
                               , qzlist = qzidlist)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/addstuqz', methods = ['Post'])
def SaveStuQz():
    if loggy:
        try:
            stuid = request.form['StuID']
            qzuid = request.form['QzID']
            qzscr = request.form['QzScr']
            with lite.connect('hw13.db') as con1:
                cur1 = con1.cursor()
                cur1.execute("INSERT INTO quizScore (stu_id, q_id, score) "
                             "VALUES(?, ?, ?);", (stuid, qzuid, qzscr))
            return render_template('./results/addstuqz.html',stulist = stulist
                                   ,qzlist = qzlist)#redirect('/login')
        except Exception as e:
            app.logger.error(traceback.format_exc())
            err = 'Invalid Entry, Please Try Again'
            return render_template('./results/addstuqz.html',stulist = stulist
                                   ,qzlist = qzlist, error = err)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

if __name__ == '__main__':
    stuload()
    qzload()
    app.run()
