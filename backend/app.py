from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:1234@localhost/evaluatedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'test'
app.config['SESSION_TYPE'] = 'filesystem'

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

    Session = Session(db)

'''
CRUD USUÁRIO
'''

@app.route('/')
def index():
    results = Session.query(User).all()
    if session.get('user_id'):
        return render_template('index.html', users=results)
    else:
        return redirect('/login')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        matricula = request.form['matricula']
        curso = request.form['curso']
        
        new_user = User(registry=matricula, name=nome, email=email, password=senha, course=curso, role_id=2)
        Session.add(new_user)
        Session.commit()
        return redirect('/')
    
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = Session.query(User).get(id)
    if request.method == 'POST':
        user.name = request.form['nome']
        user.email = request.form['email']
        user.password = request.form['senha']
        user.registry = request.form['matricula']
        user.course = request.form['curso']
        
        Session.commit()
        return redirect('/')
    
    return render_template('edit.html', user=user)

@app.route('/delete/<int:id>')
def delete(id):
    user = Session.query(User).get(id)
    Session.delete(user)
    Session.commit()
    return redirect('/')

'''
CRUD AVALIAÇÃO
'''

@app.route('/evaluations')
def evaluations():
    evaluations = Session.query(Evaluation).all()
    return render_template('evaluations.html', evaluations=evaluations)

@app.route('/evaluation/create', methods=['GET', 'POST'])
def create_evaluation():
    if request.method == 'POST':
        class_discipline = request.form['class_discipline']
        class_number = request.form['class_number']
        class_period = request.form['class_period']
        description = request.form['description']
        rating = request.form['rating']
        user_id = request.form['user_id']
        
        new_evaluation = Evaluation(
            class_discipline_code=class_discipline,
            class_number=class_number,
            class_period=class_period,
            description=description,
            rating=int(rating),
            user_id=int(user_id)
        )
        
        Session.add(new_evaluation)
        Session.commit()
        
        return redirect('/evaluations')
    
    return render_template('create_evaluation.html')

@app.route('/evaluation/edit/<int:id>', methods=['GET', 'POST'])
def edit_evaluation(id):
    evaluation = Session.query(Evaluation).get(id)
    
    if request.method == 'POST':
        evaluation.class_discipline_code = request.form['class_discipline']
        evaluation.class_number = request.form['class_number']
        evaluation.class_period = request.form['class_period']
        evaluation.description = request.form['description']
        evaluation.rating = request.form['rating']
        evaluation.user_id = request.form['user_id']
        
        Session.commit()
        
        return redirect('/evaluations')
    
    return render_template('edit_evaluation.html', evaluation=evaluation)

@app.route('/evaluation/delete/<int:id>')
def delete_evaluation(id):
    evaluation = Session.query(Evaluation).get(id)
    Session.delete(evaluation)
    Session.commit()
    return redirect('/evaluations')

"""
CRUD REPORT
"""

@app.route('/reports')
def reports():
    reports = Session.query(Report).all()
    return render_template('reports.html', reports=reports)

@app.route('/report/create/<int:evaluation_id>', methods=['GET', 'POST'])
def create_report(evaluation_id):
    if request.method == 'POST':
        reason = request.form['reason']
        
        new_report = Report(evaluation_id=evaluation_id, reason=reason)
        Session.add(new_report)
        Session.commit()
        
        return redirect('/reports')
    
    return render_template('create_report.html', evaluation_id=evaluation_id)

@app.route('/report/edit/<int:id>', methods=['GET', 'POST'])
def edit_report(id):
    report = Session.query(Report).get(id)
    
    if request.method == 'POST':
        report.reason = request.form['reason']
        
        Session.commit()
        
        return redirect('/reports')
    
    return render_template('edit_report.html', report=report)

@app.route('/report/delete/<int:id>')
def delete_report(id):
    report = Session.query(Report).get(id)
    Session.delete(report)
    Session.commit()
    return redirect('/reports')

"""
LOGIN 
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        user = Session.query(User).filter_by(email=email, password=senha).first()
        
        if user:
            session['user_id'] = user.id
            return redirect('/')
        else:
            error_message = 'Credenciais inválidas. Por favor, tente novamente.'
            return render_template('login.html', error_message=error_message)
    
    return render_template('login.html')

"""
LOGOUT 
"""

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')