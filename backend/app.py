from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:1234@localhost/evaluatedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['debug'] = True

db = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)

    Discipline = Base.classes.discipline
    Lecture = Base.classes.lecture
    Evaluation = Base.classes.evaluation
    Professor = Base.classes.professor
    Report = Base.classes.report
    Role = Base.classes.role
    User = Base.classes.user
    Department = Base.classes.department

    session = Session(db)

'''
CRUD USUÁRIO
'''

@app.route('/')
def index():
    results = session.query(User).all()
    return render_template('index.html', users=results)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        matricula = request.form['matricula']
        curso = request.form['curso']
        
        new_user = User(registry=matricula, name=nome, email=email, password=senha, course=curso, role_id=2)
        session.add(new_user)
        session.commit()
        return redirect('/')
    
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = session.query(User).get(id)
    if request.method == 'POST':
        user.name = request.form['nome']
        user.email = request.form['email']
        user.password = request.form['senha']
        user.registry = request.form['matricula']
        user.course = request.form['curso']
        
        session.commit()
        return redirect('/')
    
    return render_template('edit.html', user=user)

@app.route('/delete/<int:id>')
def delete(id):
    user = session.query(User).get(id)
    session.delete(user)
    session.commit()
    return redirect('/')

'''
CRUD AVALIAÇÃO
'''

