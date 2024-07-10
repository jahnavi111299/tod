from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jahnavi11:jahnavi@35.223.177.157/todo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SQLAlchemy model for Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.Date, default=datetime.utcnow().date)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def mark_as_finished(self):
        self.completed = True
        db.session.commit()

# Routes...

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    content = request.form['content']
    new_task = Task(content=content)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/finished/<int:task_id>', methods=['POST'])  # Ensure POST method is accepted
def mark_as_finished(task_id):
    task = Task.query.get(task_id)
    task.mark_as_finished()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])  # Ensure POST method is accepted
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)








