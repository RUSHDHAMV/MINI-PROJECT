from flask import Flask,redirect,render_template
from flask_sqlalchemy import SQLAlchemy

# mydatabase connection

local_server=True
app=Flask(__name__)
app.secret_key="rushdha"


# to config particular data
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://username:password@localhost/databasename'

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/slot'
db=SQLAlchemy(app)


@app.route("/")
def home():
    return render_template("index.html")


app.run(debug=True)