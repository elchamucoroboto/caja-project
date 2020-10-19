from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


#routes 

@app.route('/')
def home():
    return 'hello world'


# Models

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return'<User %r>' % self.username




#start app
if __name__ == '__main__':
    app.run(debug=True)
