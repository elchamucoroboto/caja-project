from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import datetime
import pytz



app = Flask(__name__)

SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)

class Operacion(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, amount):
        
        self.amount = amount
        self.date_created = datetime.datetime.now(pytz.timezone('America/Caracas'))

    

'''
op1 = Operacion(22.22)

db.session.add(op1)

ops = Operacion.query.all()
print (ops)
'''
    


    


#routes 

'''

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks = tasks)

@app.route('/create', methods=['POST'])
def create():
    task = Task(content=request.form['task'], done=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<id>')
def delete(id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for('home'))

'''

#Start App

if __name__ == '__main__':
    app.run(debug=True)
