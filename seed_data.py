"""
Seed data script for All-in-One Government Complaint Management System.
Populates admin accounts, realistic government complaints across all 11 categories,
multi-stage timeline audits, and official announcements.
"""
import os
import datetime
from database import init_db, get_db, hash_password

def seed_database():
    print("[INFO] Initializing schema...")
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # Clear existing data for fresh seed
    cursor.execute("DELETE FROM complaint_timeline")
    cursor.execute("DELETE FROM complaint_attachments")
    cursor.execute("DELETE FROM complaints")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM announcements")

    now = datetime.datetime.now()

    def dt_ago(days=0, hours=0, minutes=0):
        t = now - datetime.timedelta(days=days, hours=hours, minutes=minutes)
        return t.strftime("%Y-%m-%d %H:%M:%S")

    print("[INFO] Seeding official officer accounts...")
    users = [
        ("admin", "admin123", "Shri Arvind Saxena, IAS", "superadmin", "Central Grievance Redressal Cell", "IAS-88219", "admin.pgportal@gov.in", "9876543210"),
        ("cyber_officer", "cyber123", "Dy. SP Rajesh Kumar", "officer", "Cybercrime Investigation Cell", "IPS-CYB-402", "cybercell@gov.in", "9811223344"),
        ("police_acp", "police123", "ACP Manoj Verma", "officer", "State Police & Law Enforcement", "ACP-DL-1102", "police.grievance@gov.in", "9822334455"),
        ("pwd_engineer", "pwd123", "Er. K. S. Sharma", "officer", "Public Works Department (PWD)", "PWD-EE-771", "pwd.roads@gov.in", "9833445566"),
        ("health_officer", "muni123", "Dr. R. Mehra", "officer", "Municipal Corporation & Sanitation Dept", "MCD-MHO-339", "sanitation@mc.gov.in", "9844556677"),
        ("power_engineer", "power123", "Er. V. Patel", "officer", "State Electricity Board (Distribution)", "SEB-EE-552", "complaints@powercorp.gov.in", "9855667788"),
    ]

    for u in users:
        cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, role, department, badge_number, email, phone, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (u[0], hash_password(u[1]), u[2], u[3], u[4], u[5], u[6], u[7], dt_ago(days=30)))

    print("[INFO] Seeding official government announcements...")
    announcements = [
        ("Public Advisory: Beware of APK Loan Fraud & Fake Police Digital Arrest Calls", 
         "Citizens are advised that law enforcement agencies never issue digital arrests over video calls. Report any suspicious scam calls immediately to 1930 or submit a complaint here.", 
         "High Alert", dt_ago(days=2)),
        ("Monsoon Infrastructure & Pothole Repair Blitz 2026 Launched", 
         "Public Works Department (PWD) has deployed rapid response civic teams for arterial roads. Pothole complaints are prioritized within 48 hours.", 
         "Civic Update", dt_ago(days=5)),
        ("24x7 Drinking Water Quality Testing & Tanker Support Activated", 
         "Jal Board helpline 1916 is synchronized with this portal. Real-time water supply telemetry complaints are routed immediately to zonal engineers.", 
         "Public Notice", dt_ago(days=8))
    ]
    for a in announcements:
        cursor.execute("INSERT INTO announcements (title, content, badge, created_at) VALUES (?, ?, ?, ?)", a)

    print("[INFO] Seeding realistic complaints across all 11 required categories...")

    sample_complaints = [
        {
            "id": "GOV-2026-10492",
            "citizen_name": "Rohan Deshmukh",
            "citizen_phone": "9819234501",
            "citizen_email": "rohan.deshmukh@gmail.com",
            "citizen_aadhaar_last4": "4829",
            "category": "Cybercrime",
            "subcategory": "Phishing & Banking Fraud",
            "subject": "Unauthorized withdrawal of Rs 68,000 through fraudulent banking APK",
            "description": "Received an SMS claiming electricity bill was overdue with an APK link. Upon installing, screen went dark and Rs 68,000 was debited in two UPI transactions to unknown account. Transaction IDs and screenshots attached.",
            "state": "Maharashtra",
            "district": "Mumbai Suburban",
            "pincode": "400053",
            "incident_address": "Andheri West, Link Road",
            "incident_date": (now - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
            "urgency": "Critical",
            "status": "In Progress",
            "assigned_dept": "Cybercrime Investigation Cell",
            "assigned_officer": "Dy. SP Rajesh Kumar",
            "resolution_remarks": None,
            "created_at": dt_ago(days=3, hours=4),
            "updated_at": dt_ago(days=1, hours=2),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Complaint registered and assigned unique ID GOV-2026-10492.", dt_ago(days=3, hours=4)),
                ("REVIEWED", "Under Review", "Cyber Crime Triage Desk", "Inspector Anjali Joshi", "Cybercrime initial triage completed. Bank accounts identified. Transaction freeze requested under Section 91 CrPC.", dt_ago(days=2, hours=18)),
                ("FORWARDED", "Forwarded to Concerned Department", "Cyber Crime Division", "Dy. SP Rajesh Kumar", "Forwarded to Cyber Forensic & Financial Crime Interception Unit for CDR and IP trace.", dt_ago(days=2, hours=6)),
                ("PROGRESS_UPDATED", "In Progress", "Cyber Forensic Cell", "Dy. SP Rajesh Kumar", "Liaison with merchant gateway initiated. Rs 45,000 successfully frozen in beneficiary wallet. Formal notice issued.", dt_ago(days=1, hours=2))
            ],
            "attachment": ("bank_transaction_screenshot.png", "sample_bank_statement.png", 245000)
        },
        {
            "id": "GOV-2026-21840",
            "citizen_name": "Pooja Sundaram",
            "citizen_phone": "9840123984",
            "citizen_email": "pooja.sundaram@outlook.com",
            "citizen_aadhaar_last4": "7104",
            "category": "Online Scams and Fraud",
            "subcategory": "Work-From-Home / Telegram Task Scam",
            "subject": "Extortion and fraud of Rs 1,40,000 under pretext of YouTube video rating jobs",
            "description": "Joined a Telegram group promising daily earnings for liking videos. Initially received Rs 300, then was coerced into depositing Rs 1.4 lakhs in progressive 'prepaid crypto merchant tasks' with withdrawal blocked unless more funds paid.",
            "state": "Tamil Nadu",
            "district": "Chennai",
            "pincode": "600028",
            "incident_address": "R. A. Puram",
            "incident_date": (now - datetime.timedelta(days=6)).strftime("%Y-%m-%d"),
            "urgency": "High",
            "status": "Forwarded to Concerned Department",
            "assigned_dept": "Economic Offences Wing & Financial Fraud",
            "assigned_officer": "Inspector Sunita Rao",
            "resolution_remarks": None,
            "created_at": dt_ago(days=6, hours=5),
            "updated_at": dt_ago(days=4, hours=1),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Complaint registered with proof of payment screenshots.", dt_ago(days=6, hours=5)),
                ("REVIEWED", "Under Review", "Cyber Grievance Nodal", "Sub-Inspector V. Raman", "Cross-verified beneficiary mule accounts across 3 payment banks.", dt_ago(days=5, hours=10)),
                ("FORWARDED", "Forwarded to Concerned Department", "Central Grievance Cell", "ACP Vigilance", "Forwarded to Economic Offences Wing (Cyber Taskforce) for coordinated interstate arrest warrant.", dt_ago(days=4, hours=1))
            ],
            "attachment": ("telegram_chat_records.pdf", "sample_chat_records.pdf", 512000)
        },
        {
            "id": "GOV-2026-33918",
            "citizen_name": "Vikramaditya Chauhan",
            "citizen_phone": "9871144220",
            "citizen_email": "v.chauhan@gmail.com",
            "citizen_aadhaar_last4": "9312",
            "category": "Police-Related Issues",
            "subcategory": "FIR Registration Refusal",
            "subject": "Local station refused to lodge FIR for motorcycle theft citing jurisdictional ambiguity",
            "description": "My two-wheeler (Registration DL 4S CA 1944) was stolen outside Sector 22 market. When I visited the police station, duty officer refused to log FIR and asked to check another outpost.",
            "state": "Delhi (NCT)",
            "district": "South West",
            "pincode": "110077",
            "incident_address": "Sector 22 Market, Dwarka",
            "incident_date": (now - datetime.timedelta(days=4)).strftime("%Y-%m-%d"),
            "urgency": "High",
            "status": "In Progress",
            "assigned_dept": "State Police & Law Enforcement",
            "assigned_officer": "ACP Manoj Verma",
            "resolution_remarks": None,
            "created_at": dt_ago(days=4, hours=8),
            "updated_at": dt_ago(days=1, hours=5),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Complaint submitted with CCTV footage location details.", dt_ago(days=4, hours=8)),
                ("REVIEWED", "Under Review", "Police HQ Grievance Cell", "Inspector Hardeep Singh", "Taking cognizance under Zero FIR guidelines.", dt_ago(days=3, hours=12)),
                ("PROGRESS_UPDATED", "In Progress", "Dwarka Sub-Division", "ACP Manoj Verma", "Zero FIR No. 418/2026 registered. Show-cause explanation sought from concerned Station Duty Officer.", dt_ago(days=1, hours=5))
            ],
            "attachment": ("vehicle_rc_copy.pdf", "sample_vehicle_rc.pdf", 310000)
        },
        {
            "id": "GOV-2026-44821",
            "citizen_name": "Anita Sengupta",
            "citizen_phone": "9830219876",
            "citizen_email": "anita.sengupta@kolkata.gov.in",
            "citizen_aadhaar_last4": "6032",
            "category": "Road and Infrastructure Problems",
            "subcategory": "Dangerous Potholes & Cave-in",
            "subject": "Deep crater pothole on EM Bypass connector causing multiple two-wheeler skids",
            "description": "A massive 2-foot deep trench pothole has developed right after the flyover ramp. Two motorcyclists have already fallen in the last 48 hours. Immediate emergency bitumen patching required.",
            "state": "West Bengal",
            "district": "Kolkata",
            "pincode": "700107",
            "incident_address": "EM Bypass Junction, Near Ruby Crossing",
            "incident_date": (now - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            "urgency": "Critical",
            "status": "In Progress",
            "assigned_dept": "Public Works Department (PWD)",
            "assigned_officer": "Er. K. S. Sharma",
            "resolution_remarks": None,
            "created_at": dt_ago(days=2, hours=10),
            "updated_at": dt_ago(hours=14),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Civic infrastructure complaint registered with live geotagged photo.", dt_ago(days=2, hours=10)),
                ("REVIEWED", "Under Review", "PWD Central Control Room", "Er. Pradeep Dey", "Priority ticket categorized as hazard level 4 (Critical).", dt_ago(days=2, hours=4)),
                ("PROGRESS_UPDATED", "In Progress", "PWD Roads Maintenance Division 3", "Er. K. S. Sharma", "Road repair van and cold-mix asphalt gang dispatched. Warning cones erected on site.", dt_ago(hours=14))
            ],
            "attachment": ("pothole_photo_geotag.jpg", "sample_pothole.jpg", 420000)
        },
        {
            "id": "GOV-2026-55932",
            "citizen_name": "Suresh Babu",
            "citizen_phone": "9845012398",
            "citizen_email": "sureshbabu.bengaluru@gmail.com",
            "citizen_aadhaar_last4": "1190",
            "category": "Traffic Management",
            "subcategory": "Defective Traffic Lights & Congestion",
            "subject": "Traffic lights non-functional for 5 days at Outer Ring Road Silk Board Junction",
            "description": "Signal is constantly stuck on flashing yellow. Peak hour delays have increased by 45 minutes and pedestrians are unable to cross safely.",
            "state": "Karnataka",
            "district": "Bengaluru Urban",
            "pincode": "560068",
            "incident_address": "Silk Board Junction, Outer Ring Road",
            "incident_date": (now - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
            "urgency": "High",
            "status": "Resolved",
            "assigned_dept": "Traffic Management Directorate",
            "assigned_officer": "DCP Traffic A. K. Singh",
            "resolution_remarks": "Traffic signaling microcontroller was replaced and synchronized with central ATCS (Adaptive Traffic Control System). Timing cycle recalibrated and tested operational on 25-Oct-2026.",
            "created_at": dt_ago(days=7, hours=6),
            "updated_at": dt_ago(days=2, hours=1),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Complaint registered.", dt_ago(days=7, hours=6)),
                ("REVIEWED", "Under Review", "Traffic Command Center", "Inspector G. Murthy", "Inspection verified controller failure.", dt_ago(days=6, hours=12)),
                ("FORWARDED", "Forwarded to Concerned Department", "Traffic Signal Maintenance Wing", "DCP Traffic A. K. Singh", "Maintenance team assigned for circuit board replacement.", dt_ago(days=5, hours=8)),
                ("PROGRESS_UPDATED", "In Progress", "Signal Tech Cell", "DCP Traffic A. K. Singh", "New motherboard installed and sensor loop tested.", dt_ago(days=3, hours=4)),
                ("RESOLVED", "Resolved", "Traffic Directorate", "DCP Traffic A. K. Singh", "Traffic signaling microcontroller was replaced and synchronized with central ATCS. Timing cycle recalibrated and tested operational.", dt_ago(days=2, hours=1))
            ],
            "attachment": ("traffic_junction_photo.jpg", "sample_traffic.jpg", 180000)
        },
        {
            "id": "GOV-2026-66710",
            "citizen_name": "Meera Nambiar",
            "citizen_phone": "9895112233",
            "citizen_email": "meera.nambiar@yahoo.com",
            "citizen_aadhaar_last4": "8245",
            "category": "Public Services",
            "subcategory": "Citizen Certificates & Welfare Delay",
            "subject": "Income & Caste Certificate application pending over 50 days despite all valid documents",
            "description": "Applied for state merit scholarship required for college admission. Application number KL-REV-2026-4401 has been stalled without any objection or query.",
            "state": "Kerala",
            "district": "Ernakulam",
            "pincode": "682016",
            "incident_address": "Kochi Taluk Revenue Office",
            "incident_date": (now - datetime.timedelta(days=12)).strftime("%Y-%m-%d"),
            "urgency": "Medium",
            "status": "Under Review",
            "assigned_dept": "Citizen Services & Public Grievances",
            "assigned_officer": "Nodal Officer Ananya Sen",
            "resolution_remarks": None,
            "created_at": dt_ago(days=5, hours=3),
            "updated_at": dt_ago(days=3, hours=7),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Grievance submitted with e-District application acknowledgement slip.", dt_ago(days=5, hours=3)),
                ("REVIEWED", "Under Review", "State Public Service Delivery Oversight", "Nodal Officer Ananya Sen", "Summoned application file from Taluk Tehsildar. Disciplinary notice issued for exceeding Citizen Charter timeline of 15 days.", dt_ago(days=3, hours=7))
            ],
            "attachment": ("acknowledgement_slip.pdf", "sample_ack_slip.pdf", 195000)
        },
        {
            "id": "GOV-2026-77823",
            "citizen_name": "Deepak Khurana",
            "citizen_phone": "9810445566",
            "citizen_email": "deepak.khurana@live.com",
            "citizen_aadhaar_last4": "3391",
            "category": "Corruption",
            "subcategory": "Bribery & Malpractice in Civic Approvals",
            "subject": "Junior engineer demanding unofficial facilitation fee of Rs 25,000 for residential water meter sanction",
            "description": "All plumbing drawings and statutory fees have been paid. Field official explicitly stated file will not move without cash payment. Audio recording and formal affidavit submitted.",
            "state": "Punjab",
            "district": "Ludhiana",
            "pincode": "141001",
            "incident_address": "Zonal Municipal Water Dept, Zone B",
            "incident_date": (now - datetime.timedelta(days=8)).strftime("%Y-%m-%d"),
            "urgency": "Critical",
            "status": "Under Review",
            "assigned_dept": "Anti-Corruption Bureau & Vigilance Commission",
            "assigned_officer": "Director Vigilance S. Nair",
            "resolution_remarks": None,
            "created_at": dt_ago(days=4, hours=2),
            "updated_at": dt_ago(days=2, hours=11),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Vigilance complaint lodged under Whistleblower Protection provisions.", dt_ago(days=4, hours=2)),
                ("REVIEWED", "Under Review", "Vigilance Secret Investigation Wing", "Director Vigilance S. Nair", "Complainant verified. Preliminary inquiry registered and surveillance trap authorized.", dt_ago(days=2, hours=11))
            ],
            "attachment": ("vigilance_affidavit.pdf", "sample_vigilance_affidavit.pdf", 480000)
        },
        {
            "id": "GOV-2026-88901",
            "citizen_name": "Sunil Kumar Tiwari",
            "citizen_phone": "9826117788",
            "citizen_email": "suniltiwari@gmail.com",
            "citizen_aadhaar_last4": "5512",
            "category": "Sanitation",
            "subcategory": "Open Garbage Dump & Pest Infestation",
            "subject": "Piles of rotting municipal garbage outside Government Girls Senior Secondary School",
            "description": "Garbage collection truck has not visited Ward 14 for 10 days. Dump has spilled onto school entrance, foul smell is unbearable, and stray animals create risk for school children.",
            "state": "Madhya Pradesh",
            "district": "Bhopal",
            "pincode": "462003",
            "incident_address": "Ward 14, Near GGSSS, Jahangirabad",
            "incident_date": (now - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "urgency": "High",
            "status": "Resolved",
            "assigned_dept": "Municipal Corporation & Sanitation Dept",
            "assigned_officer": "Health Officer Dr. R. Mehra",
            "resolution_remarks": "Site fully cleared by emergency municipal compactor on 26-Oct-2026. Area sanitized with lime and disinfectant spray. Daily morning compactor route reinstated.",
            "created_at": dt_ago(days=5, hours=8),
            "updated_at": dt_ago(days=1, hours=3),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Sanitation complaint submitted with photos.", dt_ago(days=5, hours=8)),
                ("REVIEWED", "Under Review", "Swachh Civic Control Desk", "Sanitary Inspector V. Yadav", "Inspection confirmed accumulated waste.", dt_ago(days=4, hours=14)),
                ("FORWARDED", "Forwarded to Concerned Department", "Zonal Solid Waste Management", "Dr. R. Mehra", "Emergency compactor crew scheduled.", dt_ago(days=3, hours=6)),
                ("PROGRESS_UPDATED", "In Progress", "Sanitation Field Crew", "Health Officer Dr. R. Mehra", "Two 10-ton compactors deployed. 14 metric tonnes of municipal solid waste removed.", dt_ago(days=2, hours=4)),
                ("RESOLVED", "Resolved", "Municipal Health Department", "Health Officer Dr. R. Mehra", "Site fully cleared by emergency municipal compactor on 26-Oct-2026. Area sanitized with lime and disinfectant spray. Daily morning compactor route reinstated.", dt_ago(days=1, hours=3))
            ],
            "attachment": ("garbage_site_photo.jpg", "sample_garbage.jpg", 340000)
        },
        {
            "id": "GOV-2026-99014",
            "citizen_name": "Harish Chandra Gupta",
            "citizen_phone": "9837119900",
            "citizen_email": "hcgupta.agra@yahoo.com",
            "citizen_aadhaar_last4": "4280",
            "category": "Electricity",
            "subcategory": "Transformer Burnout & Prolonged Power Outage",
            "subject": "Distribution transformer burned down, 180 households in darkness for 36 hours",
            "description": "High voltage surge caused loud explosion in 250kVA transformer near Sub-station 4. Power supply completely dead for entire block, water pumps unable to run.",
            "state": "Uttar Pradesh",
            "district": "Agra",
            "pincode": "282001",
            "incident_address": "Kamla Nagar, Block C",
            "incident_date": (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "urgency": "Critical",
            "status": "In Progress",
            "assigned_dept": "State Electricity Board (Distribution)",
            "assigned_officer": "Er. V. Patel",
            "resolution_remarks": None,
            "created_at": dt_ago(days=1, hours=12),
            "updated_at": dt_ago(hours=4),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Critical electricity blackout complaint submitted.", dt_ago(days=1, hours=12)),
                ("REVIEWED", "Under Review", "Discom Central Grid Desk", "Junior Engineer S. Bansal", "Confirmed transformer burnout due to phase imbalance.", dt_ago(days=1, hours=8)),
                ("PROGRESS_UPDATED", "In Progress", "Sub-Station Emergency Team", "Er. V. Patel", "Replacement 250kVA transformer loaded from divisional store onto crane truck. Installation underway on site.", dt_ago(hours=4))
            ],
            "attachment": ("burnt_transformer_pic.jpg", "sample_transformer.jpg", 280000)
        },
        {
            "id": "GOV-2026-11234",
            "citizen_name": "Lakshmi Narayanan",
            "citizen_phone": "9848123456",
            "citizen_email": "lakshmi.narayan@rediffmail.com",
            "citizen_aadhaar_last4": "2087",
            "category": "Water Supply",
            "subcategory": "Pipeline Burst & Sewage Contamination",
            "subject": "Drinking water supply mixed with sewage drain water; dark brown foul-smelling tap water",
            "description": "Main feeder drinking pipeline broke right adjacent to storm drain. Over 80 homes receiving sewage contaminated water. Residents falling sick with gastroenteritis.",
            "state": "Telangana",
            "district": "Hyderabad",
            "pincode": "500034",
            "incident_address": "Banjara Hills, Road No 12",
            "incident_date": (now - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            "urgency": "Critical",
            "status": "In Progress",
            "assigned_dept": "Jal Board (Water Supply & Drainage)",
            "assigned_officer": "Zonal Engineer P. Deshmukh",
            "resolution_remarks": None,
            "created_at": dt_ago(days=2, hours=7),
            "updated_at": dt_ago(hours=8),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Emergency contamination grievance filed.", dt_ago(days=2, hours=7)),
                ("REVIEWED", "Under Review", "Jal Board Emergency Cell", "Assistant Engineer K. Rao", "Water supply to line immediately isolated to prevent public health risk. Drinking water tankers deployed.", dt_ago(days=1, hours=16)),
                ("PROGRESS_UPDATED", "In Progress", "Pipeline Repair Wing", "Zonal Engineer P. Deshmukh", "Excavator digging trench to isolate ruptured 300mm ductile iron pipe. Chlorination test scheduled post welding.", dt_ago(hours=8))
            ],
            "attachment": ("contaminated_water_sample.jpg", "sample_water.jpg", 310000)
        },
        {
            "id": "GOV-2026-12345",
            "citizen_name": "Baljit Singh Gill",
            "citizen_phone": "9872019283",
            "citizen_email": "baljit.gill@gmail.com",
            "citizen_aadhaar_last4": "6419",
            "category": "Other Government-Related Issues",
            "subcategory": "Illegal Public Land Encroachment",
            "subject": "Commercial unauthorized tin sheds erected on designated public community park",
            "description": "Sector community park green belt has been encroached by commercial scrap dealers who have erected permanent tin sheds and unauthorized generator sets.",
            "state": "Punjab",
            "district": "SAS Nagar (Mohali)",
            "pincode": "160055",
            "incident_address": "Sector 70 Community Park, Phase 8",
            "incident_date": (now - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "urgency": "Medium",
            "status": "Forwarded to Concerned Department",
            "assigned_dept": "Public Works Department (PWD)",
            "assigned_officer": "Executive Engineer K. S. Sharma",
            "resolution_remarks": None,
            "created_at": dt_ago(days=8, hours=2),
            "updated_at": dt_ago(days=5, hours=9),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Encroachment complaint registered with cadastral survey maps.", dt_ago(days=8, hours=2)),
                ("REVIEWED", "Under Review", "Town Planning Grievance Wing", "Town Planner R. Chawla", "Checked master plan. Area confirmed as designated green park zone.", dt_ago(days=6, hours=14)),
                ("FORWARDED", "Forwarded to Concerned Department", "Enforcement & Demolition Directorate", "Er. K. S. Sharma", "Demolition notice under Section 12 Public Premises Act served on occupants with 7-day vacate notice.", dt_ago(days=5, hours=9))
            ],
            "attachment": ("encroachment_photos.pdf", "sample_encroachment.pdf", 620000)
        },
        {
            "id": "GOV-2026-13579",
            "citizen_name": "Kavita R. Nair",
            "citizen_phone": "9847055443",
            "citizen_email": "kavita.nair@gmail.com",
            "citizen_aadhaar_last4": "5021",
            "category": "Cybercrime",
            "subcategory": "Identity Theft & Fake Social Profile",
            "subject": "Impersonation and defamatory fake profiles created on Instagram using private family photos",
            "description": "Unknown miscreant created fake account using my name, phone number and manipulated photos, soliciting money from contacts. URLs and screenshots provided.",
            "state": "Kerala",
            "district": "Thiruvananthapuram",
            "pincode": "695001",
            "incident_address": "Statue Junction",
            "incident_date": (now - datetime.timedelta(days=14)).strftime("%Y-%m-%d"),
            "urgency": "High",
            "status": "Resolved",
            "assigned_dept": "Cybercrime Investigation Cell",
            "assigned_officer": "Dy. SP Rajesh Kumar",
            "resolution_remarks": "Formal emergency takedown notice issued to Meta/Instagram legal compliance cell under Section 79(3)(b) of IT Act. Fake profile deactivated and origin IP logged for charge-sheet.",
            "created_at": dt_ago(days=14, hours=1),
            "updated_at": dt_ago(days=4, hours=10),
            "timeline": [
                ("SUBMITTED", "Submitted", "Citizen Portal", "Citizen / Self", "Cybercrime complaint filed.", dt_ago(days=14, hours=1)),
                ("REVIEWED", "Under Review", "Cyber Women & Child Safety Cell", "Inspector Kavitha Menon", "Verified evidence and preserved URL headers.", dt_ago(days=12, hours=8)),
                ("FORWARDED", "Forwarded to Concerned Department", "Cyber Investigation Wing", "Dy. SP Rajesh Kumar", "Notified social media intermediary.", dt_ago(days=10, hours=5)),
                ("PROGRESS_UPDATED", "In Progress", "Cyber Intermediary Liaison Desk", "Dy. SP Rajesh Kumar", "Emergency preservation order sent to platform operator.", dt_ago(days=7, hours=2)),
                ("RESOLVED", "Resolved", "Cybercrime Cell", "Dy. SP Rajesh Kumar", "Formal emergency takedown notice issued under Section 79(3)(b) IT Act. Fake profile removed and IP traces documented in investigation diary.", dt_ago(days=4, hours=10))
            ],
            "attachment": ("fake_profile_screenshot.jpg", "sample_profile_screenshot.jpg", 175000)
        }
    ]

    for item in sample_complaints:
        cursor.execute("""
        INSERT INTO complaints (
            complaint_id, citizen_name, citizen_phone, citizen_email, citizen_aadhaar_last4,
            category, subcategory, subject, description, state, district, pincode,
            incident_address, incident_date, urgency, status, assigned_department,
            assigned_officer, resolution_remarks, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["id"],
            item["citizen_name"],
            item["citizen_phone"],
            item["citizen_email"],
            item["citizen_aadhaar_last4"],
            item["category"],
            item["subcategory"],
            item["subject"],
            item["description"],
            item["state"],
            item["district"],
            item["pincode"],
            item["incident_address"],
            item["incident_date"],
            item["urgency"],
            item["status"],
            item["assigned_dept"],
            item["assigned_officer"],
            item["resolution_remarks"],
            item["created_at"],
            item["updated_at"]
        ))

        # Seed timeline
        for t in item["timeline"]:
            cursor.execute("""
            INSERT INTO complaint_timeline (
                complaint_id, action_type, status, department, officer_name, remarks, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (item["id"], t[0], t[1], t[2], t[3], t[4], t[5]))

        # Seed attachment
        att = item.get("attachment")
        if att:
            cursor.execute("""
            INSERT INTO complaint_attachments (
                complaint_id, original_name, stored_filename, file_size, uploaded_at
            ) VALUES (?, ?, ?, ?, ?)
            """, (item["id"], att[0], att[1], att[2], item["created_at"]))

    conn.commit()
    conn.close()
    print(f"[OK] Seeded {len(users)} users, {len(announcements)} announcements, and {len(sample_complaints)} detailed complaints!")

if __name__ == "__main__":
    seed_database()
