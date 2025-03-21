from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Mesocycle, WorkoutType, Athlete
from datetime import datetime

coach_bp = Blueprint('coach', __name__, template_folder='templates')

@coach_bp.route('/')
def dashboard():
    mesocycles = Mesocycle.query.all()
    workout_types = WorkoutType.query.all()
    athletes = Athlete.query.all()
    return render_template('dashboard.html', 
                           mesocycles=mesocycles, 
                           workout_types=workout_types,
                           athletes=athletes)

@coach_bp.route('/mesocycle/create', methods=['GET', 'POST'])
def create_mesocycle():
    if request.method == 'POST':
        name = request.form['name']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        mesocycle = Mesocycle(name=name, start_date=start_date, end_date=end_date)
        db.session.add(mesocycle)
        db.session.commit()
        return redirect(url_for('coach.dashboard'))
    return render_template('create_mesocycle.html')

@coach_bp.route('/workout-type/create', methods=['GET', 'POST'])
def create_workout_type():
    mesocycles = Mesocycle.query.all()
    if request.method == 'POST':
        name = request.form['name']
        mesocycle_id = request.form['mesocycle_id']
        repetitions_planned = request.form['repetitions_planned']
        distance_planned = request.form.get('distance_planned')
        time_planned_seconds = request.form.get('time_planned_seconds')

        workout_type = WorkoutType(
            name=name,
            mesocycle_id=mesocycle_id,
            repetitions_planned=repetitions_planned,
            distance_planned=distance_planned or None,
            time_planned_seconds=time_planned_seconds or None
        )
        db.session.add(workout_type)
        db.session.commit()
        return redirect(url_for('coach.dashboard'))
    return render_template('create_workout_type.html', mesocycles=mesocycles)

@coach_bp.route('/athlete/create', methods=['GET', 'POST'])
def create_athlete():
    if request.method == 'POST':
        name = request.form['name']
        year_of_birth = int(request.form['year_of_birth'])

        athlete = Athlete(name=name, year_of_birth=year_of_birth)
        db.session.add(athlete)
        db.session.commit()
        return redirect(url_for('coach.dashboard'))

    return render_template('create_athlete.html')

from .models import WorkoutSession

@coach_bp.route('/workout-session/create', methods=['GET', 'POST'])
def create_workout_session():
    athletes = Athlete.query.all()
    workout_types = WorkoutType.query.all()

    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        athlete_id = request.form['athlete_id']
        workout_type_id = request.form['workout_type_id']
        load_percentage = float(request.form['load_percentage'])
        repetitions_completed = request.form.get('repetitions_completed')
        distance_completed = request.form.get('distance_completed')
        time_elapsed_seconds = request.form.get('time_elapsed_seconds')
        pace = request.form.get('pace')
        average_splits = request.form.get('average_splits')
        note = request.form.get('note')

        # Convert optional fields to appropriate types or None
        repetitions_completed = int(repetitions_completed) if repetitions_completed else None
        distance_completed = int(distance_completed) if distance_completed else None
        time_elapsed_seconds = float(time_elapsed_seconds) if time_elapsed_seconds else None
        average_splits = float(average_splits) if average_splits else None

        pace_seconds = None
        if pace:
            minutes, seconds = map(float, pace.split(':'))
            pace_seconds = minutes * 60 + seconds

        workout_session = WorkoutSession(
            date=date,
            athlete_id=athlete_id,
            workout_type_id=workout_type_id,
            load_percentage=load_percentage,
            repetitions_completed=repetitions_completed,
            distance_completed=distance_completed,
            time_elapsed_seconds=time_elapsed_seconds,
            pace_seconds=pace_seconds,
            average_splits=average_splits,
            note=note
        )

        if pace_seconds:
            workout_session.calculate_watt()

        db.session.add(workout_session)
        db.session.commit()
        return redirect(url_for('coach.dashboard'))

    return render_template('create_workout_session.html', athletes=athletes, workout_types=workout_types)


