from app import db
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class AssessmentSession(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    patient_id = db.Column(db.String(36), db.ForeignKey('patients.id'), nullable=False, index=True)
    
    # Metadata
    session_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, processing, completed, failed
    
    # Pre-fusion Modality Scores (0.0 to 100.0)
    voice_risk_score = db.Column(db.Float, nullable=True)
    handwriting_risk_score = db.Column(db.Float, nullable=True)
    gait_risk_score = db.Column(db.Float, nullable=True)
    
    # Global AI Fusion Rating (0.0 to 100.0)
    composite_risk_score = db.Column(db.Float, nullable=True)
    
    # Clinical Review
    doctor_notes = db.Column(db.Text, nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    media_files = db.relationship('MediaFile', backref='session', lazy='dynamic', cascade='all, delete-orphan')
    report = db.relationship('DiagnosticReport', backref='session', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Assessment {self.id} for Patient {self.patient_id}>'

class MediaFile(db.Model):
    __tablename__ = 'media_files'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    assessment_id = db.Column(db.String(36), db.ForeignKey('assessments.id'), nullable=False, index=True)
    
    # Media classification
    modality_type = db.Column(db.String(20), nullable=False) # voice, handwriting, gait
    file_path = db.Column(db.String(512), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(50), nullable=False)
    file_size_bytes = db.Column(db.Integer, nullable=False)
    
    # AI specific raw feature JSON extracted during processing
    extracted_features_json = db.Column(db.Text, nullable=True) 

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Media {self.modality_type} for Assessment {self.assessment_id}>'

class DiagnosticReport(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    assessment_id = db.Column(db.String(36), db.ForeignKey('assessments.id'), nullable=False, unique=True)
    
    pdf_report_path = db.Column(db.String(512), nullable=True)
    summary_json = db.Column(db.Text, nullable=True) # Full inference details
    
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Report for Assessment {self.assessment_id}>'
