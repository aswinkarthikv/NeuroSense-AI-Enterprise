from flask import request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.api.v1 import auth_bp
from app.models.user import User

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({
            'status': 'success', 
            'message': 'Logged in successfully',
            'user': {'email': user.email, 'role': user.role, 'name': f"{user.first_name} {user.last_name}"}
        })
    return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success', 'message': 'Logged out successfully'})
