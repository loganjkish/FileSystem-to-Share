# Imports for WebDAV server and middleware
from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.fs_dav_provider import FilesystemProvider
from wsgidav.mw.base_mw import BaseMiddleware
from wsgidav.request_resolver import RequestResolver
from wsgidav.error_printer import ErrorPrinter
from wsgidav.http_authenticator import HTTPAuthenticator
from wsgidav.mw.cors import Cors
from wsgidav.dir_browser import WsgiDavDirBrowser

# Import for combining Flask and WsgiDAV apps
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Standard library imports
import os
import sys
import json

# Import for serving the combined app
from waitress import serve

# Flask imports
from flask import Flask, send_from_directory, request

# Function to determine the correct directory for config.json
def check_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))
# Load configuration
with open(os.path.join(check_directory(), "config.json"), "r") as f:
    config = json.load(f)

# Custom middleware to restrict folder write access based on username
class FolderWriteRestriction(BaseMiddleware):  
    def __call__(self, environ, start_response):
        method = environ.get("REQUEST_METHOD", "")
        path = environ.get("PATH_INFO", "").strip("/")
        username = environ.get("wsgidav.auth.user_name")
        print(f"User: {username}, Method: {method}, Path: {path}")

        if method in ("PUT", "DELETE", "MKCOL", "MOVE", "COPY"):
            normalized_path = path.lstrip("/")
            parts = normalized_path.split("/", 1)
            top_folder = parts[0] if parts else ""

            if top_folder != username and top_folder != "public":
                start_response("403 Forbidden", [("Content-Type", "text/plain"), ("Content-Length", "43")])
                return [b"Forbidden: you dont have write access here."]

        return self.next_app(environ, start_response)

# Create folders if they don't exist
os.makedirs("./fsts", exist_ok=True)
os.makedirs("./fsts/public", exist_ok=True)
for user in config["USERS"]:
    os.makedirs(os.path.join("./fsts", user), exist_ok=True)

# WebDAV server configuration
davConfig = {
    "host": config["HOST"],
    "port": config["PORT"],
    "provider_mapping": {
        "/": FilesystemProvider("./fsts")
    },
    "simple_dc": {
        "user_mapping": {
            "*": {u: {"password": p} for u, p in config["USERS"].items()}
        }
    },
    "http_authenticator": {
        "domain_controller": "wsgidav.dc.simple_dc.SimpleDomainController",
        "accept_basic": True,
        "accept_digest": False,
        "default_to_digest": False
    },
    "cors": {
        "enable": True,
        "allow_origin": [f"http://{config['HOSTNAME']}:{config['PORT']}"],
    },
    "dir_browser": { "enable": True },
    "middleware_stack": [
        Cors,
        ErrorPrinter,
        HTTPAuthenticator,
        WsgiDavDirBrowser,
        FolderWriteRestriction,
        RequestResolver
    ],
    "verbose": 1,
}
davapp = WsgiDAVApp(davConfig)

# Flask app for serving setup pages and scripts
app = Flask(__name__, static_folder="static")
@app.route("/")
def setup_page():
    # Detect user OS from User-Agent header
    ua = (request.headers.get("User-Agent") or "windows").lower()
    if "windows" in ua:
        return send_from_directory(app.static_folder, "setup_windows.html")
    elif "linux" in ua or "macintosh" in ua:
        return send_from_directory(app.static_folder, "setup_unix.html")
    return send_from_directory(app.static_folder, "setup_windows.html")
@app.route("/setup_download")
def setup_download():
    # Check what OS the client is using and serve right script
    args = request.args.to_dict()
    client_os = args.get("os")
    if client_os == "windows":
        # Get drive letter
        drive_letter = args.get("drive_letter")
        with open("fsts-setupFiles/windows.bat", "r") as f:
            script_content = f.read()
        # Replace placeholders in script
        script_content = script_content.replace("<DriveLetter>", drive_letter)
        script_content = script_content.replace("<WebDAV-Server-URL>", f"http://{config['HOSTNAME']}:{config['PORT']}/dav")
        return script_content, 200, {
            "Content-Type": "application/octet-stream",
            "Content-Disposition": f'attachment; filename="setup_{client_os}.bat"'
        }
    elif client_os == "linux" or client_os == "mac":
        # Get mount point
        mount_point = args.get("mount_point")
        if not mount_point.startswith("/"):
            mount_point = "/" + mount_point
        # Check if on Linux or Mac
        if client_os == "linux":
            with open("fsts-setupFiles/linux.sh", "r") as f:
                script_content = f.read()
        else:
            with open("fsts-setupFiles/mac.sh", "r") as f:
                script_content = f.read()
        # Replace placeholders in script
        script_content = script_content.replace("<MOUNT_POINT>", mount_point)
        script_content = script_content.replace("<WebDAV-Server-URL>", f"http://{config['HOSTNAME']}:{config['PORT']}/dav")
        return script_content, 200, {
            "Content-Type": "application/octet-stream",
            "Content-Disposition": f'attachment; filename="setup_{client_os}.sh"'
        }

    return "Please use the UI to get the setup script.", 400

# Combine Flask and WsgiDAV apps and serve
combined_app = DispatcherMiddleware(app.wsgi_app, {"/dav": davapp})
if __name__ == "__main__":
    serve(combined_app, host=config["HOST"], port=config["PORT"])