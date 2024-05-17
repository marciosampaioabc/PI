from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import ScheduleForm
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    db.init_app(app)

    return app

app = create_app()

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Numeric, nullable=False)
    data = db.Column(db.String(20), nullable=False)
    hora = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    schedules = Schedule.query.all()
    return render_template('index.html', schedules=schedules)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    form = ScheduleForm()
    if form.validate_on_submit():
        new_schedule = Schedule(
            nome=form.nome.data,
            valor=form.valor.data,
            data=form.data.data,
            hora=form.hora.data.strftime('%H:%M')
        )
        db.session.add(new_schedule)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('schedule.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)