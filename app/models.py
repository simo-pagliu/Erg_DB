from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year_of_birth = db.Column(db.Integer, nullable=False)
    workout_sessions = relationship('WorkoutSession', backref='athlete', lazy=True)

class Mesocycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    workout_types = relationship('WorkoutType', backref='mesocycle', lazy=True)

class WorkoutType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mesocycle_id = db.Column(db.Integer, ForeignKey('mesocycle.id'), nullable=False)
    repetitions_planned = db.Column(db.Integer, nullable=False)
    distance_planned = db.Column(db.Integer, nullable=True)  # Nullable if not applicable
    time_planned_seconds = db.Column(db.Float, nullable=True)  # Nullable if not applicable
    workout_sessions = relationship('WorkoutSession', backref='workout_type', lazy=True)

class WorkoutSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    athlete_id = db.Column(db.Integer, ForeignKey('athlete.id'), nullable=False)
    workout_type_id = db.Column(db.Integer, ForeignKey('workout_type.id'), nullable=False)
    load_percentage = db.Column(db.Float, nullable=False)
    repetitions_completed = db.Column(db.Integer, nullable=True)
    distance_completed = db.Column(db.Integer, nullable=True)  # Nullable if not applicable
    time_elapsed_seconds = db.Column(db.Float, nullable=True)  # Nullable if not applicable
    pace_seconds = db.Column(db.Float, nullable=True)           # Nullable if not applicable
    watt = db.Column(db.Float, nullable=True)
    average_splits = db.Column(db.Float, nullable=True)
    note = db.Column(db.Text, nullable=True)

    def calculate_watt(self):
        if self.pace_seconds is not None:
            # Calculate watt using the formula W = 2.8 / (pace^3)
            self.watt = 2.8 / (self.pace_seconds ** 3)
