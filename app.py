from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
import datetime
import pytz
from datetime import date as dt




app = Flask(__name__)


#APP CONFIG

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'eleazar'
db = SQLAlchemy(app)

#LOGIN MANAGER

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# MODELS

class Operacion(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(100))



    def __init__(self, amount, method, reason):
        
        self.amount = amount
        self.date_created = datetime.date.today()#datetime.datetime.now(pytz.timezone('America/Caracas'))
        self.method = method
        self.reason = reason

class User(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    





    
#ROUTES 

@app.route('/signup', methods=['POST', 'GET'])
@login_required
def signup():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        #si el usuario existe, lo devuelve a la pagina de registro
        if user:
            flash('Usuario ya existe')
            return redirect(url_for('signup'))

        #crea usuario nuevo
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        return render_template('signup.html')
    else:
        return render_template('login.html')


@app.route('/', methods=['POST','GET'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('USUARIO O CLAVE EQUIVOCADA, INTENTE DE NUEVO')
            return redirect(url_for('login'))

        
        login_user(user)
        return (redirect(url_for('home')))

        


    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    
    today = datetime.date.today()
    operations = Operacion.query.filter(Operacion.date_created == today).all()
    ops = db.session.query(Operacion).all()

    listZelle = [0]
    listPunto = [0]
    listEfectivoD = [0]
    listEfectivoBS = [0]
    fondoCajaD = 0.00
    fondoCajaBs = 0.00
    sumZelle = 0.00
    sumPunto = 0.00
    sumEfectivoD = 0.00
    sumEfectivoBS = 0.00




    def currencyFormat(monto):
        currency = "{:,.2f}".format(monto)
        return currency





    for op in operations:
        if 'ZELLE' in op.method.upper():
            listZelle.insert(0, op.amount)
            sumZelle = sum(listZelle)
            

        if 'PUNTO' in op.method.upper():
            listPunto.insert(0, op.amount)
            sumPunto = sum(listPunto)

        if 'DOLARES EFECTIVO' in op.method.upper():
            listEfectivoD.insert(0, op.amount)
            sumEfectivoD = sum(listEfectivoD)
            

        if 'BOLIVARES EFECTIVO' in op.method.upper():
            listEfectivoBS.insert(0, op.amount)
            sumEfectivoBS = sum(listEfectivoBS)

        if 'FONDO DE CAJA DOLARES' in op.method.upper():
            fondoCajaD = op.amount

        if 'FONDO DE CAJA BOLIVARES' in op.method.upper():
            fondoCajaBs = op.amount
            
    
    venta_total_dolares = sumZelle + sumEfectivoD
    venta_total_bolivares = sumPunto + sumEfectivoBS


    return render_template('prueba.html', operations = operations , sumZelle = currencyFormat(sumZelle), sumPunto = currencyFormat(sumPunto), sumEfectivoBS = currencyFormat(sumEfectivoBS) , 
    venta_total_dolares = currencyFormat(venta_total_dolares), venta_total_bolivares = currencyFormat(venta_total_bolivares), sumEfectivoD = currencyFormat(sumEfectivoD), fondoCajaD = currencyFormat(fondoCajaD), fondoCajaBs = currencyFormat(fondoCajaBs))

@app.route('/create', methods=['POST'])
@login_required
def create():
    amount = request.form['amount']
    method = request.form['method']
    reason = request.form['reason']
    

    def floatToNegative(monto):

        monto = '-'+str(monto)
        monto = float(monto)
        return monto

    if 'DEVOLUCION' in reason.upper():#and 'ZELLE' in method.upper() or 'PUNTO' in method.upper() or 'DOLARES EFECTIVO' in method.upper() or 'BOLIVARES EFECTIVO' in method.upper():
        amount = floatToNegative(amount)

    oper = Operacion(float(amount), method, reason)

    
    db.session.add(oper)
    db.session.commit()
    return redirect(url_for('home'))



@app.route('/informes', methods=['POST', 'GET'])
@login_required
def informes():

    if request.method == 'POST':

        desde = request.form['desde']
        hasta = request.form['hasta']

        informe = Operacion.query.filter(Operacion.date_created <= hasta).filter(Operacion.date_created >= desde).all()

        
        return render_template('informes.html', informe = informe, desde = desde, hasta = hasta)
    else:
        return render_template('informes.html')

    





#Start App

if __name__ == '__main__':
    app.run(debug=True)


