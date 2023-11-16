from flask import Flask,redirect,render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from sqlalchemy import text

from werkzeug.security import generate_password_hash,check_password_hash


# mydatabase connection
#helloo
local_server=True
app=Flask(__name__)
app.secret_key="rushdha"




# to config particular data
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://username:password@localhost/databasename'

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/slot'
db=SQLAlchemy(app)




class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

class User(UserMixin,db.Model):
    uid=db.Column(db.Integer,primary_key=True)
    srfid=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(20))
    dob=db.Column(db.String(20))
       

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/usersignup")
def usersignup():
    return render_template("usersignup.html")


@app.route("/userlogin")
def userlogin():
    return render_template("userlogin.html")
# when anyone sign in the submit btn then all the infrmtn will happen in signup
#/signup happen in main.py file
@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method=="POST":
        srfid=request.form.get('srf')
        email=request.form.get('email')
        dob=request.form.get('dob')
        #print(srfid,email,dob)
        encpassword=generate_password_hash(dob)
        from sqlalchemy import create_engine
        
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
        engine=engine.connect()
        #new_user=db.engine.execute(f"INSERT INTO `user` (`srfid`,`email`,`dob`) VALUES ('{srfid}','{email}','{encpassword}') ")
        new_user=User(srfid=srfid,email=email,dob=dob)
        db.session.add(new_user)
        db.session.commit()
                
       
    
        return 'USER added'
        
       

    return render_template("usersignup.html")
        

        




   


# testing whether db is connected or not

@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        return 'mydatabase is connected'
    except Exception as e:
        print(e)
        return f'mydatabase is not connected {e}'



app.run(debug=True)