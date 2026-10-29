"""
Database models and queries for All-in-One Government Complaint Management System
Uses Python's built-in sqlite3 database engine.
"""
import sqlite3
import hashlib
import random
import string
import datetime
from pathlib import Path
from config import DATABASE_PATH, CATEGORIES, STATUSES

def get_db():
    """Return a database connection with row factory configured."""
    conn = sqlite3.connect(DATABASE_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt."""
    salt = "gov_cms_secure_salt_2026"
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password match."""
    return hash_password(plain_password) == hashed_password

def generate_complaint_id() -> str:
    """Generate a realistic official complaint tracking ID, e.g. GOV-2026-78392."""
    year = datetime.datetime.now().year
    digits = ''.join(random.choices(string.digits, k=5))
    return f"GOV-{year}-{digits}"

def init_db():
    """Initialize database tables and indexes."""
    conn = get_db()
    cursor = conn.cursor()

    # Users / Officers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,          -- 'superadmin', 'officer', 'citizen'
        department TEXT,
        badge_number TEXT,
        email TEXT,
        phone TEXT,
        created_at TEXT NOT NULL
    );
    """)

    # Complaints Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id TEXT UNIQUE NOT NULL,
        citizen_name TEXT NOT NULL,
        citizen_phone TEXT NOT NULL,
        citizen_email TEXT,
        citizen_aadhaar_last4 TEXT,
        category TEXT NOT NULL,
        subcategory TEXT,
        subject TEXT NOT NULL,
        description TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        pincode TEXT NOT NULL,
        incident_address TEXT,
        incident_date TEXT,
        urgency TEXT DEFAULT 'Medium', -- 'Low', 'Medium', 'High', 'Critical'
        status TEXT NOT NULL DEFAULT 'Submitted',
        assigned_department TEXT,
        assigned_officer TEXT,
        resolution_remarks TEXT,
        citizen_rating INTEGER,
        citizen_feedback TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # Complaint Timeline (Audit Log & Status History)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaint_timeline (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id TEXT NOT NULL,
        action_type TEXT NOT NULL,
        status TEXT NOT NULL,
        department TEXT,
        officer_name TEXT,
        remarks TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE
    );
    """)

    # Complaint Attachments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaint_attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id TEXT NOT NULL,
        original_name TEXT NOT NULL,
        stored_filename TEXT NOT NULL,
        file_size INTEGER,
        uploaded_at TEXT NOT NULL,
        FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE
    );
    """)

    # Public Announcements / Alerts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        badge TEXT DEFAULT 'Public Notice',
        created_at TEXT NOT NULL
    );
    """)

    # Indexes for fast lookup
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_complaint_id ON complaints(complaint_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_complaint_phone ON complaints(citizen_phone);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_complaint_status ON complaints(status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_complaint_category ON complaints(category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timeline_complaint ON complaint_timeline(complaint_id);")

    conn.commit()
    conn.close()

def create_complaint(data: dict) -> str:
    """Create a new citizen complaint and add the first timeline record."""
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate unique complaint ID
    complaint_id = generate_complaint_id()
    while True:
        cursor.execute("SELECT id FROM complaints WHERE complaint_id = ?", (complaint_id,))
        if not cursor.fetchone():
            break
        complaint_id = generate_complaint_id()

    # Determine default initial department if specified
    assigned_dept = data.get("assigned_department")
    if not assigned_dept:
        # Auto-route initial triage based on category
        cat_map = {
            "Cybercrime": "Cybercrime Investigation Cell",
            "Online Scams and Fraud": "Economic Offences Wing & Financial Fraud",
            "Police-Related Issues": "State Police & Law Enforcement",
            "Road and Infrastructure Problems": "Public Works Department (PWD)",
            "Traffic Management": "Traffic Management Directorate",
            "Public Services": "Citizen Services & Public Grievances",
            "Corruption": "Anti-Corruption Bureau & Vigilance Commission",
            "Sanitation": "Municipal Corporation & Sanitation Dept",
            "Electricity": "State Electricity Board (Distribution)",
            "Water Supply": "Jal Board (Water Supply & Drainage)",
        }
        assigned_dept = cat_map.get(data.get("category", ""), "Public Grievance Redressal Cell")

    cursor.execute("""
    INSERT INTO complaints (
        complaint_id, citizen_name, citizen_phone, citizen_email, citizen_aadhaar_last4,
        category, subcategory, subject, description, state, district, pincode,
        incident_address, incident_date, urgency, status, assigned_department,
        assigned_officer, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Submitted', ?, 'Central Triage Officer', ?, ?)
    """, (
        complaint_id,
        data.get("citizen_name", "").strip(),
        data.get("citizen_phone", "").strip(),
        data.get("citizen_email", "").strip(),
        data.get("citizen_aadhaar_last4", "").strip(),
        data.get("category", "Other Government-Related Issues"),
        data.get("subcategory", ""),
        data.get("subject", "").strip(),
        data.get("description", "").strip(),
        data.get("state", "Delhi (NCT)").strip(),
        data.get("district", "Central").strip(),
        data.get("pincode", "110001").strip(),
        data.get("incident_address", "").strip(),
        data.get("incident_date", now_str[:10]),
        data.get("urgency", "Medium"),
        assigned_dept,
        now_str,
        now_str
    ))

    # Add initial timeline step
    cursor.execute("""
    INSERT INTO complaint_timeline (
        complaint_id, action_type, status, department, officer_name, remarks, timestamp
    ) VALUES (?, 'SUBMITTED', 'Submitted', 'Citizen Portal', 'Citizen / Self', 'Complaint registered successfully on the National Grievance Portal. Assigned for initial triage.', ?)
    """, (complaint_id, now_str))

    # Add initial attachment if provided
    attachments = data.get("attachments", [])
    for att in attachments:
        cursor.execute("""
        INSERT INTO complaint_attachments (
            complaint_id, original_name, stored_filename, file_size, uploaded_at
        ) VALUES (?, ?, ?, ?, ?)
        """, (
            complaint_id,
            att.get("original_name", "document.pdf"),
            att.get("stored_filename", "sample.pdf"),
            att.get("file_size", 0),
            now_str
        ))

    conn.commit()
    conn.close()
    return complaint_id

def get_complaint(complaint_id: str):
    """Retrieve complete complaint record including timeline and attachments."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints WHERE complaint_id = ? COLLATE NOCASE", (complaint_id.strip(),))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    complaint = dict(row)

    # Get timeline
    cursor.execute("""
    SELECT * FROM complaint_timeline 
    WHERE complaint_id = ? 
    ORDER BY id ASC
    """, (complaint["complaint_id"],))
    timeline = [dict(t) for t in cursor.fetchall()]

    # Get attachments
    cursor.execute("""
    SELECT * FROM complaint_attachments 
    WHERE complaint_id = ? 
    ORDER BY id ASC
    """, (complaint["complaint_id"],))
    attachments = [dict(a) for a in cursor.fetchall()]

    conn.close()
    complaint["timeline"] = timeline
    complaint["attachments"] = attachments
    return complaint

def find_complaints_by_phone(phone: str):
    """Search complaints by citizen phone number."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT complaint_id, citizen_name, category, subject, status, urgency, created_at, updated_at
    FROM complaints
    WHERE citizen_phone LIKE ?
    ORDER BY id DESC
    """, (f"%{phone.strip()}%",))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def list_complaints(filters: dict = None, search: str = "", limit: int = 50, offset: int = 0):
    """Query complaints with dynamic filtering, search, and pagination."""
    conn = get_db()
    cursor = conn.cursor()

    clauses = ["1=1"]
    params = []

    if filters:
        if filters.get("status"):
            clauses.append("status = ?")
            params.append(filters["status"])
        if filters.get("category"):
            clauses.append("category = ?")
            params.append(filters["category"])
        if filters.get("urgency"):
            clauses.append("urgency = ?")
            params.append(filters["urgency"])
        if filters.get("department"):
            clauses.append("assigned_department LIKE ?")
            params.append(f"%{filters['department']}%")

    if search:
        search_term = f"%{search.strip()}%"
        clauses.append("(complaint_id LIKE ? OR citizen_name LIKE ? OR citizen_phone LIKE ? OR subject LIKE ? OR description LIKE ?)")
        params.extend([search_term, search_term, search_term, search_term, search_term])

    where_clause = " AND ".join(clauses)

    # Total count
    cursor.execute(f"SELECT COUNT(*) AS total FROM complaints WHERE {where_clause}", params)
    total_count = cursor.fetchone()["total"]

    # Paginated results
    query = f"""
    SELECT id, complaint_id, citizen_name, citizen_phone, category, subject, urgency,
           status, assigned_department, assigned_officer, created_at, updated_at
    FROM complaints
    WHERE {where_clause}
    ORDER BY id DESC
    LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])
    cursor.execute(query, params)
    items = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "items": items
    }

