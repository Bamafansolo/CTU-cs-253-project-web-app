import logging
from flask import render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app import app, db
from models import Registration, Admin, Stats
import re

# Create or get the stats object
def get_stats():
    stats = Stats.query.first()
    if not stats:
        stats = Stats()
        db.session.add(stats)
        db.session.commit()
    return stats

# Increment page views
def increment_page_views():
    stats = get_stats()
    stats.page_views += 1
    db.session.commit()

# Email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Admin login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    increment_page_views()
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    try:
        # Get form data
        data = request.json
        email = data.get('email', '').strip().lower()
        full_name = data.get('fullName', '').strip()
        
        # Update stats
        stats = get_stats()
        
        # Validate data
        if not email or not full_name:
            stats.form_errors += 1
            db.session.commit()
            return jsonify({'success': False, 'message': 'Email and full name are required.'}), 400
        
        if not is_valid_email(email):
            stats.form_errors += 1
            db.session.commit()
            return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400
            
        if len(full_name) < 2:
            stats.form_errors += 1
            db.session.commit()
            return jsonify({'success': False, 'message': 'Please enter your full name.'}), 400
        
        # Check if email already exists
        existing_registration = Registration.query.filter_by(email=email).first()
        if existing_registration:
            return jsonify({'success': False, 'message': 'This email is already registered.'}), 400
        
        # Create new registration
        registration = Registration(
            email=email,
            full_name=full_name,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        
        # Save to database
        db.session.add(registration)
        stats.form_submissions += 1
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Thank you for joining our waitlist!'}), 200
        
    except Exception as e:
        logging.error(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while processing your request.'}), 500

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    registrations = Registration.query.order_by(Registration.timestamp.desc()).all()
    stats = get_stats()
    return render_template('admin.html', registrations=registrations, stats=stats)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('index'))

# Initialize admin user if not exists
# Create admin user on app initialization
# This will be called from app.py after db.create_all()
