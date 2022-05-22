from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

#!Create Flask Object
app = Flask(__name__)
app.secret_key = 'blogdsa3@*51!3#'

#!Connect Mysql and Xampp Server
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ybblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"#return queryset data as django quersets
mysql = MySQL(app)

#!Register Form
class RegisterForm(Form):
    name = StringField(label='Isim Soyisim',validators=[validators.Length(min=4,max=25)])
    username = StringField(label='Kullanici Adi',validators=[validators.Length(min=5,max=35)])
    email = StringField(label='Email Adresi',validators=[validators.Email(message='Lutfen Gecerli Bir Email Adresi Girin...')])
    password = PasswordField(label='Parola:',validators=[
        validators.DataRequired(message='Lutfen bit parola belirleyin'),
        validators.EqualTo(fieldname='confirm',message='Parolaniz Uyusmuyor')
    ])
    confirm = PasswordField('Parola Tekrar')

#!indexView
@app.route('/')
def indexView():
    context = {
        "name":"Kenan",
        "surname":"Suleymanov"
    }
    return render_template('blogtemplates/index.html',context=context)

#!aboutView
@app.route('/about')
def aboutView():
    context = {
        "description":"Welcome my blog site"
    }
    return render_template('blogtemplates/about.html',context=context)

#!detailView
@app.route('/detail/<int:id>')
def detailView(id):
    return f"Detail Post Id - {id}"

@app.route('/register',methods=['GET','POST'])
def registerView():
    form = RegisterForm(request.form)#form icindeki deyerleri getirir
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data 
        email = form.email.data 
        password = sha256_crypt.encrypt(form.password.data)
        
        cursor = mysql.connection.cursor()
        query = "INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(name,email,username,password))
        mysql.connection.commit()
        cursor.close()
        flash('Başarıyla Kayıt Oldunuz...','success')
        return redirect(url_for('indexView'))#yeni indexView adli funksiya isleyende hemin funksiyanin url ni getsin ele bil url_for o isi gorur
    else:
        return render_template('blogtemplates/register.html',form=form)

#!__name__ == '__main__'
if __name__ == '__main__':
    app.run(debug=True)