from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app

# Create blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_index'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if username == current_app.config['ADMIN_USERNAME'] and password == current_app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.admin_index'))
        else:
            error = 'Invalid username or password.'

    return render_template('admin_login.html', error=error)


@admin.route('/logout')
def logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('main.index'))


@admin.route('/')
@login_required
def admin_index():
    """
    Admin page route
    Displays webinar signups from localStorage
    """
    return render_template('admin.html')
