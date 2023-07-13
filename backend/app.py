from flask import Flask, render_template, request, redirect, session, jsonify
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

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    user_id = session.get('user_id')
    user = Session.query(User).get(user_id)
    if request.method == 'POST':
        user.name = request.form['nome']
        user.email = request.form['email']
        user.password = request.form['senha']
        user.registry = request.form['matricula']
        user.course = request.form['curso']
        
        Session.commit()
        return redirect('/home')
    
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
        if session.get('user_id'):
            user_id = session.get('user_id')
        else:
            return redirect('/login')
        if Session.query(User.role_id).filter(User.id == user_id)[0][0] == 1:
            return render_template('error.html', error_message='Não é permitido admins criarem avaliações.')
        class_discipline_name = request.form['class_discipline']
        class_number = request.form['class_number']
        class_period = request.form['class_period']
        description = request.form['description']
        rating = request.form['rating']
        
        new_evaluation = Evaluation(
            class_discipline_code=(Session.query(Discipline.discipline_code).where(Discipline.name == class_discipline_name)[0])[0],
            class_number=class_number,
            class_period=class_period,
            description=description,
            rating=int(rating),
            user_id=int(user_id)
        )
        
        Session.add(new_evaluation)
        Session.commit()
        
        return redirect('/home')
    
    return render_template('create_evaluation.html')

@app.route('/evaluation/edit/<int:id>', methods=['GET', 'POST'])
def edit_evaluation(id):
    evaluation = Session.query(Evaluation).get(id)

    if evaluation.user_id != session.get('user_id'):
        # If the logged-in user is not the owner of the evaluation, redirect them to an error page or handle it accordingly
        return render_template('error.html', error_message='Você não é autorizado a editar essa avaliação.')

    if request.method == 'POST':
        evaluation.class_discipline_code = request.form['class_discipline']
        evaluation.class_number = request.form['class_number']
        evaluation.class_period = request.form['class_period']
        evaluation.description = request.form['description']
        evaluation.rating = request.form['rating']
        evaluation.user_id = request.form['user_id']
        
        Session.commit()
        
        return redirect('/home')
    
    return render_template('edit_evaluation.html', evaluation=evaluation)

@app.route('/evaluation/delete/<int:id>')
def delete_evaluation(id):
    evaluation = Session.query(Evaluation).get(id)
    if evaluation.user_id != session.get('user_id'):
        if Session.query(User.role_id).filter(User.id == evaluation.user_id)[0][0] != 1:
            return render_template('error.html', error_message='Você não é autorizado a deletar essa avaliação.')
    Session.delete(evaluation)
    Session.commit()
    return redirect('/home')

"""
CRUD REPORT
"""

@app.route('/reports')
def reports():
    user_id = session.get('user_id')
    if Session.query(User.role_id).filter(User.id == user_id)[0][0] != 1:
            return render_template('error.html', error_message='Você não é autorizado a vizualizar ou deletar avaliações.')
    reports = Session.query(Report).all()
    return render_template('reports.html', reports=reports)

@app.route('/report/create/<int:evaluation_id>', methods=['GET', 'POST'])
def create_report(evaluation_id):
    user_id = session.get('user_id')
    if Session.query(User.role_id).filter(User.id == user_id)[0][0] == 1:
        return render_template('error.html', error_message='Admins não são autorizados a criar reports.')
    if request.method == 'POST':
        reason = request.form['reason']
        
        new_report = Report(evaluation_id=evaluation_id, reason=reason)
        Session.add(new_report)
        Session.commit()
        
        return redirect('/home')
    
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

    evaluation_id = Session.query(Evaluation.id).filter(Evaluation.id == report.evaluation_id)
    for report in Session.query(Report.id).filter(Report.evaluation_id == evaluation_id):
        Session.delete(Session.query(Report).get(report[0]))

    Session.delete(Session.query(Evaluation).get(evaluation_id[0][0]))
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
            return redirect('/home')
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

"""
HOME 
"""

@app.route('/home')
def home():
    if session.get('user_id'):
        evaluations = Session.query(Evaluation).all()
        return render_template('home.html', evaluations=evaluations)
    else:
        return redirect('/login')
    

"""
DEPENDENT DROPDOWN MENU
"""

@app.route('/get_periods/')
def get_periods():

    periods = Session.query(Lecture.period).distinct().all()
    periods_list = [period[0] for period in periods]
    return jsonify(periods_list)


@app.route('/get_disciplines/<selected_period>')
def get_disciplines(selected_period):

    discipline_names = Session.query(Discipline.name).join(Lecture, Discipline.discipline_code == Lecture.discipline_code).filter(Lecture.period == selected_period).distinct().all()
    discipline_names_list = [discipline_name[0] for discipline_name in discipline_names]
    return jsonify(discipline_names_list)

@app.route('/get_professors/<selected_period>/<selected_discipline>')
def get_professors(selected_period, selected_discipline):
    professors_names = Session.query(Lecture.professor_name).join(Discipline, Lecture.discipline_code == (Session.query(Discipline.discipline_code).where(Discipline.name == selected_discipline)[0])[0]).filter(Lecture.period == selected_period).distinct().all()
    professors_names_list = [professors_name[0] for professors_name in professors_names]
    return jsonify(professors_names_list)

@app.route('/get_professors/<selected_period>/<selected_discipline>/<selected_professor>')
def get_class_numbers(selected_period, selected_discipline, selected_professor):
    class_numbers = Session.query(Lecture.class_number).join(Discipline, Lecture.discipline_code == (Session.query(Discipline.discipline_code).where(Discipline.name == selected_discipline)[0])[0]).filter(Lecture.period == selected_period).filter(Lecture.professor_name == selected_professor).distinct().all()
    class_numbers_list = [class_number[0] for class_number in class_numbers]
    return jsonify(class_numbers_list)