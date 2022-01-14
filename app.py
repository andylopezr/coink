from flask import Flask, request, jsonify, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

# Initializing app
app = Flask(__name__)

# Using secret key for flash messages
app.config['SECRET_KEY'] = '2496c6d62b0c524876c5e05ce420677651e7e38bd0383609'

fields = [{'name': '',
             'email': '',
             'city': ''},
            ]

homedir = os.path.abspath(os.path.dirname(__file__))
            
# Database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(homedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing DB
db = SQLAlchemy(app)

# Initializing Marshmallow
ma = Marshmallow(app)

# Form Model
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, city):
        self.name = name
        self.email = email
        self.city = city

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

# Route to get user fields
@app.route('/post', methods=['POST'])
def add_fields():
    name = request.json['name']
    email = request.json['email']
    city = request.json['city']

    new_reg = Form(name, email, city)

    db.session.add(new_reg)
    db.session.commit()

    return form_schema.jsonify(new_reg)

# Get all regs
@app.route('/get', methods=['GET'])
def get_all():
    all_regs = Form.query.all()
    result = forms_schema.dump(all_regs)
    return jsonify(result)

# Obtain data from form

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
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('create.html')


# Run Server
if __name__ == '__main__':
    app.run(debug=True)