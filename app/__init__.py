import os
from flask import Flask
from config.settings import Config
from config.logging_config import setup_logger

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Extension initialization
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize app specific configs (directories)
    config_class.init_app(app)
    
    # Setup Logging
    setup_logger(app)
    
    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # Register blueprints (To be implemented)
    from app.api.v1 import auth_bp, patients_bp, assessments_bp
    from app.views.dashboards import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(patients_bp, url_prefix='/api/v1/patients')
    app.register_blueprint(assessments_bp, url_prefix='/api/v1/assessments')
    app.register_blueprint(dashboard_bp)
    
    # Welcome route
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'system': 'NeuroSense Enterprise Application Running'}
        
    return app
