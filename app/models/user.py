from app import db
from datetime import datetime
from flask_login import UserMixin
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='patient') # admin, doctor, patient
    
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    patients = db.relationship('PatientProfile', backref='user', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='PatientProfile.user_id')
    doctor_patients = db.relationship('PatientProfile', backref='doctor', lazy='dynamic', foreign_keys='PatientProfile.assigned_doctor_id')
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
        
    @property
    def is_admin(self):
        return self.role == 'admin'
        
    @property
    def is_doctor(self):
        return self.role == 'doctor'
        
    @property
    def is_patient(self):
        return self.role == 'patient'
        
class PatientProfile(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    assigned_doctor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    medical_history = db.Column(db.Text, nullable=True) # JSON or Text
    
    # Metrics
    baseline_risk_score = db.Column(db.Float, nullable=True)
    last_assessment_date = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    assessments = db.relationship('AssessmentSession', backref='patient', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Patient {self.id}>'
