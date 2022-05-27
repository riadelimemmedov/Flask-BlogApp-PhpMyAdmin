from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from functools import wraps
from passlib.hash import sha256_crypt

#!Create Flask Object
app = Flask(__name__)
app.secret_key = 'blogdsa3@*51!3#'

#!login_required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:#if user not logged in
            flash('This page not loading because you are not logged in site...','info')
            return redirect(url_for('loginView'))
    return decorated_function

#!Connect Mysql and Xampp Server
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ybblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"#return queryset data as django quersets
mysql = MySQL(app)

#!RegisterForm
class RegisterForm(Form):
    name = StringField(label='Isim Soyisim',validators=[validators.Length(min=4,max=25)])
    username = StringField(label='Kullanici Adi',validators=[validators.Length(min=5,max=35)])
    email = StringField(label='Email Adresi',validators=[validators.Email(message='Lutfen Gecerli Bir Email Adresi Girin...')])
    password = PasswordField(label='Parola:',validators=[
        validators.DataRequired(message='Lutfen bit parola belirleyin'),
        validators.EqualTo(fieldname='confirm',message='Parolaniz Uyusmuyor')
    ])
    confirm = PasswordField('Parola Tekrar')

#!ArticleForm
class ArticleForm(Form):
    title = StringField(label='Makale Basligi',validators=[validators.Length(min=5,max=100)])
    content = TextAreaField(label='Makale Icerigi',validators=[validators.Length(min=10)])
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

#!articleDetailView
@app.route('/article/detail/<int:id>')
def articleDetailView(id):
    cursor = mysql.connection.cursor()
    qs = "SELECT * FROM articles WHERE id=%s"# => %s yazilmasindaki sebeb sorgunu dynamic bir sekilde yazmag ucundur => %s ifadesi
    result = cursor.execute(qs,(id,))
    if result > 0:
        article = cursor.fetchone()
        return render_template('blogtemplates/article.html',article=article)
    else:
        return render_template('blogtemplates/article.html')

#!dashboardView
@app.route('/dashboard')
@login_required
def dashboardView():
    cursor = mysql.connection.cursor()
    qs  = "SELECT * FROM articles WHERE author=%s"
    result = cursor.execute(qs,(session['username_in'],))
    if result > 0:
        articles = cursor.fetchall()
        return render_template('blogtemplates/dashboard.html',articles=articles)
    else:
        return render_template('blogtemplates/dashboard.html')

#!addArticle
@app.route('/addarticle',methods=['GET','POST'])
def addArticle():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        
        cursor = mysql.connection.cursor()
        qs = "INSERT INTO articles(title,author,content) VALUES(%s,%s,%s)"
        cursor.execute(qs,(title,session['username_in'],content))
        mysql.connection.commit()
        cursor.close()
        
        flash('Makale Basariyla Eklendi','success')
        return redirect(url_for('dashboardView'))
    return render_template('blogtemplates/addarticle.html',form=form)

#!deleteArticle
@app.route('/delete/<int:id>')
@login_required
def deleteArticle(id):
    cursor = mysql.connection.cursor()
    qs = "SELECT * FROM articles WHERE author=%s AND id=%s"
    result = cursor.execute(qs,(session['username_in'],id))
    if result > 0:
        qs2 = "DELETE FROM articles WHERE id=%s"
        cursor.execute(qs2,(id,))
        mysql.connection.commit()
        flash('Successfully Deleted Article')
        return redirect(url_for('dashboardView'))
    else:
        flash('This article not found or not permissions deleted article','danger')
        return redirect(url_for('indexView'))


@app.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def updateArticle(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qs_get_data = "SELECT * FROM articles WHERE author=%s AND id=%s"
        result = cursor.execute(qs_get_data,(session['username_in'],id))
        if result == 0:
            flash('This article not found or not permissions updated')
            return redirect(url_for('indexView'))
        else:
            article = cursor.fetchone()
            form = ArticleForm()
            form.title.data = article['title']
            form.content.data = article['content']
            return render_template('blogtemplates/update.html',form=form)
    else:#if request.method == 'POST'
        form = ArticleForm(request.form)
        newTitle = form.title.data
        newContent = form.content.data
        
        cursor = mysql.connection.cursor()
        qs_update_data = "UPDATE articles SET title=%s,content=%s WHERE id=%s"
        cursor.execute(qs_update_data,(newTitle,newContent,id))
        mysql.connection.commit()
        flash('Updated Article Successfully','success')
        return redirect(url_for('dashboardView'))
    
#!articleListView
@app.route('/articles')
def articleListView():
    cursor = mysql.connection.cursor()#yeni mysql connect ol cursoru baslat menasinda cagir cursor() funksiyasini ele bil
    qs = "SELECT * FROM articles"
    result = cursor.execute(qs)
    
    if result > 0:
        articles = cursor.fetchall()
        return render_template('blogtemplates/articles.html',articles=articles)
    else:
        return render_template('blogtemplates/articles.html')

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

#!loginView
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
                session['logged_in'] = True
                session['username_in'] = username_entered
                return redirect(url_for('indexView'))
            else:
                flash('Please Correct Password or Username','danger')
                return redirect(url_for('loginView'))
        else:#if not user found in database
            flash('Not User Found In Database...','danger')
            return redirect(url_for('loginView'))
    return render_template('blogtemplates/login.html',form=form)

#!logoutView
@app.route('/logout')
def logoutView():
    session.clear()
    return redirect(url_for('indexView'))

#!__name__ == '__main__'
if __name__ == '__main__':
    app.run(debug=True)