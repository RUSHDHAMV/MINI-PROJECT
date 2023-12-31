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


# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT='465',
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME='gmail account',
#     MAIL_PASSWORD='gmail account password'
# )
#mail = Mail(app)



#this is for getting unique access
login_manager=LoginManager(app)
login_manager.login_view='login'


# to config particular data
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://username:password@localhost/databasename'

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/slot'
db=SQLAlchemy(app)






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) or Hospitaluser.query.get(int(user_id))





class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

class User(UserMixin,db.Model):
   id=db.Column(db.Integer,primary_key=True)
   srfid=db.Column(db.String(20),unique=True)
   email=db.Column(db.String(100))
   dob=db.Column(db.String(2000))
   

class Hospitaluser(UserMixin,db.Model):
   id=db.Column(db.Integer,primary_key=True)
   hcode=db.Column(db.String(20))
   email=db.Column(db.String(100))
   password=db.Column(db.String(1000))

class Hospitaldata(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20),unique=True)
    hname=db.Column(db.String(100))
    normalbed=db.Column(db.Integer)
    hicubed=db.Column(db.Integer)
    icubed=db.Column(db.Integer)
    vbed=db.Column(db.Integer)




class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(50))
    normalbed=db.Column(db.Integer)
    hicubed=db.Column(db.Integer)
    icubed=db.Column(db.Integer)
    vbed=db.Column(db.Integer)
    querys=db.Column(db.String(50))
    date=db.Column(db.String(50))