def update_complaint_status(complaint_id: str, new_status: str, officer_name: str, department: str, remarks: str):
    """Update complaint status and record official timeline action."""
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT status, assigned_department FROM complaints WHERE complaint_id = ?", (complaint_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Complaint not found"

    old_status = row["status"]
    dept = department or row["assigned_department"]

    resolution_note = remarks if new_status in ("Resolved", "Rejected") else None

    if resolution_note:
        cursor.execute("""
        UPDATE complaints 
        SET status = ?, assigned_department = ?, assigned_officer = ?, 
            resolution_remarks = ?, updated_at = ?
        WHERE complaint_id = ?
        """, (new_status, dept, officer_name, resolution_note, now_str, complaint_id))
    else:
        cursor.execute("""
        UPDATE complaints 
        SET status = ?, assigned_department = ?, assigned_officer = ?, updated_at = ?
        WHERE complaint_id = ?
        """, (new_status, dept, officer_name, now_str, complaint_id))

    action_type = f"STATUS_CHANGE_{new_status.upper().replace(' ', '_')}"
    cursor.execute("""
    INSERT INTO complaint_timeline (
        complaint_id, action_type, status, department, officer_name, remarks, timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (complaint_id, action_type, new_status, dept, officer_name, remarks, now_str))

    conn.commit()
    conn.close()
    return True, "Complaint status updated successfully"

def forward_complaint(complaint_id: str, new_department: str, officer_name: str, forward_remarks: str):
    """Forward a complaint to another department."""
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT * FROM complaints WHERE complaint_id = ?", (complaint_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Complaint not found"

    new_status = "Forwarded to Concerned Department"
    cursor.execute("""
    UPDATE complaints 
    SET status = ?, assigned_department = ?, assigned_officer = ?, updated_at = ?
    WHERE complaint_id = ?
    """, (new_status, new_department, f"Nodal Officer, {new_department}", now_str, complaint_id))

    cursor.execute("""
    INSERT INTO complaint_timeline (
        complaint_id, action_type, status, department, officer_name, remarks, timestamp
    ) VALUES (?, 'FORWARDED', ?, ?, ?, ?, ?)
    """, (complaint_id, new_status, new_department, officer_name, forward_remarks, now_str))

    conn.commit()
    conn.close()
    return True, f"Complaint successfully forwarded to {new_department}"

def submit_citizen_feedback(complaint_id: str, rating: int, feedback: str):
    """Store citizen rating (1-5 stars) and feedback on resolved complaints."""
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    UPDATE complaints 
    SET citizen_rating = ?, citizen_feedback = ?, updated_at = ?
    WHERE complaint_id = ?
    """, (rating, feedback.strip(), now_str, complaint_id))

    cursor.execute("""
    INSERT INTO complaint_timeline (
        complaint_id, action_type, status, department, officer_name, remarks, timestamp
    ) VALUES (?, 'FEEDBACK_SUBMITTED', 'Resolved', 'Citizen Feedback Portal', 'Citizen', ?, ?)
    """, (complaint_id, f"Citizen submitted satisfaction rating: {rating}/5 stars. Feedback: '{feedback}'", now_str))

    conn.commit()
    conn.close()
    return True

