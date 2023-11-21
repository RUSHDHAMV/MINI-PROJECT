from flask import Flask, flash, json,redirect,render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from sqlalchemy.exc import OperationalError, ProgrammingError


#from sqlalchemy import create_engine

from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Mail

# mydatabase connection
#helloo
local_server=True
app=Flask(__name__)
app.secret_key="rushdha"



with open('config.json','r') as c:
    params=json.load(c)["params"]


app.config.update(
     MAIL_SERVER='smtp.gmail.com',
     MAIL_PORT='465',
     MAIL_USE_SSL=True,
     MAIL_USERNAME='gmail-user',
     MAIL_PASSWORD='gmail-password'
 )
mail = Mail(app)



#this is for getting unique access
login_manager=LoginManager(app)
login_manager.login_view='login'


# to config particular data
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://username:password@localhost/databasename'

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/slot'
db=SQLAlchemy(app)






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 




class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

class User(UserMixin,db.Model):
   id=db.Column(db.Integer,primary_key=True)
   srfid=db.Column(db.String(20),unique=True)
   email=db.Column(db.String(100))
   dob=db.Column(db.String(2000))

class Hospitaluser(UserMixin,db.Model):
   hid=db.Column(db.Integer,primary_key=True)
   hcode=db.Column(db.String(20))
   email=db.Column(db.String(100))
   password=db.Column(db.String(1000))
       
       

@app.route("/")
def home():
    return render_template("index.html")

#@app.route("/usersignup")
#def usersignup():
 #   return render_template("usersignup.html")

#@app.route("/userlogin")
#def userlogin():
 #   return render_template("userlogin.html")



# when anyone sign in the submit btn then all the infrmtn will happen in signup
#/signup happen in main.py file
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        srfid=request.form.get('srf')
        email=request.form.get('email')
        dob=request.form.get('dob')
        #print(srfid,email,dob)
        #encrypting dob ,at the time of login it decrypt
        encpassword=generate_password_hash(dob)
        user=User.query.filter_by(srfid=srfid).first()
        
         # to ckeck user is already exist

        emailUser=User.query.filter_by(email=email).first()
        if user or emailUser:
            flash("Email or srfid is already taken","warning")
            return render_template("usersignup.html")
        



        #engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
        #engine=engine.connect()
        #new_user=db.engine.execute(f"INSERT INTO `user` (`srfid`,`email`,`dob`) VALUES ('{srfid}','{email}','{encpassword}') ")
        new_user=User(srfid=srfid,email=email,dob=encpassword)
        db.session.add(new_user)
        db.session.commit()
        
        flash("SignUp Success Please Login","success")
        return render_template("userlogin.html")
        
       

    return render_template("usersignup.html")
        

@app.route('/login',methods=['POST','GET'])       
def login():
    if request.method=="POST":
        srfid=request.form.get('srf')
        dob=request.form.get('dob')
        user=User.query.filter_by(srfid=srfid).first()
        if user and check_password_hash(user.dob,dob):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("userlogin.html")


    return render_template("userlogin.html")

   
#admin
@app.route('/admin',methods=['POST','GET'])       
def admin():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        if(username==params['user'] and password==params['password']):
            session['user']=username
            flash("Login success","info")
            return render_template("addHosUser.html")
        else:
             flash("Invalid Credentials","danger")



    return render_template("admin.html")





@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successfully","warning")
    return redirect(url_for('login'))


@app.route('/addHospitalUser',methods=['POST','GET'])
def hospitalUser():
   
    if('user' in session and session['user']=="admin"):
      
        if request.method=="POST":
            hcode=request.form.get('hcode')
            email=request.form.get('email')
            password=request.form.get('password')        
            encpassword=generate_password_hash(password)  
            hcode=hcode.upper()      
            emailUser=Hospitaluser.query.filter_by(email=email).first()
            if  emailUser:
                flash("Email or srif is already taken","warning")
         
            #db.engine.execute(f"INSERT INTO `hospitaluser` (`hcode`,`email`,`password`) VALUES ('{hcode}','{email}','{encpassword}') ")
            query=Hospitaluser(hcode=hcode,email=email,password=encpassword)
            db.session.add(query)
            db.session.commit()

            # my mail starts from here 
           
            mail.send_message('COVID CARE CENTER',sender=params['gmail-user'],recipients=[email],body=f"Welcome thanks for choosing us\nYour Login Credentials Are:\n Email Address: {email}\nPassword: {password}\n\nHospital Code {hcode}\n\n Do not share your password\n\n\nThank You..." )

            flash("Data Sent and Inserted Successfully","warning")
            return render_template("addHosUser.html")

        else:   
             flash("Login and try Again","warning")
             return render_template("/admin")
    





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
    
@app.route('/logoutadmin')

def logoutadmin():
    session.pop('user')
    flash("You are Logout admin","primary")
    return redirect('/admin')




app.run(debug=True)