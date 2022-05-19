from flask import Flask,render_template

app = Flask(__name__)

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

#!__name__ == '__main__'
if __name__ == '__main__':
    app.run(debug=True)