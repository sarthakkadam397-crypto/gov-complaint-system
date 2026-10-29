# System Architecture & Technical Specification
## All-in-One Government Complaint Management System

---

## 1. System Overview & Architecture Design

The All-in-One Government Complaint Management System implements a multi-tier modular architecture designed for high availability, low latency, and zero deployment friction.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION TIER (UI)                          │
│   ┌──────────────┐   ┌──────────────┐   ┌─────────────┐  ┌───────────┐ │
│   │ Citizen Home │   │ Registration │   │ Track / SLA │  │ Officer   │ │
│   │ (index.html) │   │ (register)   │   │ (track.html)│  │ (admin)   │ │
│   └───────┬──────┘   └──────┬───────┘   └──────┬──────┘  └─────┬─────┘ │
│           │                 │                  │               │       │
│           └─────────────────┼──────────────────┼───────────────┘       │
│                             ▼                                          │
│           HTML5 / CSS3 / Vanilla ES6+ Fetch API Client                 │
└─────────────────────────────┬──────────────────────────────────────────┘
                              │ HTTP / RESTful JSON
                              ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       APPLICATION LOGIC TIER                           │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Multi-Threaded HTTP Server (app.py) / Optional Flask           │   │
│   └───────────────────────┬────────────────────────────────────────┘   │
│                           │                                            │
│   ┌───────────────┬───────┴───────┬───────────────┬────────────────┐   │
│   │ Triage Router │ Auth / Token  │ File Evidence │ Status Machine │   │
│   │ & Validation  │ Engine        │ Handler       │ & Audit Logger │   │
│   └───────┬───────┴───────┬───────┴───────┬───────┴────────┬───────┘   │
└───────────┼───────────────┼───────────────┼────────────────┼───────────┘
            │               │               │                │
            ▼               ▼               ▼                ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          DATA STORAGE TIER                             │
│   ┌───────────────────────────────┐   ┌────────────────────────────┐   │
│   │ SQLite3 Database Engine       │   │ File Evidence Storage      │   │
│   │ (complaints.db)               │   │ (/uploads/ directory)      │   │
│   │ Users • Complaints • Timeline │   │ Documents • Photos • PDFs  │   │
│   └───────────────────────────────┘   └────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Entity-Relationship (ER) Model

```mermaid
erDiagram
    USERS ||--o{ COMPLAINTS : "audits / resolves"
    COMPLAINTS ||--|{ COMPLAINT_TIMELINE : "possesses history"
    COMPLAINTS ||--o{ COMPLAINT_ATTACHMENTS : "contains"
    
    USERS {
        int id PK
        string username UK
        string password_hash
        string full_name
        string role
        string department
        string badge_number
        string email
        string phone
        datetime created_at
    }

    COMPLAINTS {
        int id PK
        string complaint_id UK
        string citizen_name
        string citizen_phone
        string citizen_email
        string citizen_aadhaar_last4
        string category
        string subcategory
        string subject
        string description
        string state
        string district
        string pincode
        string incident_address
        string incident_date
        string urgency
        string status
        string assigned_department
        string assigned_officer
        string resolution_remarks
        int citizen_rating
        string citizen_feedback
        datetime created_at
        datetime updated_at
    }

    COMPLAINT_TIMELINE {
        int id PK
        string complaint_id FK
        string action_type
        string status
        string department
        string officer_name
        string remarks
        datetime timestamp
    }

    COMPLAINT_ATTACHMENTS {
        int id PK
        string complaint_id FK
        string original_name
        string stored_filename
        int file_size
        datetime uploaded_at
    }
```

---

## 3. Data Flow Diagram (DFD Level 1)

```
[Citizen] ─────── Lodges Complaint ─────────> (1.0 Registration Desk)
                                                        │
                                                        ├── Store Record & Attachments ──> [Complaints DB]
                                                        │
[Citizen] <────── Returns Complaint ID ─────────────────┤
                                                        │
                                                        ▼
[Nodal Officer] <── Assigns & Reviews ────── (2.0 Triage & Forwarding)
       │                                                │
       │                                                ├── Write Audit Log ──> [Timeline DB]
       ▼                                                │
(3.0 Field Redressal Action) ───────────────────────────┘
       │
       ├── Updates Status (In Progress / Resolved)
       ▼
(4.0 Citizen Tracking & Feedback) <────── Query Status & Timeline ────── [Citizen]
       │
       └── Submits 5-Star Rating & Review ──> [Complaints DB]
```

---

## 4. Complaint Lifecycle State Transition Machine

```mermaid
stateDiagram-v2
    [*] --> Submitted: Citizen submits grievance
    Submitted --> Under_Review: Nodal Officer begins triage
    Under_Review --> Forwarded: Transferred to specialized dept
    Under_Review --> In_Progress: Direct action initiated
    Forwarded --> In_Progress: Field team dispatched
    In_Progress --> Resolved: Corrective action verified
    Under_Review --> Rejected: Out of jurisdiction / False
    Resolved --> [*]: Citizen feedback recorded
    Rejected --> [*]: Case closed
```

---

## 5. Security & Privacy Safeguards

1. **Authentication**:
   - SHA-256 cryptographic password hashing with unique salt string.
   - Bearer session token verification for privileged officer mutations.
2. **Citizen Privacy**:
   - Identity numbers (Aadhaar) are strictly masked to the last 4 digits only.
   - Public transparency pages anonymize citizen names to uphold privacy while keeping grievance status public.
3. **Evidence File Safety**:
   - Filenames are sanitized and prepended with UTC timestamp tokens to prevent file collisions.
   - Strict extension whitelisting (`.png`, `.jpg`, `.jpeg`, `.pdf`, `.docx`, `.txt`) and 10 MB payload limits prevent directory traversal or remote script execution.
4. **Data Integrity**:
   - Foreign key cascading ensures timeline and attachment records remain synchronized with root complaint entries.
   - Database operations use atomic commits with automatic rollback on error.
