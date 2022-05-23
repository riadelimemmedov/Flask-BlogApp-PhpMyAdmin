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

#!LoginForm
class LoginForm(Form):
    username = StringField(label='Kullanici Adi')
    password = PasswordField(label='Sifreniz')

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

#!registerView
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
        flash('Successfully Register...','success')
        return redirect(url_for('loginView'))#yeni indexView adli funksiya isleyende hemin funksiyanin url ni getsin ele bil url_for o isi gorur
    else:
        return render_template('blogtemplates/register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def loginView():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username_entered = form.username.data
        password_entered = form.password.data
        
        cursor = mysql.connection.cursor()
        qs = "SELECT * FROM users WHERE username=%s"
        
        result_qs = cursor.execute(qs,(username_entered,))#result returned object list lenght
        print('Username Single or Username List')
        #print(result_qs)
        #print(cursor.fetchone())
        
        if result_qs>0:#if have data sql
            data_qs = cursor.fetchone()
            real_password = data_qs['password']
            print('Real Password ',real_password)
            print('Entered password ', password_entered)
            if sha256_crypt.verify(password_entered,real_password):
                flash('Successfully Logged...','success')
                return redirect(url_for('indexView'))
            else:
                flash('Please Correct Password or Username','danger')
                return redirect(url_for('loginView'))
        else:#if not user found in database
            flash('Not User Found In Database...','danger')
            return redirect(url_for('loginView'))
        
        
        
    return render_template('blogtemplates/login.html',form=form)

#!__name__ == '__main__'
if __name__ == '__main__':
    app.run(debug=True)