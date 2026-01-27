from flask import Blueprint, render_template

# Create blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def admin_index():
    """
    Admin page route
    Displays webinar signups from localStorage
    """
    return render_template('admin.html')
