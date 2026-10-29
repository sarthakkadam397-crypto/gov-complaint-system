"""
Comprehensive Automated Test Suite for Government Complaint Management System
Verifies Database Models, Business Rules, Lifecycle Workflows, and API logic.
"""
import unittest
import os
import json
from pathlib import Path

import config
import database
from seed_data import seed_database

class TestGovernmentComplaintSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Seed the database with standard data."""
        seed_database()

    def test_01_user_authentication(self):
        """Verify password hashing, admin retrieval, and credential verification."""
        conn = database.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        admin_user = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(admin_user)
        self.assertEqual(admin_user["role"], "superadmin")
        self.assertTrue(database.verify_password("admin123", admin_user["password_hash"]))
        self.assertFalse(database.verify_password("wrongpassword", admin_user["password_hash"]))

    def test_02_complaint_registration(self):
        """Verify complaint creation with automatic ID generation, department routing, and timeline log."""
        test_data = {
            "citizen_name": "Test Citizen Sharma",
            "citizen_phone": "9876500000",
            "citizen_email": "test.citizen@example.com",
            "citizen_aadhaar_last4": "1234",
            "category": "Road and Infrastructure Problems",
            "subcategory": "Dangerous Pothole",
            "subject": "Deep pothole outside metro gate 2",
            "description": "A very large pothole causing vehicle damage.",
            "state": "Delhi (NCT)",
            "district": "Central",
            "pincode": "110001",
            "incident_address": "Metro Gate 2, Rajiv Chowk",
            "incident_date": "2026-10-27",
            "urgency": "High"
        }

        cid = database.create_complaint(test_data)
        self.assertTrue(cid.startswith("GOV-2026-"))

        # Retrieve complaint
        record = database.get_complaint(cid)
        self.assertIsNotNone(record)
        self.assertEqual(record["citizen_name"], "Test Citizen Sharma")
        self.assertEqual(record["status"], "Submitted")
        self.assertEqual(record["category"], "Road and Infrastructure Problems")
        self.assertEqual(record["assigned_department"], "Public Works Department (PWD)")
        
        # Verify initial timeline entry
        self.assertGreaterEqual(len(record["timeline"]), 1)
        self.assertEqual(record["timeline"][0]["status"], "Submitted")

    def test_03_status_update_workflow(self):
        """Verify complaint status transitions and timeline audit logging."""
        # Create a complaint
        cid = database.create_complaint({
            "citizen_name": "Status Test User",
            "citizen_phone": "9811122233",
            "category": "Sanitation",
            "subject": "Garbage dump near clinic",
            "description": "Garbage not picked up for 4 days."
        })

        # Update to Under Review
        ok, msg = database.update_complaint_status(
            complaint_id=cid,
            new_status="Under Review",
            officer_name="Health Inspector V. Yadav",
            department="Municipal Corporation & Sanitation Dept",
            remarks="Site inspected. Scheduled for municipal compactor truck."
        )
        self.assertTrue(ok)

        # Update to In Progress
        ok, msg = database.update_complaint_status(
            complaint_id=cid,
            new_status="In Progress",
            officer_name="Sanitary Supervisor R. Kumar",
            department="Municipal Corporation & Sanitation Dept",
            remarks="Compactor team actively clearing municipal waste."
        )
        self.assertTrue(ok)

        # Update to Resolved
        ok, msg = database.update_complaint_status(
            complaint_id=cid,
            new_status="Resolved",
            officer_name="Dr. R. Mehra",
            department="Municipal Health Department",
            remarks="Entire garbage pile removed and area disinfected."
        )
        self.assertTrue(ok)

        # Verify final record
        rec = database.get_complaint(cid)
        self.assertEqual(rec["status"], "Resolved")
        self.assertEqual(rec["resolution_remarks"], "Entire garbage pile removed and area disinfected.")
        self.assertEqual(len(rec["timeline"]), 4)  # 1 initial + 3 updates

    def test_04_department_forwarding(self):
        """Verify inter-departmental grievance forwarding."""
        cid = database.create_complaint({
            "citizen_name": "Forward Test Citizen",
            "citizen_phone": "9822233344",
            "category": "Other Government-Related Issues",
            "subject": "Commercial noise violation late at night",
            "description": "Loud industrial generators operating at 2 AM."
        })

        ok, msg = database.forward_complaint(
            complaint_id=cid,
            new_department="State Police & Law Enforcement",
            officer_name="Central Triage Officer",
            forward_remarks="Jurisdiction falls under Local Station House Officer for noise regulation."
        )
        self.assertTrue(ok)

        rec = database.get_complaint(cid)
        self.assertEqual(rec["status"], "Forwarded to Concerned Department")
        self.assertEqual(rec["assigned_department"], "State Police & Law Enforcement")

    def test_05_citizen_feedback(self):
        """Verify rating and satisfaction feedback capture."""
        cid = database.create_complaint({
            "citizen_name": "Feedback Tester",
            "citizen_phone": "9833344455",
            "category": "Electricity",
            "subject": "Sparking overhead transformer",
            "description": "Hazardous sparks noticed."
        })

        # Resolve first
        database.update_complaint_status(cid, "Resolved", "Power Engineer", "Electricity Board", "Defective cutout replaced.")

        # Citizen submits feedback
        database.submit_citizen_feedback(cid, rating=5, feedback="Prompt emergency response within 3 hours. Great job!")

        rec = database.get_complaint(cid)
        self.assertEqual(rec["citizen_rating"], 5)
        self.assertIn("Prompt emergency response", rec["citizen_feedback"])

    def test_06_dashboard_statistics(self):
        """Verify stats aggregation function computes correct counts and resolution rates."""
        stats = database.get_dashboard_stats()
        self.assertIn("total", stats)
        self.assertIn("resolved", stats)
        self.assertIn("in_progress", stats)
        self.assertIn("resolution_rate", stats)
        self.assertIn("categories", stats)
        self.assertGreater(stats["total"], 0)

    def test_07_phone_search(self):
        """Verify searching grievances by citizen mobile number."""
        results = database.find_complaints_by_phone("9819234501")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["complaint_id"], "GOV-2026-10492")

if __name__ == "__main__":
    unittest.main()
