import os
import sys
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash
from faker import Faker

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User, PatientProfile
from app.models.assessment import AssessmentSession, MediaFile, DiagnosticReport

fake = Faker()

def create_admin():
    print("Creating Admin User...")
    admin = User(
        email='admin@neurosense.com',
        password_hash=generate_password_hash('admin123'),
        role='admin',
        first_name='System',
        last_name='Administrator'
    )
    db.session.add(admin)
    return admin

def create_doctors(num_doctors=50):
    print(f"Creating {num_doctors} Doctors...")
    doctors = []
    # Create a specific doctor for easy login testing
    master_doc = User(
        email='doctor@neurosense.com',
        password_hash=generate_password_hash('doctor123'),
        role='doctor',
        first_name='Gregory',
        last_name='House'
    )
    db.session.add(master_doc)
    doctors.append(master_doc)
    
    for _ in range(num_doctors - 1):
        doc = User(
            email=fake.unique.company_email(),
            password_hash=generate_password_hash('password123'),
            role='doctor',
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        db.session.add(doc)
        doctors.append(doc)
        
    db.session.commit()
    return doctors

def create_patients(doctors, num_patients=500):
    print(f"Creating {num_patients} Patients...")
    patients = []
    
    for _ in range(num_patients):
        # Create User Auth
        user = User(
            email=fake.unique.email(),
            password_hash=generate_password_hash('patient123'),
            role='patient',
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        db.session.add(user)
        db.session.flush() # Get user ID
        
        # Create Profile
        assigned_doc = random.choice(doctors)
        dob = fake.date_of_birth(minimum_age=40, maximum_age=90)
        
        profile = PatientProfile(
            user_id=user.id,
            assigned_doctor_id=assigned_doc.id,
            date_of_birth=dob,
            gender=random.choice(['Male', 'Female', 'Other']),
            medical_history=fake.text(max_nb_chars=200),
            baseline_risk_score=round(random.uniform(5.0, 85.0), 2)
        )
        db.session.add(profile)
        patients.append(profile)
        
    db.session.commit()
    return patients

def create_assessments(patients, num_per_patient=3):
    print(f"Creating Assessments for Patients (Max {num_per_patient} per patient)...")
    total_assessments = 0
    
    for patient in patients:
        num_sessions = random.randint(0, num_per_patient)
        
        # Simulate temporal degradation or improvement
        current_risk = patient.baseline_risk_score
        current_date = datetime.utcnow() - timedelta(days=num_sessions * 30)
        
        for i in range(num_sessions):
            assessment = AssessmentSession(
                patient_id=patient.id,
                session_date=current_date,
                status='completed',
                voice_risk_score=min(100.0, current_risk + random.uniform(-10, 15)),
                handwriting_risk_score=min(100.0, current_risk + random.uniform(-5, 20)),
                gait_risk_score=min(100.0, current_risk + random.uniform(-15, 25)),
            )
            
            assessment.composite_risk_score = (
                assessment.voice_risk_score * 0.3 + 
                assessment.handwriting_risk_score * 0.3 + 
                assessment.gait_risk_score * 0.4
            )
            
            assessment.doctor_notes = fake.sentence() if random.random() > 0.5 else None
            if assessment.doctor_notes:
                assessment.reviewed_at = current_date + timedelta(days=1)
                
            db.session.add(assessment)
            db.session.flush()
            
            # Create Mock Media Files
            create_media_files(assessment.id, patient.user_id, current_date)
            
            total_assessments += 1
            
            # Age the date and potentially worsen risk for next session
            current_date += timedelta(days=30)
            if random.random() > 0.3: # 70% chance of getting worse
                current_risk = min(95.0, current_risk + random.uniform(2, 8))
                
        # Update patient last assessment
        if num_sessions > 0:
            patient.last_assessment_date = current_date - timedelta(days=30)
            
    db.session.commit()
    print(f"Created {total_assessments} Total Assessments!")

def create_media_files(assessment_id, user_id, date):
    # Mocking actual file paths for display purposes
    modalities = ['voice', 'handwriting', 'gait']
    extensions = {'voice': '.wav', 'handwriting': '.png', 'gait': '.mp4'}
    mimes = {'voice': 'audio/wav', 'handwriting': 'image/png', 'gait': 'video/mp4'}
    
    for mod in modalities:
        if random.random() > 0.1: # 90% chance modality was completed
            media = MediaFile(
                assessment_id=assessment_id,
                modality_type=mod,
                file_path=f"/storage/{mod}/{user_id}_{date.strftime('%Y%m%d')}{extensions[mod]}",
                file_name=f"test_{mod}{extensions[mod]}",
                mime_type=mimes[mod],
                file_size_bytes=random.randint(1024, 15000000), # 1KB to 15MB
                uploaded_at=date
            )
            db.session.add(media)

def seed_database():
    app = create_app()
    with app.app_context():
        print("Dropping all existing tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        admin = create_admin()
        doctors = create_doctors(50)
        patients = create_patients(doctors, 500)
        create_assessments(patients, 5)
        
        print("✅ Enterprise Data Seeding Complete!")
        print("--------------------------------------------------")
        print("Doctor Login: doctor@neurosense.com / doctor123")
        print("Admin Login: admin@neurosense.com / admin123")
        print("--------------------------------------------------")

if __name__ == '__main__':
    seed_database()
