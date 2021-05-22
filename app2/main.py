from flask import Flask,render_template,request,redirect,session
from  flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app=Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-pass']
)
mail = Mail(app)

app.secret_key = "super secret key"
app.secret_key = "super_str"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Contacts(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    message=db.Column(db.String(500),nullable=False)

    
    def __repr__(self) -> str:
        return f"{self.sno} + {self.message}"


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method=="POST":
        name=request.form.get('name')
        email=request.form.get('email')
        message=request.form.get('message')
        entry=Contacts(name=name,email=email,message=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New report from DealerBot by ' + name,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body=message
                          )
    return render_template('contact.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login",methods=["GET","POST"])
def login():
    if 'uname' in session and session ['uname'] ==params['admin-user']:
        return render_template("admin.html",params=params)
    if request.method == "POST":
        username=request.form.get('username')
        password=request.form.get('password')
        session['uname']=username
        if username==params['admin-user'] and password==params['admin-pass']:
            return redirect("/admin")
        else:
            return redirect("/login")        
    return render_template('login.html',params=params)

@app.route("/admin")
def admin():
    if 'uname' in session and session ['uname'] ==params['admin-user']:
        report=Contacts.query.all()
        return render_template('admin.html',params=params,report=report)
    else:
        return redirect("/login")

@app.route("/login1",methods=["GET","POST"])
def login1():
    if 'uname1' in session and session ['uname1'] ==params['admin-user2']:
        return render_template("admin2.html",params=params)
    if request.method == "POST":
        username=request.form.get('username')
        password=request.form.get('password')
        session['uname1']=username
        if username==params['admin-user2'] and password==params['admin-pass2']:
            return redirect("/admin2")
        else:
            return render_template('login1.html',params=params)        
    return render_template('login1.html',params=params)

@app.route("/admin2")
def admin2():
    if 'uname1' in session and session ['uname1'] ==params['admin-user2']:
        report=Contacts.query.all()
        return render_template('admin2.html',params=params,report=report)
    else:
        return redirect("/login")


@app.route("/halloffame")
def halloffame():
    return render_template('donators.html')



@app.route("/donate")
def donate():
    return render_template('donate.html')

@app.route("/logout")
def logout():
        if 'uname' in session and session ['uname'] ==params['admin-user']:
            session.pop('uname')
            return redirect("/login")


@app.route("/logout1")
def logout1():
        if 'uname1' in session and session ['uname1'] ==params['admin-user2']:
            session.pop('uname1')
            return redirect("/login")

if __name__=="__main__":
    app.run(debug=True,port=8000)
