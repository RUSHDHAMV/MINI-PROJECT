from flask import Flask,redirect,render_template
from flask_sqlalchemy import SQLAlchemy

# mydatabase connection
#helloo
local_server=True
app=Flask(__name__)
app.secret_key="rushdha"


# to config particular data
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://username:password@localhost/databasename'

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost/slot'
db=SQLAlchemy(app)

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    

@app.route("/")
def home():
    return render_template("index.html")

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