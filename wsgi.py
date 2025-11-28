"""
WSGI Application for Render Deployment
=======================================
This module provides a production-ready WSGI interface.
"""

import json
import os
import mimetypes
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Initialize mimetypes
mimetypes.init()

# Import our modules
import auth

# Cloudinary setup (optional)
try:
    import cloudinary
    import cloudinary.uploader
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False

# Configuration
DATABASE_FILE = "frames-database.json"
IMAGES_DIR = Path("images")
STATIC_DIR = Path(__file__).parent

def load_env_var(var_name):
    """Load environment variable."""
    return os.environ.get(var_name)

def setup_cloudinary():
    """Configure Cloudinary if credentials are available."""
    if not CLOUDINARY_AVAILABLE:
        return False

    cloud_name = load_env_var('CLOUDINARY_CLOUD_NAME')
    api_key = load_env_var('CLOUDINARY_API_KEY')
    api_secret = load_env_var('CLOUDINARY_API_SECRET')
    use_cloudinary = load_env_var('USE_CLOUDINARY')

    if use_cloudinary != 'true':
        return False

    if not all([cloud_name, api_key, api_secret]):
        return False

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )
    print(f"Cloudinary configured: {cloud_name}")
    return True

USE_CLOUD_STORAGE = setup_cloudinary()

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def load_database():
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_database(data):
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_frame_by_id(frame_id):
    data = load_database()
    for frame in data['frames']:
        if frame['id'] == frame_id:
            return frame, data
    return None, data

# ============================================================================
# WSGI APPLICATION
# ============================================================================

def application(environ, start_response):
    """Main WSGI application."""
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    # Handle CORS preflight
    if method == 'OPTIONS':
        start_response('200 OK', [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
        ])
        return [b'']

    # API Routes
    if path.startswith('/api/'):
        return handle_api(environ, start_response, method, path)

    # Static files
    return serve_static(environ, start_response, path)

def handle_api(environ, start_response, method, path):
    """Handle API requests."""

    def json_response(data, status='200 OK'):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        start_response(status, [
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
        ])
        return [body]

    # Get auth token from headers
    auth_header = environ.get('HTTP_AUTHORIZATION', '')
    token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else ''

    # GET requests
    if method == 'GET':
        # Auth: Get current user
        if path == '/api/auth/me':
            session = auth.verify_session(token)
            if session:
                return json_response({
                    "authenticated": True,
                    "username": session['username'],
                    "role": session['role']
                })
            return json_response({"authenticated": False}, '401 Unauthorized')

        # Auth: Get all users (admin only)
        if path == '/api/auth/users':
            session = auth.verify_session(token)
            if session and session['role'] == 'admin':
                return json_response({"users": auth.get_all_users()})
            return json_response({"error": "Admin access required"}, '403 Forbidden')

        # Frame: Get frame data
        if path.startswith('/api/frame/') and '/versions' not in path:
            try:
                frame_id = int(path.split('/')[-1])
                frame, _ = get_frame_by_id(frame_id)
                if frame:
                    viz = frame.get('visualization', {})
                    return json_response({
                        "id": frame['id'],
                        "reference": frame['reference'],
                        "text": frame['text'],
                        "title": viz.get('title', ''),
                        "asciiArt": viz.get('asciiArt', ''),
                        "imagePrompt": viz.get('imagePrompt', ''),
                        "imagePath": viz.get('imagePath'),
                        "currentVersion": frame.get('currentVersion', 1)
                    })
                return json_response({"error": "Frame not found"}, '404 Not Found')
            except:
                return json_response({"error": "Invalid frame ID"}, '400 Bad Request')

        # Frame: Get version history
        if '/versions' in path:
            try:
                frame_id = int(path.split('/')[3])
                frame, _ = get_frame_by_id(frame_id)
                if frame:
                    versions = []
                    for v in frame.get('versionHistory', []):
                        versions.append({
                            'version': v['version'],
                            'timestamp': v['timestamp'],
                            'title': v.get('title', ''),
                            'hasImage': bool(v.get('imagePath')),
                            'imagePath': v.get('imagePath'),
                            'asciiArt': v.get('asciiArt', ''),
                            'isCurrent': False
                        })
                    viz = frame.get('visualization', {})
                    versions.append({
                        'version': frame.get('currentVersion', 1),
                        'timestamp': frame.get('timestamp', ''),
                        'title': viz.get('title', ''),
                        'hasImage': bool(viz.get('imagePath')),
                        'imagePath': viz.get('imagePath'),
                        'asciiArt': viz.get('asciiArt', ''),
                        'isCurrent': True
                    })
                    versions.sort(key=lambda x: x['version'])
                    return json_response({
                        "frameId": frame['id'],
                        "reference": frame['reference'],
                        "versions": versions
                    })
                return json_response({"error": "Frame not found"}, '404 Not Found')
            except Exception as e:
                return json_response({"error": str(e)}, '400 Bad Request')

    # POST requests
    if method == 'POST':
        # Read request body
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length).decode('utf-8')
            post_data = json.loads(body) if body else {}
        except:
            post_data = {}

        # Auth: Login
        if path == '/api/auth/login':
            username = post_data.get('username', '')
            password = post_data.get('password', '')
            if not username or not password:
                return json_response({"error": "Username and password required"}, '400 Bad Request')
            result = auth.login(username, password)
            status = '200 OK' if result['success'] else '401 Unauthorized'
            return json_response(result, status)

        # Auth: Logout
        if path == '/api/auth/logout':
            result = auth.logout(token)
            return json_response(result)

        # Auth: Register (admin only)
        if path == '/api/auth/register':
            session = auth.verify_session(token)
            if not session or session['role'] != 'admin':
                return json_response({"error": "Admin access required"}, '403 Forbidden')

            username = post_data.get('username', '')
            password = post_data.get('password', '')
            role = post_data.get('role', 'editor')

            if not username or not password:
                return json_response({"error": "Username and password required"}, '400 Bad Request')

            result = auth.create_user(username, password, role)
            status = '200 OK' if result['success'] else '400 Bad Request'
            return json_response(result, status)

        # Auth: Delete user (admin only)
        if path == '/api/auth/delete':
            username = post_data.get('username', '')
            result = auth.delete_user(username, token)
            status = '200 OK' if result['success'] else '403 Forbidden'
            return json_response(result, status)

        # Frame editing endpoints would go here
        # (Simplified for deployment - full editing requires more setup)

    return json_response({"error": "Unknown endpoint"}, '404 Not Found')

def serve_static(environ, start_response, path):
    """Serve static files."""
    if path == '/':
        path = '/index.html'

    file_path = STATIC_DIR / path.lstrip('/')

    if file_path.is_file():
        content_type, _ = mimetypes.guess_type(str(file_path))
        if content_type is None:
            content_type = 'application/octet-stream'

        with open(file_path, 'rb') as f:
            content = f.read()

        start_response('200 OK', [
            ('Content-Type', content_type),
            ('Content-Length', str(len(content))),
        ])
        return [content]

    # 404
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'Not Found']

# For local testing
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting WSGI server on port {port}")
    server = make_server('', port, application)
    server.serve_forever()
