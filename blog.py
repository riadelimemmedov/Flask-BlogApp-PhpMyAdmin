from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

#!Create Flask Object
app = Flask(__name__)

#!Connect Mysql and Xampp Server
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ybblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"#return queryset data as django quersets
mysql = MySQL(app)

#!Views
@app.route('/')
def indexView():
    context = {
        "name":"Kenan",
        "surname":"Suleymanov"
    }
    return render_template('blogtemplates/index.html',context=context)

@app.route('/about')
def aboutView():
    context = {
        "description":"Welcome my blog site"
    }
    return render_template('blogtemplates/about.html',context=context)

@app.route('/detail/<int:id>')
def detailView(id):
    return f"Detail Post Id - {id}"

#!__name__ == '__main__'
if __name__ == '__main__':
    app.run(debug=True)