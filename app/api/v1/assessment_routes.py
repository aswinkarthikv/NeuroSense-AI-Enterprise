from flask import request, jsonify
from flask_login import login_required, current_user
from app.api.v1 import assessments_bp
from app.models.user import PatientProfile
from app.models.assessment import AssessmentSession, MediaFile
from app import db

@assessments_bp.route('/<patient_id>/start', methods=['POST'])
@login_required
def start_assessment(patient_id):
    patient = PatientProfile.query.get_or_404(patient_id)
    if current_user.is_doctor and patient.assigned_doctor_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    assessment = AssessmentSession(
        patient_id=patient.id,
        status='pending'
    )
    db.session.add(assessment)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Assessment started',
        'assessment_id': assessment.id
    })

@assessments_bp.route('/<assessment_id>/upload/<modality>', methods=['POST'])
@login_required
def upload_media(assessment_id, modality):
    if modality not in ['voice', 'handwriting', 'gait']:
        return jsonify({'error': 'Invalid modality'}), 400
        
    # In a full implementation, this reads the file, saves it to storage via storage_service,
    # and then adds it to the database. For now we mock the successful response.
    return jsonify({
        'status': 'success',
        'message': f'{modality.capitalize()} media uploaded and queued for processing.'
    })

@assessments_bp.route('/<assessment_id>/process', methods=['POST'])
@login_required
def process_assessment(assessment_id):
    assessment = AssessmentSession.query.get_or_404(assessment_id)
    
    # Normally this would trigger a Celery task that calls the AI Pipelines and fusion engine.
    # We will just mark it as processing for the mock API.
    assessment.status = 'processing'
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'AI Pipelines triggered. Awaiting fusion results.'
    })
