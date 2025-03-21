from flask import Blueprint, request, jsonify
from . import db
from .models import WorkoutSession, Athlete, Mesocycle, WorkoutType
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/workout-sessions', methods=['POST'])
def add_workout_session():
    data = request.get_json()

    pace_seconds = None
    if 'pace' in data and data['pace']:
        minutes, seconds = map(float, data['pace'].split(':'))
        pace_seconds = minutes * 60 + seconds

    new_workout_session = WorkoutSession(
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        athlete_id=data['athlete_id'],
        workout_type_id=data['workout_type_id'],
        load_percentage=data['load_percentage'],
        repetitions_completed=data.get('repetitions_completed'),
        distance_completed=data.get('distance_completed'),
        time_elapsed_seconds=data.get('time_elapsed_seconds'),
        pace_seconds=pace_seconds,
        average_splits=data.get('average_splits'),
        note=data.get('note')
    )

    if pace_seconds is not None:
        new_workout_session.calculate_watt()

    db.session.add(new_workout_session)
    db.session.commit()

    return jsonify({'message': 'Workout session added successfully!'}), 201

@api_bp.route('/athletes', methods=['POST'])
def add_athlete():
    data = request.get_json()
    new_athlete = Athlete(
        name=data['name'],
        year_of_birth=data['year_of_birth']
    )
    db.session.add(new_athlete)
    db.session.commit()
    return jsonify({'message': 'Athlete added successfully!'}), 201

@api_bp.route('/athletes', methods=['GET'])
def get_athletes():
    athletes = Athlete.query.all()
    return jsonify([athlete.name for athlete in athletes]), 200

@api_bp.route('/mesocycles', methods=['POST'])
def add_mesocycle():
    data = request.get_json()
    new_mesocycle = Mesocycle(
        name=data['name'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    )
    db.session.add(new_mesocycle)
    db.session.commit()
    return jsonify({'message': 'Mesocycle added successfully!'}), 201

@api_bp.route('/mesocycles', methods=['GET'])
def get_mesocycles():
    mesocycles = Mesocycle.query.all()
    return jsonify([mesocycle.name for mesocycle in mesocycles]), 200

@api_bp.route('/workout-types', methods=['POST'])
def add_workout_type():
    data = request.get_json()
    new_workout_type = WorkoutType(
        name=data['name'],
        mesocycle_id=data['mesocycle_id'],
        repetitions_planned=data['repetitions_planned'],
        distance_planned=data.get('distance_planned'),
        time_planned_seconds=data.get('time_planned_seconds')
    )
    db.session.add(new_workout_type)
    db.session.commit()
    return jsonify({'message': 'Workout type added successfully!'}), 201

@api_bp.route('/workout-types', methods=['GET'])
def get_workout_types():
    workout_types = WorkoutType.query.all()
    return jsonify([workout_type.name for workout_type in workout_types]), 200
