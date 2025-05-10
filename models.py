from datetime import datetime
from app import db

class Registration(db.Model):
    """Model for waitlist registrations."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 can be up to 45 chars
    user_agent = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f"<Registration {self.email}>"

class Admin(db.Model):
    """Model for admin users."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def __repr__(self):
        return f"<Admin {self.username}>"

class Stats(db.Model):
    """Model for basic analytics."""
    id = db.Column(db.Integer, primary_key=True)
    page_views = db.Column(db.Integer, default=0)
    form_submissions = db.Column(db.Integer, default=0)
    form_errors = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Stats views:{self.page_views} submissions:{self.form_submissions}>"
