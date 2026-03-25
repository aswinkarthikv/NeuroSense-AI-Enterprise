import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(app):
    log_dir = os.path.join(app.root_path, '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure the global logger
    logging.basicConfig(level=logging.INFO)
    
    # File handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'neurosense_app.log'), 
        maxBytes=10240000, 
        backupCount=10
    )
    
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('NeuroSense AI Enterprise startup')
