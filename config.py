"""
All-in-One Government Complaint Management System
Configuration Settings
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "complaints.db"
UPLOAD_FOLDER = BASE_DIR / "uploads"
STATIC_FOLDER = BASE_DIR / "static"

PORT = 5000
HOST = "127.0.0.1"

# Upload limits
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".txt", ".doc", ".docx"}

# Complaint Categories
CATEGORIES = [
    "Cybercrime",
    "Online Scams and Fraud",
    "Police-Related Issues",
    "Road and Infrastructure Problems",
    "Traffic Management",
    "Public Services",
    "Corruption",
    "Sanitation",
    "Electricity",
    "Water Supply",
    "Other Government-Related Issues"
]

# Lifecyle Statuses
STATUSES = [
    "Submitted",
    "Under Review",
    "Forwarded to Concerned Department",
    "In Progress",
    "Resolved",
    "Rejected"
]

# Government Departments
DEPARTMENTS = [
    {
        "id": "CYBER",
        "name": "Cybercrime Investigation Cell",
        "email": "cybercell@gov.in",
        "helpline": "1930",
        "head": "Dy. SP Rajesh Kumar"
    },
    {
        "id": "EOW",
        "name": "Economic Offences Wing & Financial Fraud",
        "email": "fraud-cell@gov.in",
        "helpline": "155260",
        "head": "Inspector Sunita Rao"
    },
    {
        "id": "POLICE",
        "name": "State Police & Law Enforcement",
        "email": "police.grievance@gov.in",
        "helpline": "112",
        "head": "ACP Manoj Verma"
    },
    {
        "id": "PWD",
        "name": "Public Works Department (Roads & Bridges)",
        "email": "pwd.roads@gov.in",
        "helpline": "1800-11-2233",
        "head": "Executive Engineer K. S. Sharma"
    },
    {
        "id": "TRAFFIC",
        "name": "Traffic Management Directorate",
        "email": "traffic.helpline@gov.in",
        "helpline": "1095",
        "head": "DCP Traffic A. K. Singh"
    },
    {
        "id": "SANITATION",
        "name": "Municipal Corporation & Sanitation Dept",
        "email": "sanitation@mc.gov.in",
        "helpline": "1969",
        "head": "Health Officer Dr. R. Mehra"
    },
    {
        "id": "POWER",
        "name": "State Electricity Board (Distribution)",
        "email": "complaints@powercorp.gov.in",
        "helpline": "1912",
        "head": "Superintending Engineer V. Patel"
    },
    {
        "id": "WATER",
        "name": "Jal Board (Water Supply & Drainage)",
        "email": "jalboard.helpline@gov.in",
        "helpline": "1916",
        "head": "Zonal Engineer P. Deshmukh"
    },
    {
        "id": "VIGILANCE",
        "name": "Anti-Corruption Bureau & Vigilance Commission",
        "email": "vigilance@state.gov.in",
        "helpline": "1064",
        "head": "Director Vigilance S. Nair"
    },
    {
        "id": "PUBLIC_SRV",
        "name": "Citizen Services & Public Grievances",
        "email": "pgportal@gov.in",
        "helpline": "1800-11-4000",
        "head": "Nodal Officer Ananya Sen"
    }
]
