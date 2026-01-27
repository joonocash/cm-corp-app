from flask import Blueprint, render_template, request, jsonify, current_app
from app.business.services.webinar_service import WebinarService

# Create blueprint
main = Blueprint('main', __name__)


def get_webinar_service():
    """Get webinar service instance"""
    return WebinarService(current_app.config)


@main.route('/')
def index():
    """
    Homepage route
    Renders webinar signup page
    """
    service = get_webinar_service()
    webinar_config = service.get_webinar_config()

    return render_template(
        'index.html',
        webinar_date=webinar_config['date']
    )


@main.route('/api/signup', methods=['POST'])
def signup_api():
    """
    API endpoint for signup submission

    Currently not used by frontend (localStorage only)
    Available for future backend integration

    Expects JSON:
    {
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "consent": boolean
    }
    """
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()
    service = get_webinar_service()
    result = service.process_signup(data)

    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400
