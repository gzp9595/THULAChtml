#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import *
import os
import json
import random
import string
import time
import MySQLdb
import ConfigParser
import codecs

app = Flask(__name__)
server_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(server_dir, 'config.py')
app.config.from_pyfile(config_file)


def handle_static(res, name):
    # if not app.config['DEBUG']:
    #     abort(403)
    #     return
    return send_from_directory(os.path.dirname(os.path.realpath(__file__))+'/templates/'+res, name)

_tpl_dir = os.path.dirname(os.path.realpath(__file__))+'/templates/'
_source_dir = os.path.dirname(os.path.realpath(__file__))+'/source/'
conf = ConfigParser.ConfigParser()


def send_page(name):
    return send_from_directory(_tpl_dir, name)


@app.route('/js/<path:name>')
def static_js(name):
    return handle_static('js', name)


@app.route('/styles/<path:name>')
def static_css(name):
    return handle_static('styles', name)


@app.route('/image/<path:name>')
def static_img(name):
    return handle_static('image', name)


@app.route('/img/<int:img_id>')
def get_img(img_id):
    return handle_static('img', img_id+'.jpg')


@app.route('/css/<path:name>')
def get_assets(name):
    return handle_static('css', name)


@app.route('/fonts/<path:name>')
def get_fonts(name):
    return handle_static('fonts', name)


@app.route('/source/<path:name>')
def get_source(name):
    if('user' in session and session['user'] == 1):
        return send_from_directory(_source_dir, name)
    return abort(404)


@app.route('/')
def readme():
    return send_page("readme.html")


@app.route('/index')
def index():
    return send_page("index.html")


@app.route('/message')
def message():
    return send_page("message.html")


@app.route('/register')
def register():
    return send_page("register.html")


@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    session['user'] = 1
    s = request.form
    if(s["name"] == "" or s["orgname"] == "" or s['email'] == "" or s['optionsRadios'] != u"agree"):
            return redirect("message")
    else:
        try:
            conn = MySQLdb.connect(
                host=conf.get("db","db_host"),
                user=conf.get("db","db_name"),
                passwd=conf.get("db","db_password"),
                db=conf.get("db","db_database"),
                charset="utf8")
            cursor = conn.cursor()

            # insert into tasks
            insertSql = 'insert into message values(null,\'' \
                        + s["name"] + '\',\''\
                        + s["orgname"] + '\',\''\
                        + s["email"] + '\',\'' \
                        + s['address'] + '\',\'' \
                        + s['telephone'] + '\')'
            cursor.execute(insertSql)
            conn.commit()

        except MySQLdb.Error, e:
            print"Mysql Error %d: %s" % (e.args[0], e.args[1])
            return redirect("message")
        finally:
            cursor.close()
            conn.close()
        return send_page("download.html")


@app.route("/demo")
def demo():
    return send_page("demo.html")


@app.route("/getResult", methods=['POST'])
def getResult():
    s = request.form['context']
    s = s[:1000]
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    f = codecs.open("temp/" + salt, "w", "utf-8")
    f.write(s)
    f.close()
    ans = os.popen("./Algorithm/thulac -model_dir Algorithm/models <"+"temp/"+salt)
    return ans.read()

# @app.route("/getmarkdown")
# def getMarkdown():
#     f = open("txt/README.md","r")
#     s = f.read()
#     return s



if __name__ == '__main__':
    # if app.config['DEBUG']:
    conf.read("config.cfg")
    app.run()
