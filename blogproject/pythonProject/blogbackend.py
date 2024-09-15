import flask
from flask import Flask,render_template,session,request,redirect,url_for,flash
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)
app.secret_key="hello"
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:anjanawatal%40240405@127.0.0.1:3306/mydatabase'
db=SQLAlchemy(app)

class logindata(db.Model):
    gmail=db.Column(db.String(255),unique=True,primary_key=True)
    userpassword=db.Column(db.String(255),unique=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if "user" in session:
        return render_template("blogfrontpage.html",visited=1)
    return render_template("blogfrontpage.html",visited=0)

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        cemail=logindata.query.filter_by(gmail=email).first()
        if cemail!=None:
            flash("user account already exists")
            return render_template("blogsignup.html")
        else:
           response=logindata(gmail=email,userpassword=password)
           db.session.add(response)
           db.session.commit()
           session['user']=email
           return render_template("blogfrontpage.html",visited=1)
    return render_template("blogsignup.html",visited=0)

@app.route('/login',methods=['GET','POST'])
def login():
    visited=0
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        cemail=logindata.query.filter_by(gmail=email).first()
        if cemail==None:
            flash("Email not found please create account first")
            return render_template("bloglogin.html")
        elif not email:
            flash("Not written anything in the email field")
            return render_template("bloglogin.html")
        elif not password:
            flash("Not written anything in the password field")
            return render_template("bloglogin.html")
        elif cemail.userpassword!=password:
            flash("Wrong username or password")
            return render_template("bloglogin.html")
        else:
            session['user']=email
        if "user" in session:
            visited=1
        else:
            visited=0
        return render_template("blogfrontpage.html",visited=visited)
    return render_template("bloglogin.html")

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for("index"))

if __name__=="__main__":
    app.run(debug=True)