class Bookingpatient(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    srfid=db.Column(db.String(20),unique=True)
    bedtype=db.Column(db.String(100))
    hcode=db.Column(db.String(20))
    spo2=db.Column(db.Integer)
    pname=db.Column(db.String(100))
    pphone=db.Column(db.String(100))
    paddress=db.Column(db.String(100))

       

@app.route("/")
def home():
    return render_template("index.html")

#@app.route("/usersignup")
#def usersignup():
 #   return render_template("usersignup.html")

#@app.route("/userlogin")
#def userlogin():
 #   return render_template("userlogin.html")





@app.route("/trigers")
def trigers():
    if('user' in session and session['user']=="admin"):
        query=Trig.query.all() 
        return render_template("trigers.html",query=query)
    else:   
             flash("Login and try Again","warning")
             return render_template("/addHosUser.html")
        


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


@app.route('/hospitallogin',methods=['POST','GET'])
def hospitallogin():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=Hospitaluser.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("hospitallogin.html")
        




    return render_template("hospitallogin.html")


   
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
           
            #mail.send_message('BED SLOT BOOKINGCENTER',sender=params['gmail-user'],recipients=[email],body=f"Welcome thanks for choosing us\nYour Login Credentials Are:\n Email Address: {email}\nPassword: {password}\n\nHospital Code {hcode}\n\n Do not share your password\n\n\nThank You..." )

            flash("Data Sent and Inserted Successfully","warning")
            return render_template("addHosUser.html")
        else:
            return render_template("/addHosUser.html")


    else:   
        flash("Login and try Again","warning")
        return render_template("/addHosUser.html")
    





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






def updatess(code):
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()
    return render_template("hospitaldata.html",postsdata=postsdata)



@app.route("/addhospitalinfo",methods=['POST','GET'])
def addhospitalinfo():
    email=current_user.email
    posts=Hospitaluser.query.filter_by(email=email).first()
    code=posts.hcode
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()

    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        nbed=request.form.get('normalbed')
        hbed=request.form.get('hicubeds')
        ibed=request.form.get('icubeds')
        vbed=request.form.get('ventbeds')
        #hcode wiil be in uppercase
        hcode=hcode.upper()
        #to check particular user is there
        huser=Hospitaluser.query.filter_by(hcode=hcode).first()
        #if already hcode is data added then it can update only
        hduser=Hospitaldata.query.filter_by(hcode=hcode).first()
        if hduser:
            flash("Data is already Present you can update it..","primary")
            return render_template("hospitaldata.html")
        #if user is there then execute this query
        if huser:            
            # db.engine.execute(f"INSERT INTO `hospitaldata` (`hcode`,`hname`,`normalbed`,`hicubed`,`icubed`,`vbed`) VALUES ('{hcode}','{hname}','{nbed}','{hbed}','{ibed}','{vbed}')")
            query=Hospitaldata(hcode=hcode,hname=hname,normalbed=nbed,hicubed=hbed,icubed=ibed,vbed=vbed)
            db.session.add(query)
            db.session.commit()
            flash("Data Is Added","primary")
            return redirect('/addhospitalinfo')
            

        else:
            flash("Hospital Code not Exist","warning")
            return render_template('/addhospitalinfo')




    return render_template("hospitaldata.html",postsdata=postsdata)

@app.route("/hedit/<string:id>",methods=['POST','GET'])
@login_required
def hedit(id):
    posts=Hospitaldata.query.filter_by(id=id).first()
  
    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        nbed=request.form.get('normalbed')
        hbed=request.form.get('hicubeds')
        ibed=request.form.get('icubeds')
        vbed=request.form.get('ventbeds')
        hcode=hcode.upper()
        # db.engine.execute(f"UPDATE `hospitaldata` SET `hcode` ='{hcode}',`hname`='{hname}',`normalbed`='{nbed}',`hicubed`='{hbed}',`icubed`='{ibed}',`vbed`='{vbed}' WHERE `hospitaldata`.`id`={id}")
        post=Hospitaldata.query.filter_by(id=id).first()
        post.hcode=hcode
        post.hname=hname
        post.normalbed=nbed
        post.hicubed=hbed
        post.icubed=ibed
        post.vbed=vbed
        db.session.commit()
        flash("Slot Updated","info")
        return redirect("/addhospitalinfo")

    # posts=Hospitaldata.query.filter_by(id=id).first()
    return render_template("hedit.html",posts=posts)


@app.route("/hdelete/<string:id>",methods=['POST','GET'])
@login_required
def hdelete(id):
    # db.engine.execute(f"DELETE FROM `hospitaldata` WHERE `hospitaldata`.`id`={id}")
    post=Hospitaldata.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash("Date Deleted","danger")
    return redirect("/addhospitalinfo")



@app.route("/pdetails",methods=['GET'])
@login_required
def pdetails():
    code=current_user.srfid
    print(code)
    data=Bookingpatient.query.filter_by(srfid=code).first()
    

    return render_template("details.html",data=data)




@app.route("/slotbooking",methods=['POST','GET'])
@login_required
def slotbooking():
    # query1=db.engine.execute(f"SELECT * FROM `hospitaldata` ")
    # query=db.engine.execute(f"SELECT * FROM `hospitaldata` ")
    query1=Hospitaldata.query.all()
    query=Hospitaldata.query.all()
    if request.method=="POST":
        
        srfid=request.form.get('srfid')
        bedtype=request.form.get('bedtype')
        hcode=request.form.get('hcode')
        spo2=request.form.get('spo2')
        pname=request.form.get('pname')
        pphone=request.form.get('pphone')
        paddress=request.form.get('paddress')  
        check2=Hospitaldata.query.filter_by(hcode=hcode).first()
        checkpatient=Bookingpatient.query.filter_by(srfid=srfid).first()
        if checkpatient:
            flash("already srd id is registered ","warning")
            return render_template("booking.html",query=query,query1=query1)
        
        if not check2:
            flash("Hospital Code not exist","warning")
            return render_template("booking.html",query=query,query1=query1)

        code=hcode
        # dbb=db.engine.execute(f"SELECT * FROM `hospitaldata` WHERE `hospitaldata`.`hcode`='{code}' ")  
        
        dbb=Hospitaldata.query.filter_by(hcode=hcode).first()      
        bedtype=bedtype
        if bedtype=="NormalBed" and dbb:       
            
            seat=dbb.normalbed
            print(seat)
            ar=Hospitaldata.query.filter_by(hcode=code).first()
            ar.normalbed=seat-1
            db.session.commit()
                
            
        elif bedtype=="HICUBed" and dbb:
            seat=dbb.hicubed
            print(seat)
            ar=Hospitaldata.query.filter_by(hcode=code).first()
            ar.hicubed=seat-1
            db.session.commit()

        elif bedtype=="ICUBed" and dbb:
            seat=dbb.icubed
            print(seat)
            ar=Hospitaldata.query.filter_by(hcode=code).first()
            ar.icubed=seat-1
            db.session.commit()

        elif bedtype=="VENTILATORBed" and dbb:
            seat=dbb.vbed
            ar=Hospitaldata.query.filter_by(hcode=code).first()
            ar.vbed=seat-1
            db.session.commit()
        else:
            pass

        check=Hospitaldata.query.filter_by(hcode=hcode).first()
        if check!=None:
            if(seat>0 and check):
                res=Bookingpatient(srfid=srfid,bedtype=bedtype,hcode=hcode,spo2=spo2,pname=pname,pphone=pphone,paddress=paddress)
                db.session.add(res)
                db.session.commit()
                flash("Slot is Booked kindly Visit Hospital for Further Procedure","success")
                return render_template("booking.html",query=query,query1=query1)
            else:
                flash("Something Went Wrong","danger")
                return render_template("booking.html",query=query,query1=query1)
        else:
            flash("Give the proper hospital Code","info")
            return render_template("booking.html",query=query,query1=query1)
            
    
    return render_template("booking.html",query=query,query1=query1)


app.run(debug=True)