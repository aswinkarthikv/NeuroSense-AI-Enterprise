from flask import Blueprint

dashboard_bp = Blueprint('dashboards', __name__)

from app.views import dashboards
