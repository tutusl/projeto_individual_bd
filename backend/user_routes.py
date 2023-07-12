""" from flask import render_template, request, redirect
from app import app, db
from models import User, Department

@app.route('/')
def index():
    #users = User.query.all()
    #return render_template('index.html', users=users)
    results = db.session.query(Department).all()
    for r in results:
        print(r.name)
    return ''

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        matricula = request.form['matricula']
        curso = request.form['curso']
        
        new_user = User(nome=nome, email=email, senha=senha, matricula=matricula, curso=curso)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.get(id)
    
    if request.method == 'POST':
        user.nome = request.form['nome']
        user.email = request.form['email']
        user.senha = request.form['senha']
        user.matricula = request.form['matricula']
        user.curso = request.form['curso']
        
        db.session.commit()
        return redirect('/')
    
    return render_template('edit.html', user=user)

@app.route('/delete/<int:id>')
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/') """