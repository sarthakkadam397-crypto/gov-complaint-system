# All-in-One Government Complaint Management System
### Centralized Digital Public Grievance Redressal & Monitoring Platform

The **All-in-One Government Complaint Management System** is a unified, transparent, and citizen-centric web platform engineered to provide citizens with a single digital window to register, track, and resolve complaints across various government departments and civic utilities.

---

## 🏛️ Project Highlights & Scope

The platform addresses all essential public service categories specified in the citizen charter:

1. **Cybercrime & Data Theft**: Hacking, identity theft, malware/APK fraud, ransomware, social media extortion.
2. **Online Scams & Financial Fraud**: UPI fraud, investment task scams, fake job schemes, phishing websites.
3. **Police-Related Issues**: Refusal to register FIR (Zero FIR compliance), police harassment, misconduct, lack of investigation.
4. **Road and Infrastructure Problems**: Dangerous potholes, road cave-ins, collapsed bridges, broken footpaths, road signage.
5. **Traffic Management**: Defective traffic signals, peak hour gridlocks, illegal encroachment parking, traffic diversion.
6. **Public Services & Citizen Facilities**: Delays in issuance of Ration Cards, Income/Caste certificates, Aadhaar services, pensions.
7. **Corruption & Vigilance**: Demands for bribes, extortion by public officials, misuse of government funds, whistle-blower reports.
8. **Sanitation & Municipal Waste**: Overflowing garbage dumps, uncollected waste, mosquito breeding, toxic municipal dumping.
9. **Electricity & Power Grid**: Transformer explosions, prolonged power outages, dangerous low-hanging wires, billing anomalies.
10. **Water Supply & Drainage**: Sewage-contaminated drinking water, burst pipelines, low water pressure, contaminated supply.
11. **Other Government Issues**: Encroachment of community parks, illegal construction, civic noise pollution, general queries.

---

## 🔄 Complaint Lifecycle & Tracking

Every submitted complaint is assigned a **unique 14-digit Complaint ID** (e.g., `GOV-2026-10492`). Citizens and officials track the complaint across 5 standardized stages:

```
[1. Submitted] ──> [2. Under Review] ──> [3. Forwarded to Dept] ──> [4. In Progress] ──> [5. Resolved]
```

- **Submitted**: Complaint recorded in the national registry; acknowledgement slip generated.
- **Under Review**: Triage nodal officer reviews jurisdiction, inspects documents, and verifies admissibility.
- **Forwarded to Concerned Department**: Inter-departmental transfer to field offices (e.g. Cyber Forensic Unit, PWD Roads, Jal Board).
- **In Progress**: Ground team dispatched, parts repaired, FIR lodged, or site cleared.
- **Resolved**: Official closure remarks issued; citizen can rate redressal quality (1-5 stars) and submit feedback.

---

## 💻 Technology Stack

- **Frontend**:
  - Semantic **HTML5** & responsive **CSS3** (National Portal theme, tricolor accents, mobile-responsive layout).
  - Vanilla **JavaScript (ES6+)** (Dynamic API client, drag-and-drop file upload, base64 encoder, interactive modals).
  - Print-ready stylesheet for printable official acknowledgement slips and resolution certificates.
- **Backend**:
  - **Zero-Dependency Python Web Server** (`app.py`): Runs natively on Python 3 (3.8 - 3.14+) using built-in standard library (`http.server`, `socketserver.ThreadingMixIn`, `json`, `urllib.parse`, `hashlib`, `uuid`).
  - **Optional Flask Server** (`app_flask.py`): Included for academic requirements or deployment on platforms like Render / Heroku / Gunicorn.
- **Database**:
  - **SQLite3** (`complaints.db`): Serverless, zero-configuration relational database with foreign key constraints, indexes, and full audit logs.

---

## 📁 Project Directory Structure

```
gov_complaint_system/
├── app.py                      # Production-ready Python server (Zero external dependencies)
├── app_flask.py                # Optional Flask equivalent server
├── config.py                   # System configuration, departments list, categories, file limits
├── database.py                 # SQLite database schema, queries, audit logging, analytics
├── seed_data.py                # Seeding script with realistic complaints across all 11 categories
├── test_system.py              # Automated unit and integration test suite
├── start.bat                   # 1-Click Windows runner (opens server & browser)
├── start.sh                    # Linux/macOS runner
├── requirements.txt            # Minimal pip dependencies (only if using Flask)
├── SYSTEM_ARCHITECTURE.md      # Detailed academic/technical system architecture
├── README.md                   # Project documentation
├── uploads/                    # Secure directory for citizen uploaded evidence documents
└── static/                     # Frontend UI assets
    ├── index.html              # Citizen Portal Homepage (Hero, Stats, Tracker, Categories, Directory)
    ├── register.html           # Multi-step Complaint Registration Form with file upload
    ├── track.html              # Dedicated Complaint Tracking & Visual Timeline Stepper
    ├── admin.html              # Departmental Officer & Admin Dashboard
    ├── transparency.html       # Public Accountability Scorecard & SLA Charter
    ├── css/
    │   ├── style.css           # National Government portal styling & responsiveness
    │   └── admin.css           # Specialized Officer dashboard layout
    └── js/
        ├── app.js              # Shared toast notifications, badge helpers, date formatting
        ├── register.js         # Form validation, drag-and-drop upload, receipt modal
        ├── track.js            # Live tracking, 5-stage stepper renderer, feedback capture
        └── admin.js            # Officer authentication, filters, status transitions, forwarding
```

