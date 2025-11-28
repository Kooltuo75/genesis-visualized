"""
Authentication Module for Genesis Visualized
=============================================
Handles user accounts, login, sessions, and authorization.
"""

import json
import hashlib
import secrets
import os
from pathlib import Path
from datetime import datetime, timedelta

USERS_FILE = "users.json"
SESSIONS = {}  # In-memory session store (token -> user_info)
SESSION_DURATION = timedelta(hours=24)

def load_users():
    """Load users from JSON file."""
    if not Path(USERS_FILE).exists():
        # Create default admin user on first run
        default_users = {
            "users": [
                {
                    "username": "admin",
                    "password_hash": hash_password("admin123"),
                    "role": "admin",
                    "created": datetime.now().isoformat()
                }
            ]
        }
        save_users(default_users)
        print("Created default admin user (username: admin, password: admin123)")
        return default_users

    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(data):
    """Save users to JSON file."""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def hash_password(password):
    """Hash a password using SHA-256 with salt."""
    # Use a simple but secure hash (for production, use bcrypt)
    salt = "genesis_visualized_2024"
    salted = f"{salt}{password}{salt}"
    return hashlib.sha256(salted.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify a password against its hash."""
    return hash_password(password) == password_hash

def create_user(username, password, role="editor"):
    """Create a new user account."""
    data = load_users()

    # Check if username already exists
    for user in data['users']:
        if user['username'].lower() == username.lower():
            return {"success": False, "error": "Username already exists"}

    # Create new user
    new_user = {
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "created": datetime.now().isoformat()
    }

    data['users'].append(new_user)
    save_users(data)

    return {"success": True, "message": f"User '{username}' created successfully"}

def login(username, password):
    """Authenticate a user and create a session."""
    data = load_users()

    for user in data['users']:
        if user['username'].lower() == username.lower():
            if verify_password(password, user['password_hash']):
                # Create session token
                token = secrets.token_urlsafe(32)
                SESSIONS[token] = {
                    "username": user['username'],
                    "role": user['role'],
                    "expires": datetime.now() + SESSION_DURATION
                }
                return {
                    "success": True,
                    "token": token,
                    "username": user['username'],
                    "role": user['role']
                }
            else:
                return {"success": False, "error": "Invalid password"}

    return {"success": False, "error": "User not found"}

def logout(token):
    """End a user session."""
    if token in SESSIONS:
        del SESSIONS[token]
        return {"success": True}
    return {"success": False, "error": "Session not found"}

def verify_session(token):
    """Verify a session token is valid."""
    if not token:
        return None

    session = SESSIONS.get(token)
    if not session:
        return None

    # Check if session expired
    if datetime.now() > session['expires']:
        del SESSIONS[token]
        return None

    return session

def get_all_users():
    """Get list of all users (without password hashes)."""
    data = load_users()
    return [{
        "username": u['username'],
        "role": u['role'],
        "created": u.get('created', 'Unknown')
    } for u in data['users']]

def delete_user(username, admin_token):
    """Delete a user (admin only)."""
    session = verify_session(admin_token)
    if not session or session['role'] != 'admin':
        return {"success": False, "error": "Admin access required"}

    data = load_users()

    # Don't allow deleting yourself
    if session['username'].lower() == username.lower():
        return {"success": False, "error": "Cannot delete your own account"}

    # Find and remove user
    for i, user in enumerate(data['users']):
        if user['username'].lower() == username.lower():
            del data['users'][i]
            save_users(data)
            return {"success": True, "message": f"User '{username}' deleted"}

    return {"success": False, "error": "User not found"}

def change_password(username, old_password, new_password):
    """Change a user's password."""
    data = load_users()

    for user in data['users']:
        if user['username'].lower() == username.lower():
            if verify_password(old_password, user['password_hash']):
                user['password_hash'] = hash_password(new_password)
                save_users(data)
                return {"success": True, "message": "Password changed successfully"}
            else:
                return {"success": False, "error": "Current password is incorrect"}

    return {"success": False, "error": "User not found"}

def require_auth(handler_func):
    """Decorator to require authentication for an endpoint."""
    def wrapper(self, *args, **kwargs):
        # Get token from header or cookie
        token = self.headers.get('Authorization', '').replace('Bearer ', '')

        session = verify_session(token)
        if not session:
            self.send_json({"error": "Authentication required"}, 401)
            return None

        # Add session info to request
        self.session = session
        return handler_func(self, *args, **kwargs)

    return wrapper