def get_dashboard_stats():
    """Compute aggregate analytics for administrative dashboard and public transparency."""
    conn = get_db()
    cursor = conn.cursor()

    # Total counts by status
    cursor.execute("""
    SELECT status, COUNT(*) as count 
    FROM complaints 
    GROUP BY status
    """)
    status_counts = {row["status"]: row["count"] for row in cursor.fetchall()}

    total_complaints = sum(status_counts.values())
    resolved = status_counts.get("Resolved", 0)
    in_progress = status_counts.get("In Progress", 0)
    forwarded = status_counts.get("Forwarded to Concerned Department", 0)
    under_review = status_counts.get("Under Review", 0)
    submitted = status_counts.get("Submitted", 0)
    rejected = status_counts.get("Rejected", 0)

    resolution_rate = round((resolved / total_complaints * 100), 1) if total_complaints > 0 else 0.0

    # Counts by Category
    cursor.execute("""
    SELECT category, COUNT(*) as count 
    FROM complaints 
    GROUP BY category 
    ORDER BY count DESC
    """)
    category_counts = [dict(row) for row in cursor.fetchall()]

    # Counts by Urgency
    cursor.execute("""
    SELECT urgency, COUNT(*) as count 
    FROM complaints 
    GROUP BY urgency
    """)
    urgency_counts = {row["urgency"]: row["count"] for row in cursor.fetchall()}

    # Average citizen rating
    cursor.execute("SELECT AVG(citizen_rating) as avg_rating, COUNT(citizen_rating) as rated_count FROM complaints WHERE citizen_rating IS NOT NULL")
    rating_row = cursor.fetchone()
    avg_rating = round(rating_row["avg_rating"], 1) if rating_row and rating_row["avg_rating"] else 4.6

    conn.close()

    return {
        "total": total_complaints,
        "resolved": resolved,
        "in_progress": in_progress,
        "forwarded": forwarded,
        "under_review": under_review,
        "submitted": submitted,
        "rejected": rejected,
        "pending": submitted + under_review + forwarded + in_progress,
        "resolution_rate": resolution_rate,
        "avg_rating": avg_rating,
        "categories": category_counts,
        "urgency": urgency_counts
    }

def get_public_announcements():
    """Retrieve official government public announcements."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM announcements ORDER BY id DESC LIMIT 5")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows
