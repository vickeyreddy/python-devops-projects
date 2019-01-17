import urllib, sys, os, re, urllib2
from flask import Flask, redirect, render_template, request, session, url_for, flash,json
from urllib2 import urlopen, HTTPError, URLError
from geidm import GEIDM
from connect_db import ConnectDB

app = Flask(__name__)

##### Login View #####
@app.route("/", methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'DevOps@2016':
            error = "Error: Invalid Credentials.Please try again !!!"
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

##### Home Page View #####
@app.route("/home", methods = ['GET','POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        res = None;b=None
        if request.method == 'POST':
            sid = request.form['subnet'].strip()
            print sid
            a = GEIDM(sid)
            b = a.search_groupid()
        return render_template('index.html',res=b)


##### Manage GroupID View #####
@app.route("/groups", methods = ['GET','POST'])
def manage_groups():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        result_create = None;result_delete = None
        if request.method=='POST':
            if 'Create' in request.form:
                sid = request.form['subnet'].strip()
                buid = request.form['bid'].strip()
                idm = GEIDM(sid)
                result_create = idm.create_groupid(buid)
                return render_template('groups.html',result_create=result_create)
            elif 'Delete' in request.form:
                gid = request.form['gid'].strip()
                subnet = request.form['subnet2'].strip()
                idm = GEIDM(subnet)
                result_delete = idm.delete_groupid(gid)
                return render_template('groups.html',result_delete=result_delete)
        return render_template('groups.html')

##### Manage Subnet View #####
@app.route("/subnets", methods = ['GET','POST'])
def manage_subnets():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        result_create = None;result_delete = None
        if request.method=='POST':
            if 'buid' in request.form:
                buid = request.form['buid'].strip()  #default business unitID = 1750623
            if 'Create' in request.form:
                sid = request.form['subnet'].strip()
                if not re.match("^(\d{3})\.(\d{3})\.(\d{3})\.(\d{3})\_(\d{2})$", sid):
                    result_create = "Error.Invalid Subnet Address!!!"
                    return render_template('subnets.html',result_create=result_create)
                idm = GEIDM(sid)
                gid = idm.search_groupid()
                if len(gid) > 1:
                    gid = idm.search_groupid()['groupid']
                else:
                    create_gid = idm.create_groupid('1750623')
                    gid = idm.search_groupid()['groupid']
                d = ConnectDB('p339-0-1-scan.corporate.ge.com', 1621, 'ATPRXADM01', 'ATPRXADM01', 'cig1')
                result_create = d.save_subnet(gid, sid)
                return render_template('subnets.html',result_create=result_create)

            elif 'Delete' in request.form:
                sid = request.form['subnet2'].strip()
                if not re.match("^(\d{3})\.(\d{3})\.(\d{3})\.(\d{3})\_(\d{2})$", sid):
                    result_delete = "Error.Invalid Subnet Address!!!"
                    return render_template('subnets.html',result_delete=result_delete)
                idm = GEIDM(sid)
                gid = idm.search_groupid()
                if 'groupid' in gid:
                     idm.delete_groupid(gid['groupid'])
                d = ConnectDB('p339-0-1-scan.corporate.ge.com', 1621, 'ATPRXADM01', 'ATPRXADM01', 'cig1')
                result_delete = d.delete_subnet(sid)
                return render_template('subnets.html',result_delete=result_delete)

        return render_template('subnets.html')

##### Logout View #####
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

##### Main Program #####
if __name__ == "__main__":
    app.secret_key = 'DevOps@2016'
    #app.config['SESSION_TYPE'] = 'filesystem'
    #sess.init_app(app)
    app.debug = True
    app.run('0.0.0.0', port=80)
