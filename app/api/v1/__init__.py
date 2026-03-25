from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
patients_bp = Blueprint('patients', __name__)
assessments_bp = Blueprint('assessments', __name__)

# Import the routes
from app.api.v1 import auth_routes, patient_routes, assessment_routes
