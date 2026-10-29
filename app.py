"""
All-in-One Government Complaint Management System
Full-Featured Web Server using Python Standard Library (Zero External Dependencies)
"""
import os
import sys
import json
import base64
import urllib.parse
import mimetypes
import traceback
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

import config
import database

# Ensure uploads directory exists
config.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
config.STATIC_FOLDER.mkdir(parents=True, exist_ok=True)

# Generate a sample placeholder attachment file for demo purposes
sample_doc_path = config.UPLOAD_FOLDER / "sample_document.txt"
if not sample_doc_path.exists():
    sample_doc_path.write_text("National Grievance Redressal Portal - Official Verified Evidence Document", encoding="utf-8")

# Session store for authenticated admin/officers (token -> user_dict)
ACTIVE_SESSIONS = {}

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in separate threads for concurrency and responsiveness."""
    daemon_threads = True

class ComplaintRequestHandler(BaseHTTPRequestHandler):
    """Comprehensive request handler for API endpoints and static web assets."""

    server_version = "NationalGovPortal/2.0"

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Credentials", "true")

    def _send_json(self, status_code: int, data: dict):
        """Send formatted JSON response."""
        try:
            body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status_code)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            traceback.print_exc()

    def _send_error(self, status_code: int, message: str):
        self._send_json(status_code, {"success": False, "error": message})

    def _read_json_body(self):
        """Read and parse JSON from request body."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        raw = self.rfile.read(content_length)
        return json.loads(raw.decode("utf-8"))

    def _get_auth_user(self):
        """Check Authorization header for session token."""
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            return ACTIVE_SESSIONS.get(token)
        return None

    def do_GET(self):
        """Handle GET requests for static pages, uploaded files, and REST API."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        # ------------------- REST API ENDPOINTS -------------------
        if path == "/api/meta":
            return self._send_json(200, {
                "success": True,
                "categories": config.CATEGORIES,
                "statuses": config.STATUSES,
                "departments": config.DEPARTMENTS
            })

        if path == "/api/stats":
            stats = database.get_dashboard_stats()
            return self._send_json(200, {"success": True, "stats": stats})

        if path == "/api/announcements":
            announcements = database.get_public_announcements()
            return self._send_json(200, {"success": True, "announcements": announcements})

        if path == "/api/complaints":
            filters = {}
            if "status" in query_params:
                filters["status"] = query_params["status"][0]
            if "category" in query_params:
                filters["category"] = query_params["category"][0]
            if "urgency" in query_params:
                filters["urgency"] = query_params["urgency"][0]
            if "department" in query_params:
                filters["department"] = query_params["department"][0]

            search = query_params.get("search", [""])[0]
            limit = int(query_params.get("limit", [50])[0])
            offset = int(query_params.get("offset", [0])[0])

            result = database.list_complaints(filters, search, limit, offset)
            return self._send_json(200, {"success": True, **result})

        if path.startswith("/api/complaints/"):
            complaint_id = path[len("/api/complaints/"):].strip()
            if complaint_id:
                complaint = database.get_complaint(complaint_id)
                if complaint:
                    return self._send_json(200, {"success": True, "complaint": complaint})
                return self._send_error(404, f"Complaint with ID '{complaint_id}' was not found in national registry.")

        if path == "/api/search-phone":
            phone = query_params.get("phone", [""])[0]
            if not phone:
                return self._send_error(400, "Missing required 'phone' parameter.")
            results = database.find_complaints_by_phone(phone)
            return self._send_json(200, {"success": True, "complaints": results})

        # ------------------- UPLOADED EVIDENCE SERVING -------------------
        if path.startswith("/uploads/"):
            filename = os.path.basename(path[len("/uploads/"):])
            filepath = config.UPLOAD_FOLDER / filename
            if filepath.exists() and filepath.is_file():
                return self._serve_file(filepath)
            # Fallback to sample text document
            if sample_doc_path.exists():
                return self._serve_file(sample_doc_path)
            return self._send_error(404, "Evidence file not found.")

        # ------------------- STATIC ASSET SERVING -------------------
        route_map = {
            "/": config.STATIC_FOLDER / "index.html",
            "/index": config.STATIC_FOLDER / "index.html",
            "/index.html": config.STATIC_FOLDER / "index.html",
            "/register": config.STATIC_FOLDER / "register.html",
            "/register.html": config.STATIC_FOLDER / "register.html",
            "/track": config.STATIC_FOLDER / "track.html",
            "/track.html": config.STATIC_FOLDER / "track.html",
            "/admin": config.STATIC_FOLDER / "admin.html",
            "/admin.html": config.STATIC_FOLDER / "admin.html",
            "/transparency": config.STATIC_FOLDER / "transparency.html",
            "/transparency.html": config.STATIC_FOLDER / "transparency.html",
        }

        if path in route_map:
            target_file = route_map[path]
            if target_file.exists():
                return self._serve_file(target_file)
            else:
                return self._send_error(404, f"Page {path} not configured.")

        # Subdirectory static files (e.g. /css/style.css, /js/app.js)
        clean_path = path.lstrip("/")
        candidate = config.STATIC_FOLDER / clean_path
        if candidate.exists() and candidate.is_file() and config.STATIC_FOLDER in candidate.resolve().parents:
            return self._serve_file(candidate)

        return self._send_error(404, "Resource not found on this portal.")

    def do_POST(self):
        """Handle POST requests for authentication and complaint processing."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # ------------------- OFFICER AUTHENTICATION -------------------
        if path == "/api/login":
            try:
                body = self._read_json_body()
                username = body.get("username", "").strip()
                password = body.get("password", "").strip()

                conn = database.get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                user_row = cursor.fetchone()
                conn.close()

                if not user_row or not database.verify_password(password, user_row["password_hash"]):
                    return self._send_error(401, "Invalid officer credentials. Please verify your username and password.")

                # Generate secure session token
                import secrets
                token = secrets.token_hex(24)
                user_info = {
                    "id": user_row["id"],
                    "username": user_row["username"],
                    "full_name": user_row["full_name"],
                    "role": user_row["role"],
                    "department": user_row["department"],
                    "badge_number": user_row["badge_number"],
                    "email": user_row["email"]
                }
                ACTIVE_SESSIONS[token] = user_info

                return self._send_json(200, {
                    "success": True,
                    "token": token,
                    "user": user_info,
                    "message": f"Welcome, {user_info['full_name']} ({user_info['role'].title()})"
                })
            except Exception as e:
                traceback.print_exc()
                return self._send_error(500, f"Authentication error: {str(e)}")

        # ------------------- COMPLAINT REGISTRATION -------------------
        if path == "/api/complaints":
            try:
                body = self._read_json_body()

                # Basic validation
                citizen_name = body.get("citizen_name", "").strip()
                citizen_phone = body.get("citizen_phone", "").strip()
                category = body.get("category", "").strip()
                subject = body.get("subject", "").strip()
                description = body.get("description", "").strip()

                if not citizen_name or not citizen_phone or not category or not subject or not description:
                    return self._send_error(400, "Please fill in all mandatory fields: Citizen Name, Phone, Category, Subject, and Description.")

                # Process optional file upload if base64 provided
                file_data = body.get("file_data")
                file_name = body.get("file_name")
                attachments = []

                if file_data and file_name:
                    try:
                        # Clean base64 header if present
                        if "," in file_data:
                            _, encoded = file_data.split(",", 1)
                        else:
                            encoded = file_data
                        
                        file_bytes = base64.b64decode(encoded)
                        safe_name = os.path.basename(file_name).replace(" ", "_")
                        timestamp_prefix = database.datetime.datetime.now().strftime("%Y%m%d%H%M%S_")
                        stored_filename = f"{timestamp_prefix}{safe_name}"
                        dest_path = config.UPLOAD_FOLDER / stored_filename

                        dest_path.write_bytes(file_bytes)
                        attachments.append({
                            "original_name": file_name,
                            "stored_filename": stored_filename,
                            "file_size": len(file_bytes)
                        })
                    except Exception as upload_err:
                        print(f"[WARN] Error saving file attachment: {upload_err}")

                body["attachments"] = attachments
                complaint_id = database.create_complaint(body)

                return self._send_json(201, {
                    "success": True,
                    "complaint_id": complaint_id,
                    "message": "Complaint registered successfully in the National Grievance Redressal System.",
                    "status": "Submitted"
                })
            except Exception as e:
                traceback.print_exc()
                return self._send_error(500, f"Error processing complaint: {str(e)}")

        # ------------------- UPDATE COMPLAINT STATUS -------------------
        if path.startswith("/api/complaints/") and path.endswith("/status"):
            try:
                parts = path.split("/")
                complaint_id = parts[3]
                body = self._read_json_body()

                new_status = body.get("status")
                remarks = body.get("remarks", "").strip()
                officer_name = body.get("officer_name", "Authorized Officer").strip()
                department = body.get("department", "Central Grievance Redressal").strip()

                if not new_status or not remarks:
                    return self._send_error(400, "Both 'status' and 'remarks' are required for official status updates.")

                success, msg = database.update_complaint_status(
                    complaint_id=complaint_id,
                    new_status=new_status,
                    officer_name=officer_name,
                    department=department,
                    remarks=remarks
                )

                if success:
                    updated = database.get_complaint(complaint_id)
                    return self._send_json(200, {
                        "success": True,
                        "message": msg,
                        "complaint": updated
                    })
                return self._send_error(400, msg)
            except Exception as e:
                traceback.print_exc()
                return self._send_error(500, f"Server error: {str(e)}")

        # ------------------- FORWARD COMPLAINT -------------------
        if path.startswith("/api/complaints/") and path.endswith("/forward"):
            try:
                parts = path.split("/")
                complaint_id = parts[3]
                body = self._read_json_body()

                new_dept = body.get("department", "").strip()
                remarks = body.get("remarks", "Inter-departmental forwarding for statutory action.").strip()
                officer_name = body.get("officer_name", "Grievance Triage Officer").strip()

                if not new_dept:
                    return self._send_error(400, "Please select the target department to forward the grievance.")

                success, msg = database.forward_complaint(
                    complaint_id=complaint_id,
                    new_department=new_dept,
                    officer_name=officer_name,
                    forward_remarks=remarks
                )

                if success:
                    updated = database.get_complaint(complaint_id)
                    return self._send_json(200, {
                        "success": True,
                        "message": msg,
                        "complaint": updated
                    })
                return self._send_error(400, msg)
            except Exception as e:
                traceback.print_exc()
                return self._send_error(500, f"Server error: {str(e)}")

        # ------------------- CITIZEN FEEDBACK -------------------
        if path.startswith("/api/complaints/") and path.endswith("/feedback"):
            try:
                parts = path.split("/")
                complaint_id = parts[3]
                body = self._read_json_body()

                rating = int(body.get("rating", 5))
                feedback = body.get("feedback", "").strip()

                database.submit_citizen_feedback(complaint_id, rating, feedback)
                return self._send_json(200, {
                    "success": True,
                    "message": "Thank you! Your feedback has been recorded and helps improve public services."
                })
            except Exception as e:
                traceback.print_exc()
                return self._send_error(500, f"Server error: {str(e)}")

        return self._send_error(404, "Endpoint not found.")

    def _serve_file(self, filepath: Path):
        """Send static file with appropriate MIME type and caching headers."""
        try:
            mime_type, _ = mimetypes.guess_type(str(filepath))
            if not mime_type:
                mime_type = "application/octet-stream"

            content = filepath.read_bytes()
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            traceback.print_exc()
            self._send_error(500, f"Error reading file: {str(e)}")

    def log_message(self, format, *args):
        """Custom concise logging format."""
        sys.stderr.write(f"[{self.log_date_time_string()}] {args[0]} - {args[1]} {args[2]}\n")

