"""
Flask Application wrapper for All-in-One Government Complaint Management System.
Allows running with Flask or Gunicorn in production environments.
"""
import os
import base64
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, redirect
import config
import database

app = Flask(__name__, static_folder="static", static_url_path="")
app.config["SECRET_KEY"] = "gov-portal-secret-key-2026"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# Initialize DB on load
database.init_db()

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    if (Path(app.static_folder) / filename).exists():
        return send_from_directory(app.static_folder, filename)
    return send_from_directory(app.static_folder, "index.html")

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(config.UPLOAD_FOLDER, filename)

@app.route("/api/meta")
def get_meta():
    return jsonify({
        "success": True,
        "categories": config.CATEGORIES,
        "statuses": config.STATUSES,
        "departments": config.DEPARTMENTS
    })

@app.route("/api/stats")
def get_stats():
    return jsonify({"success": True, "stats": database.get_dashboard_stats()})

@app.route("/api/announcements")
def get_announcements():
    return jsonify({"success": True, "announcements": database.get_public_announcements()})

@app.route("/api/complaints", methods=["GET"])
def list_complaints():
    filters = {}
    for param in ["status", "category", "urgency", "department"]:
        if request.args.get(param):
            filters[param] = request.args.get(param)
    
    search = request.args.get("search", "")
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))

    result = database.list_complaints(filters, search, limit, offset)
    return jsonify({"success": True, **result})

@app.route("/api/complaints/<complaint_id>", methods=["GET"])
def get_complaint(complaint_id):
    complaint = database.get_complaint(complaint_id)
    if complaint:
        return jsonify({"success": True, "complaint": complaint})
    return jsonify({"success": False, "error": f"Complaint {complaint_id} not found"}), 404

@app.route("/api/search-phone")
def search_phone():
    phone = request.args.get("phone", "")
    if not phone:
        return jsonify({"success": False, "error": "Missing phone number"}), 400
    results = database.find_complaints_by_phone(phone)
    return jsonify({"success": True, "complaints": results})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_row = cursor.fetchone()
    conn.close()

    if not user_row or not database.verify_password(password, user_row["password_hash"]):
        return jsonify({"success": False, "error": "Invalid username or password"}), 401

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
    return jsonify({"success": True, "token": token, "user": user_info})

@app.route("/api/complaints", methods=["POST"])
def create_complaint():
    data = request.get_json(silent=True) or {}
    citizen_name = data.get("citizen_name", "").strip()
    citizen_phone = data.get("citizen_phone", "").strip()
    category = data.get("category", "").strip()
    subject = data.get("subject", "").strip()
    description = data.get("description", "").strip()

    if not citizen_name or not citizen_phone or not category or not subject or not description:
        return jsonify({"success": False, "error": "All mandatory fields must be completed."}), 400

    # Handle optional base64 file upload
    file_data = data.get("file_data")
    file_name = data.get("file_name")
    attachments = []
    if file_data and file_name:
        try:
            if "," in file_data:
                _, encoded = file_data.split(",", 1)
            else:
                encoded = file_data
            file_bytes = base64.b64decode(encoded)
            safe_name = os.path.basename(file_name).replace(" ", "_")
            timestamp = database.datetime.datetime.now().strftime("%Y%m%d%H%M%S_")
            stored = f"{timestamp}{safe_name}"
            dest = config.UPLOAD_FOLDER / stored
            dest.write_bytes(file_bytes)
            attachments.append({
                "original_name": file_name,
                "stored_filename": stored,
                "file_size": len(file_bytes)
            })
        except Exception as e:
            print("File upload error:", e)

    data["attachments"] = attachments
    complaint_id = database.create_complaint(data)
    return jsonify({
        "success": True,
        "complaint_id": complaint_id,
        "message": "Complaint successfully registered in the portal."
    }), 201

@app.route("/api/complaints/<complaint_id>/status", methods=["POST"])
def update_status(complaint_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    remarks = data.get("remarks", "").strip()
    officer_name = data.get("officer_name", "Authorized Officer")
    department = data.get("department", "Public Grievances")

    if not new_status or not remarks:
        return jsonify({"success": False, "error": "Status and remarks are required."}), 400

    success, msg = database.update_complaint_status(complaint_id, new_status, officer_name, department, remarks)
    if success:
        return jsonify({"success": True, "message": msg, "complaint": database.get_complaint(complaint_id)})
    return jsonify({"success": False, "error": msg}), 400

@app.route("/api/complaints/<complaint_id>/forward", methods=["POST"])
def forward(complaint_id):
    data = request.get_json(silent=True) or {}
    new_dept = data.get("department")
    remarks = data.get("remarks", "Inter-departmental forwarding")
    officer_name = data.get("officer_name", "Triage Officer")

    if not new_dept:
        return jsonify({"success": False, "error": "Destination department required."}), 400

    success, msg = database.forward_complaint(complaint_id, new_dept, officer_name, remarks)
    if success:
        return jsonify({"success": True, "message": msg, "complaint": database.get_complaint(complaint_id)})
    return jsonify({"success": False, "error": msg}), 400

@app.route("/api/complaints/<complaint_id>/feedback", methods=["POST"])
def feedback(complaint_id):
    data = request.get_json(silent=True) or {}
    rating = int(data.get("rating", 5))
    text = data.get("feedback", "")
    database.submit_citizen_feedback(complaint_id, rating, text)
    return jsonify({"success": True, "message": "Feedback submitted successfully."})

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True)
