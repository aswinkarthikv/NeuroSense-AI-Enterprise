from flask import render_template, send_file, request, abort
from flask_login import login_required, current_user
from app.views import dashboard_bp
from app.models.user import PatientProfile
from app.models.assessment import AssessmentSession
import io
from app.services.pdf_generator import generate_assessment_report

@dashboard_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_doctor or current_user.is_admin:
            return render_template('dashboards/doctor_home.html')
    return render_template('auth/login.html')

@dashboard_bp.route('/patients/new', methods=['GET', 'POST'])
@login_required
def register_patient():
    if request.method == 'POST':
        # In a real app we'd save it to the DB. For this premium demo, we'll mock success.
        return render_template('patients/register.html', success=True)
    return render_template('patients/register.html', success=False)

@dashboard_bp.route('/patients')
@login_required
def patients_list():
    if current_user.is_doctor:
        patients = PatientProfile.query.filter_by(assigned_doctor_id=current_user.id).all()
    else:
        patients = PatientProfile.query.all()
    return render_template('patients/patient_list.html', patients=patients)

@dashboard_bp.route('/patients/<patient_id>')
@login_required
def patient_profile(patient_id):
    patient = PatientProfile.query.get_or_404(patient_id)
    return render_template('patients/patient_profile.html', patient=patient)

@dashboard_bp.route('/assessments/new')
@login_required
def new_assessment():
    return render_template('assessments/wizard.html')

@dashboard_bp.route('/reports')
@login_required
def clinical_reports():
    if current_user.is_doctor:
        # Get assessments only for patients assigned to this doctor
        assessments = AssessmentSession.query.join(PatientProfile).filter(PatientProfile.assigned_doctor_id == current_user.id).order_by(AssessmentSession.session_date.desc()).all()
    else:
        assessments = AssessmentSession.query.order_by(AssessmentSession.session_date.desc()).all()
        
    return render_template('patients/report_list.html', assessments=assessments)

@dashboard_bp.route('/assessments/<assessment_id>/pdf')
@login_required
def download_assessment_pdf(assessment_id):
    assessment = AssessmentSession.query.get_or_404(assessment_id)
    
    # Simple permissions check
    if current_user.is_patient and assessment.patient_id != current_user.patient_profile.id:
        abort(403)
        
    pdf_bytes = generate_assessment_report(assessment)
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'NeuroSense_Report_{assessment.id[:8]}.pdf'
    )
