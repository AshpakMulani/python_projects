from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    taskno = db.Column(db.Integer, primary_key=True)
    tasktitle = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.taskno} - {self.tasktitle}"

@app.route('/', methods=['GET', 'POST'])
def todo_main():
    if request.method=='POST':
        tasktitle = request.form['tasktitle']
        desc = request.form['desc']
        todo = Todo(tasktitle=tasktitle, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:taskno>', methods=['GET', 'POST'])
def update(taskno):
    if request.method=='POST':
        tasktitle = request.form['tasktitle']
        desc = request.form['desc']
        todo = Todo.query.filter_by(taskno=taskno).first()
        todo.tasktitle = tasktitle
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(taskno=taskno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:taskno>')
def delete(taskno):
    todo = Todo.query.filter_by(taskno=taskno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)