def run_server(port=config.PORT, host=config.HOST):
    """Start the multi-threaded web server."""
    # Ensure database is initialized
    database.init_db()

    server_address = (host, port)
    try:
        httpd = ThreadedHTTPServer(server_address, ComplaintRequestHandler)
        print("=" * 72)
        print(" NATIONAL GOVERNMENT COMPLAINT & GRIEVANCE REDRESSAL PORTAL")
        print(" All-in-One Digital Public Grievance Platform")
        print("=" * 72)
        print(f" [OK] Server running at: http://{host}:{port}/")
        print(f" [PORTAL] Citizen Home:       http://{host}:{port}/")
        print(f" [PORTAL] Register Complaint: http://{host}:{port}/register.html")
        print(f" [PORTAL] Track Complaint:    http://{host}:{port}/track.html")
        print(f" [PORTAL] Admin Dashboard:    http://{host}:{port}/admin.html")
        print(f" [PORTAL] Transparency Board: http://{host}:{port}/transparency.html")
        print("=" * 72)
        print(" [INFO] Press CTRL+C in this console to stop the server.\n")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[STOPPING] Shutting down National Grievance Portal server...")
        httpd.server_close()
        print("[OK] Server stopped.")
    except Exception as e:
        print(f"[ERROR] Failed to start server: {e}")

if __name__ == "__main__":
    port = config.PORT
    host = config.HOST
    
    # Support cloud environment variables (e.g. Render, Railway, Heroku)
    if "PORT" in os.environ and os.environ["PORT"].isdigit():
        port = int(os.environ["PORT"])
        host = "0.0.0.0"
    elif len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
        if len(sys.argv) > 2:
            host = sys.argv[2]
            
    run_server(port=port, host=host)