---

## 🚀 Quick Start & Live Deployment Guide

### Option A: Make It Live on GitHub Pages (Instant 2-Minute Demo)
See the full step-by-step instructions in [DEPLOYMENT_GUIDE.md](file:///C:/Users/Abhishek/.gemini/antigravity/scratch/gov_complaint_system/DEPLOYMENT_GUIDE.md).
1. Upload this project to a new repository on GitHub.
2. In your GitHub repository, go to **Settings → Pages**.
3. Under Branch, select **`main`** and click **Save**.
4. Your website will be live at `https://<your-username>.github.io/<repo-name>/`.
*(The built-in client engine in `static/js/app.js` runs all registration, 5-stage tracking, and officer dashboard features live right in the browser!)*

### Option B: Deploy on Cloud with Python & SQLite Backend (Render.com)
1. Sign in to [Render.com](https://render.com) using your GitHub account.
2. Click **New + → Web Service** and select your GitHub repository.
3. Build Command: `pip install -r requirements.txt && python seed_data.py`
4. Start Command: `gunicorn app_flask:app --bind 0.0.0.0:$PORT`
5. Click **Create Web Service** to get a 24/7 permanent HTTPS URL.

### Option C: Launch Locally on Your Computer (Windows)
Double-click [start.bat](file:///C:/Users/Abhishek/.gemini/antigravity/scratch/gov_complaint_system/start.bat) or run:
```powershell
python app.py
```
Open **`http://127.0.0.1:5000/`** in your browser.

### 2. Run Automated Verification Tests

Run the test suite to verify all database queries, lifecycle transitions, and API endpoints:
```powershell
python test_system.py
```

---

## 👥 Pre-Seeded Officer Accounts (For Demonstration)

The Admin Portal (`/admin.html`) includes a **1-click evaluation login switcher** for instant access:

| Username | Password | Officer Name | Department / Role |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | Shri Arvind Saxena, IAS | Super Admin, Central Grievance Cell |
| `cyber_officer` | `cyber123` | Dy. SP Rajesh Kumar | Cybercrime Investigation Cell |
| `police_acp` | `police123` | ACP Manoj Verma | State Police & Law Enforcement |
| `pwd_engineer` | `pwd123` | Er. K. S. Sharma | Public Works Department (PWD) |
| `health_officer` | `muni123` | Dr. R. Mehra | Municipal Corporation & Sanitation |
| `power_engineer` | `power123` | Er. V. Patel | State Electricity Board (Distribution) |

---

## 🔍 Pre-Seeded Sample Complaints for Instant Tracking

Test the tracking page (`/track.html`) with any of these pre-seeded complaint IDs:

- **`GOV-2026-10492`**: Cybercrime (APK Banking Trojan debit) — *In Progress (Fund Freeze Notice)*
- **`GOV-2026-44821`**: Road Infrastructure (Deep crater on EM Bypass) — *In Progress (Emergency Crew Dispatched)*
- **`GOV-2026-55932`**: Traffic Management (Defective signal at Silk Board) — *Resolved (Controller Replaced)*
- **`GOV-2026-88901`**: Sanitation (Garbage dump near school) — *Resolved (Compactor Cleared & Sanitized)*
- **`GOV-2026-77823`**: Corruption (Bribe demand for water connection) — *Under Review (Vigilance Trap)*
- **`GOV-2026-99014`**: Electricity (250kVA transformer explosion) — *In Progress (Crane Truck on Site)*

You can also search by complainant mobile number: e.g. **`9819234501`**.

---

## 🌐 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/meta` | Get all categories, valid statuses, and department directory |
| `GET` | `/api/stats` | Aggregate dashboard analytics & resolution percentages |
| `GET` | `/api/announcements` | Public advisories and emergency notices |
| `GET` | `/api/complaints` | Filtered list of complaints (`status`, `category`, `urgency`, `search`) |
| `GET` | `/api/complaints/<id>` | Full complaint record with timeline audit and attachments |
| `GET` | `/api/search-phone?phone=...` | Find complaints filed under a citizen mobile number |
| `POST` | `/api/complaints` | Register new complaint (accepts base64 encoded evidence files) |
| `POST` | `/api/login` | Authenticate officer and issue session token |
| `POST` | `/api/complaints/<id>/status` | Update lifecycle status with official investigation remarks |
| `POST` | `/api/complaints/<id>/forward` | Transfer complaint to a different department |
| `POST` | `/api/complaints/<id>/feedback`| Citizen 1-5 star satisfaction rating and review |

---

## 🎓 Academic Evaluation & Viva Highlights

1. **Grievance Triage Automation**: Automatic department recommendation based on selected category.
2. **Immutable Audit Trail**: Every status change or forward action is permanently timestamped with officer name and remarks.
3. **Citizen Empowerment**: Unique tracking ID, printable acknowledgement receipt, and feedback mechanism.
4. **Zero-Dependency Architecture**: Entire stack operates on Python's built-in standard library without needing external packages or package managers.
