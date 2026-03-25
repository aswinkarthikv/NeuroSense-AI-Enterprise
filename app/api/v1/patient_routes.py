from flask import request, jsonify
from flask_login import login_required, current_user
from app.api.v1 import patients_bp
from app.models.user import PatientProfile

@patients_bp.route('/', methods=['GET'])
@login_required
def get_patients():
    if current_user.is_doctor:
        patients = current_user.doctor_patients.all()
    elif current_user.is_admin:
        patients = PatientProfile.query.all()
    else:
        return jsonify({'error': 'Unauthorized'}), 403
        
    result = [{
        'id': p.id,
        'name': f"{p.user.first_name} {p.user.last_name}",
        'email': p.user.email,
        'dob': p.date_of_birth.strftime('%Y-%m-%d'),
        'gender': p.gender,
        'baseline_risk': p.baseline_risk_score,
        'last_assessment': p.last_assessment_date.strftime('%Y-%m-%d') if p.last_assessment_date else 'Never',
    } for p in patients]
    
    return jsonify({'status': 'success', 'count': len(result), 'patients': result})

@patients_bp.route('/<patient_id>', methods=['GET'])
@login_required
def get_patient(patient_id):
    patient = PatientProfile.query.get_or_404(patient_id)
    
    if current_user.is_doctor and patient.assigned_doctor_id != current_user.id:
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized. Not assigned to this patient.'}), 403
            
    # Serialize detailed assessments
    assessments_data = []
    for ass in patient.assessments.order_by(PatientProfile.assessments.property.mapper.class_.session_date.desc()).all():
        assessments_data.append({
            'id': ass.id,
            'date': ass.session_date.strftime('%Y-%m-%d'),
            'composite_score': ass.composite_risk_score,
            'voice_score': ass.voice_risk_score,
            'handwriting_score': ass.handwriting_risk_score,
            'gait_score': ass.gait_risk_score,
            'status': ass.status
        })

    return jsonify({
        'status': 'success',
        'patient': {
            'id': patient.id,
            'name': f"{patient.user.first_name} {patient.user.last_name}",
            'medical_history': patient.medical_history,
            'baseline_risk': patient.baseline_risk_score,
        },
        'assessments': assessments_data
    })
