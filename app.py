from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime
import pytz



app = Flask(__name__)

SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

'''
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)
'''

class Operacion(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(100))



    def __init__(self, amount, method, reason):
        
        self.amount = amount
        self.date_created = datetime.datetime.now(pytz.timezone('America/Caracas'))
        self.method = method
        self.reason = reason

    


    


    


#routes 

@app.route('/')
def home():
    operations = Operacion.query.all()
    ops = db.session.query(Operacion).all()
    sumList = []
    for op in operations:
        sumList.insert(0, op.amount)
        sumList2 = sum(sumList)
        

    return render_template('index.html', operations = operations, sumList2 = sumList2)

@app.route('/create', methods=['POST'])
def create():
    amount = request.form['amount']
    method = request.form['method']
    reason = request.form['reason']
    oper = Operacion(float(amount), method, reason)

    
    db.session.add(oper)
    db.session.commit()
    return redirect(url_for('home'))

'''
@app.route('/suma')
def suma():
    
    data = Operacion.query.all()
    suma = []
    for a in data:
        i = a.amount
        suma.append(i)
        suma = sum(suma)
        return render_template('index.html', suma = suma)

 '''

    




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
