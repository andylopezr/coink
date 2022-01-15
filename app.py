from flask import Flask, request, jsonify, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os
import logging

# Initializing app
app = Flask(__name__)

fields = [{'name': '',
             'email': '',
             'city': ''},
            ]

homedir = os.path.abspath(os.path.dirname(__file__))
        
# Database location + secret key for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(homedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '2496c6d62b0c524876c5e05ce420677651e7e38bd0383609'

# Initializing DB
db = SQLAlchemy(app)

# Initializing Marshmallow
ma = Marshmallow(app)

# Form Model
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, city):
        self.name = name
        self.email = email
        self.city = city

# Creates the DB
db.create_all()

# Form Schema
class FormSchema(ma.Schema):
    class Meta:
       fields = ('id', 'name', 'email', 'city')

# Initializing Schema
form_schema = FormSchema()
forms_schema = FormSchema(many=True)

# Displaying index
@app.route('/')
def index():
    return render_template('index.html', fields=fields)

# Obtain form data
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        
        if not name:
            flash('Name is required')
        elif not email:
            flash('Email is required')
        elif not city:
            flash('City is required')
        else:
            fields.append({'name': name, 'email': email, 'city': city})
            new_reg = Form(name, email, city)
            db.session.add(new_reg)
            try:
                db.session.commit()
                # Logging user creation event
                logging.basicConfig(filename='creation.log', encoding='utf-8', level=logging.DEBUG)
                logging.info('{} - {} \n'.format(name, datetime.now()))
            except Exception as e:
                #logging
                flash('Name or Email already exists')
            return render_template('create.html')

    return render_template('create.html')


# Get all regs
@app.route('/all', methods=['GET'])
def get_all():
    all_regs = Form.query.all()
    results = forms_schema.dump(all_regs)
    return render_template('all.html', results=results)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
