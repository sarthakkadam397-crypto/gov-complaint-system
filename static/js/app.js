/**
 * All-in-One Government Complaint Management System
 * Shared Utilities, Navigation Helpers & Client-Side Offline/GitHub Pages Storage Engine
 */

const API_BASE = "";

// Show Toast Notification
function showToast(message, type = "info") {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  
  let icon = "ℹ️";
  if (type === "success") icon = "✅";
  if (type === "error") icon = "⚠️";

  toast.innerHTML = `<span>${icon}</span><div style="flex:1;">${message}</div>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Generate Status Badge HTML
function getStatusBadge(status) {
  if (!status) status = "Submitted";
  const slug = status.toLowerCase().replace(/\s+/g, "-");
  return `<span class="badge-status badge-${slug}">● ${status}</span>`;
}

// Generate Urgency Badge HTML
function getUrgencyBadge(urgency) {
  if (!urgency) urgency = "Medium";
  const slug = urgency.toLowerCase();
  return `<span class="badge-urgency urgency-${slug}">${urgency}</span>`;
}

// Format Date string
function formatDate(dateStr) {
  if (!dateStr) return "N/A";
  try {
    const d = new Date(dateStr.replace(" ", "T"));
    if (isNaN(d.getTime())) return dateStr;
    return d.toLocaleDateString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  } catch (e) {
    return dateStr;
  }
}

// Format File Size
function formatFileSize(bytes) {
  if (!bytes) return "0 KB";
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

// ============================================================================
// CLIENT-SIDE ADAPTER FOR GITHUB PAGES / STATIC HOSTING
// Automatically activates when running on github.io or without Python server!
// ============================================================================

const DEFAULT_CATEGORIES = [
  "Cybercrime", "Online Scams and Fraud", "Police-Related Issues",
  "Road and Infrastructure Problems", "Traffic Management", "Public Services",
  "Corruption", "Sanitation", "Electricity", "Water Supply", "Other Government-Related Issues"
];

const DEFAULT_STATUSES = [
  "Submitted", "Under Review", "Forwarded to Concerned Department",
  "In Progress", "Resolved", "Rejected"
];

const DEFAULT_DEPARTMENTS = [
  { id: "CYBER", name: "Cybercrime Investigation Cell", email: "cybercell@gov.in", helpline: "1930", head: "Dy. SP Rajesh Kumar" },
  { id: "EOW", name: "Economic Offences Wing & Financial Fraud", email: "fraud-cell@gov.in", helpline: "155260", head: "Inspector Sunita Rao" },
  { id: "POLICE", name: "State Police & Law Enforcement", email: "police.grievance@gov.in", helpline: "112", head: "ACP Manoj Verma" },
  { id: "PWD", name: "Public Works Department (PWD)", email: "pwd.roads@gov.in", helpline: "1800-11-2233", head: "Executive Engineer K. S. Sharma" },
  { id: "TRAFFIC", name: "Traffic Management Directorate", email: "traffic.helpline@gov.in", helpline: "1095", head: "DCP Traffic A. K. Singh" },
  { id: "SANITATION", name: "Municipal Corporation & Sanitation Dept", email: "sanitation@mc.gov.in", helpline: "1969", head: "Health Officer Dr. R. Mehra" },
  { id: "POWER", name: "State Electricity Board (Distribution)", email: "complaints@powercorp.gov.in", helpline: "1912", head: "Superintending Engineer V. Patel" },
  { id: "WATER", name: "Jal Board (Water Supply & Drainage)", email: "jalboard.helpline@gov.in", helpline: "1916", head: "Zonal Engineer P. Deshmukh" },
  { id: "VIGILANCE", name: "Anti-Corruption Bureau & Vigilance Commission", email: "vigilance@state.gov.in", helpline: "1064", head: "Director Vigilance S. Nair" },
  { id: "PUBLIC_SRV", name: "Citizen Services & Public Grievances", email: "pgportal@gov.in", helpline: "1800-11-4000", head: "Nodal Officer Ananya Sen" }
];

const DEMO_OFFICERS = [
  { username: "admin", password: "admin123", full_name: "Shri Arvind Saxena, IAS", role: "superadmin", department: "Central Grievance Redressal Cell", badge_number: "IAS-88219" },
  { username: "cyber_officer", password: "cyber123", full_name: "Dy. SP Rajesh Kumar", role: "officer", department: "Cybercrime Investigation Cell", badge_number: "IPS-CYB-402" },
  { username: "police_acp", password: "police123", full_name: "ACP Manoj Verma", role: "officer", department: "State Police & Law Enforcement", badge_number: "ACP-DL-1102" },
  { username: "pwd_engineer", password: "pwd123", full_name: "Er. K. S. Sharma", role: "officer", department: "Public Works Department (PWD)", badge_number: "PWD-EE-771" },
  { username: "health_officer", password: "muni123", full_name: "Dr. R. Mehra", role: "officer", department: "Municipal Corporation & Sanitation Dept", badge_number: "MCD-MHO-339" },
  { username: "power_engineer", password: "power123", full_name: "Er. V. Patel", role: "officer", department: "State Electricity Board (Distribution)", badge_number: "SEB-EE-552" }
];

const INITIAL_COMPLAINTS = [
  {
    complaint_id: "GOV-2026-10492",
    citizen_name: "Rohan Deshmukh",
    citizen_phone: "9819234501",
    citizen_email: "rohan.deshmukh@gmail.com",
    category: "Cybercrime",
    subcategory: "Phishing & Banking Fraud",
    subject: "Unauthorized withdrawal of Rs 68,000 through fraudulent banking APK",
    description: "Received an SMS claiming electricity bill was overdue with an APK link. Upon installing, screen went dark and Rs 68,000 was debited in two UPI transactions. Transaction IDs and screenshots attached.",
    state: "Maharashtra", district: "Mumbai Suburban", pincode: "400053",
    incident_address: "Andheri West, Link Road", incident_date: "2026-10-24",
    urgency: "Critical", status: "In Progress",
    assigned_department: "Cybercrime Investigation Cell", assigned_officer: "Dy. SP Rajesh Kumar",
    created_at: "2026-10-24 12:46:00", updated_at: "2026-10-26 14:50:00",
    timeline: [
      { action_type: "SUBMITTED", status: "Submitted", department: "Citizen Portal", officer_name: "Citizen / Self", remarks: "Complaint registered and assigned unique ID GOV-2026-10492.", timestamp: "2026-10-24 12:46:00" },
      { action_type: "REVIEWED", status: "Under Review", department: "Cyber Crime Triage Desk", officer_name: "Inspector Anjali Joshi", remarks: "Cybercrime initial triage completed. Bank accounts identified. Transaction freeze requested.", timestamp: "2026-10-25 10:15:00" },
      { action_type: "FORWARDED", status: "Forwarded to Concerned Department", department: "Cyber Crime Division", officer_name: "Dy. SP Rajesh Kumar", remarks: "Forwarded to Cyber Forensic & Financial Crime Interception Unit.", timestamp: "2026-10-25 18:30:00" },
      { action_type: "PROGRESS_UPDATED", status: "In Progress", department: "Cyber Forensic Cell", officer_name: "Dy. SP Rajesh Kumar", remarks: "Liaison with merchant gateway initiated. Rs 45,000 successfully frozen in beneficiary wallet.", timestamp: "2026-10-26 14:50:00" }
    ],
    attachments: [{ original_name: "bank_transaction_screenshot.png", stored_filename: "sample_bank_statement.png", file_size: 245000 }]
  },
  {
    complaint_id: "GOV-2026-44821",
    citizen_name: "Anita Sengupta",
    citizen_phone: "9830219876",
    citizen_email: "anita.sengupta@kolkata.gov.in",
    category: "Road and Infrastructure Problems",
    subcategory: "Dangerous Potholes & Cave-in",
    subject: "Deep crater pothole on EM Bypass connector causing multiple two-wheeler skids",
    description: "A massive 2-foot deep trench pothole has developed right after the flyover ramp. Two motorcyclists have already fallen in the last 48 hours. Immediate emergency bitumen patching required.",
    state: "West Bengal", district: "Kolkata", pincode: "700107",
    incident_address: "EM Bypass Junction, Near Ruby Crossing", incident_date: "2026-10-25",
    urgency: "Critical", status: "In Progress",
    assigned_department: "Public Works Department (PWD)", assigned_officer: "Er. K. S. Sharma",
    created_at: "2026-10-25 08:30:00", updated_at: "2026-10-26 19:40:00",
    timeline: [
      { action_type: "SUBMITTED", status: "Submitted", department: "Citizen Portal", officer_name: "Citizen / Self", remarks: "Civic infrastructure complaint registered with live geotagged photo.", timestamp: "2026-10-25 08:30:00" },
      { action_type: "REVIEWED", status: "Under Review", department: "PWD Central Control Room", officer_name: "Er. Pradeep Dey", remarks: "Priority ticket categorized as hazard level 4 (Critical).", timestamp: "2026-10-25 14:00:00" },
      { action_type: "PROGRESS_UPDATED", status: "In Progress", department: "PWD Roads Maintenance Division 3", officer_name: "Er. K. S. Sharma", remarks: "Road repair van and cold-mix asphalt gang dispatched. Warning cones erected on site.", timestamp: "2026-10-26 19:40:00" }
    ],
    attachments: [{ original_name: "pothole_photo_geotag.jpg", stored_filename: "sample_pothole.jpg", file_size: 420000 }]
  },
  {
    complaint_id: "GOV-2026-55932",
    citizen_name: "Suresh Babu",
    citizen_phone: "9845012398",
    citizen_email: "sureshbabu.bengaluru@gmail.com",
    category: "Traffic Management",
    subcategory: "Defective Traffic Lights",
    subject: "Traffic lights non-functional for 5 days at Outer Ring Road Silk Board Junction",
    description: "Signal is constantly stuck on flashing yellow. Peak hour delays have increased by 45 minutes and pedestrians are unable to cross safely.",
    state: "Karnataka", district: "Bengaluru Urban", pincode: "560068",
    incident_address: "Silk Board Junction, Outer Ring Road", incident_date: "2026-10-20",
    urgency: "High", status: "Resolved",
    assigned_department: "Traffic Management Directorate", assigned_officer: "DCP Traffic A. K. Singh",
    resolution_remarks: "Traffic signaling microcontroller was replaced and synchronized with central ATCS. Timing cycle recalibrated and tested operational on 25-Oct-2026.",
    citizen_rating: 5, citizen_feedback: "Signal was repaired and traffic flow is now smooth. Excellent job!",
    created_at: "2026-10-20 09:15:00", updated_at: "2026-10-25 15:30:00",
    timeline: [
      { action_type: "SUBMITTED", status: "Submitted", department: "Citizen Portal", officer_name: "Citizen / Self", remarks: "Complaint registered.", timestamp: "2026-10-20 09:15:00" },
      { action_type: "PROGRESS_UPDATED", status: "In Progress", department: "Signal Tech Cell", officer_name: "DCP Traffic A. K. Singh", remarks: "New motherboard installed and sensor loop tested.", timestamp: "2026-10-24 11:00:00" },
      { action_type: "RESOLVED", status: "Resolved", department: "Traffic Directorate", officer_name: "DCP Traffic A. K. Singh", remarks: "Traffic signaling microcontroller was replaced and synchronized with central ATCS.", timestamp: "2026-10-25 15:30:00" }
    ],
    attachments: []
  },
  {
    complaint_id: "GOV-2026-88901",
    citizen_name: "Sunil Kumar Tiwari",
    citizen_phone: "9826117788",
    citizen_email: "suniltiwari@gmail.com",
    category: "Sanitation",
    subcategory: "Open Garbage Dump",
    subject: "Piles of rotting municipal garbage outside Government Girls Senior Secondary School",
    description: "Garbage collection truck has not visited Ward 14 for 10 days. Dump has spilled onto school entrance, foul smell is unbearable.",
    state: "Madhya Pradesh", district: "Bhopal", pincode: "462003",
    incident_address: "Ward 14, Near GGSSS, Jahangirabad", incident_date: "2026-10-22",
    urgency: "High", status: "Resolved",
    assigned_department: "Municipal Corporation & Sanitation Dept", assigned_officer: "Health Officer Dr. R. Mehra",
    resolution_remarks: "Site fully cleared by emergency municipal compactor on 26-Oct-2026. Area sanitized with lime and disinfectant spray.",
    citizen_rating: 5, citizen_feedback: "Quick clearance once reported. Very grateful.",
    created_at: "2026-10-22 10:20:00", updated_at: "2026-10-26 16:45:00",
    timeline: [
      { action_type: "SUBMITTED", status: "Submitted", department: "Citizen Portal", officer_name: "Citizen / Self", remarks: "Sanitation complaint submitted with photos.", timestamp: "2026-10-22 10:20:00" },
      { action_type: "PROGRESS_UPDATED", status: "In Progress", department: "Sanitation Field Crew", officer_name: "Health Officer Dr. R. Mehra", remarks: "Two 10-ton compactors deployed. 14 metric tonnes removed.", timestamp: "2026-10-25 14:00:00" },
      { action_type: "RESOLVED", status: "Resolved", department: "Municipal Health Department", officer_name: "Health Officer Dr. R. Mehra", remarks: "Site fully cleared by emergency compactor. Area sanitized.", timestamp: "2026-10-26 16:45:00" }
    ],
    attachments: []
  }
];

function getLocalStore() {
  let data = localStorage.getItem("gov_cms_complaints_data");
  if (!data) {
    localStorage.setItem("gov_cms_complaints_data", JSON.stringify(INITIAL_COMPLAINTS));
    return [...INITIAL_COMPLAINTS];
  }
  try {
    return JSON.parse(data);
  } catch (e) {
    return [...INITIAL_COMPLAINTS];
  }
}

function saveLocalStore(items) {
  localStorage.setItem("gov_cms_complaints_data", JSON.stringify(items));
}

// Intercept fetch requests for seamless GitHub Pages static execution
const originalFetch = window.fetch;
window.fetch = async function(input, init = {}) {
  const url = typeof input === "string" ? input : input.url;
  const isGithubOrFile = window.location.hostname.includes("github.io") || window.location.protocol === "file:";

  // Try real network request first if running on local server or custom backend
  if (!isGithubOrFile) {
    try {
      const response = await originalFetch(input, init);
      if (response.ok || (response.status !== 404 && response.status !== 0)) {
        return response;
      }
    } catch (e) {
      // Fall through to mock adapter
    }
  }

  // Handle client-side fallback
  const parsedUrl = new URL(url, window.location.href);
  const path = parsedUrl.pathname;
  const method = (init.method || "GET").toUpperCase();

  const makeJsonRes = (body, status = 200) => {
    return new Response(JSON.stringify(body), {
      status: status,
      headers: { "Content-Type": "application/json" }
    });
  };

  // 1. Meta
  if (path.endsWith("/api/meta")) {
    return makeJsonRes({ success: true, categories: DEFAULT_CATEGORIES, statuses: DEFAULT_STATUSES, departments: DEFAULT_DEPARTMENTS });
  }

  // 2. Announcements
  if (path.endsWith("/api/announcements")) {
    return makeJsonRes({
      success: true,
      announcements: [
        { title: "Public Advisory: Beware of APK Financial Scam Calls", content: "Citizens are advised that law enforcement agencies never issue digital arrests over video calls. Report any suspicious scam calls immediately to 1930." }
      ]
    });
  }

  // 3. Stats
  if (path.endsWith("/api/stats")) {
    const list = getLocalStore();
    const resolved = list.filter(c => c.status === "Resolved").length;
    const in_progress = list.filter(c => c.status === "In Progress").length;
    const under_review = list.filter(c => c.status === "Under Review").length;
    const submitted = list.filter(c => c.status === "Submitted").length;
    const forwarded = list.filter(c => c.status === "Forwarded to Concerned Department").length;
    const total = list.length;
    const rate = total > 0 ? ((resolved / total) * 100).toFixed(1) : "0.0";

    const catMap = {};
    list.forEach(c => { catMap[c.category] = (catMap[c.category] || 0) + 1; });
    const categories = Object.keys(catMap).map(k => ({ category: k, count: catMap[k] }));

    return makeJsonRes({
      success: true,
      stats: { total, resolved, in_progress, under_review, submitted, forwarded, pending: total - resolved, resolution_rate: rate, avg_rating: 4.8, categories }
    });
  }

  // 4. Officer Login
  if (path.endsWith("/api/login") && method === "POST") {
    const body = JSON.parse(init.body || "{}");
    const officer = DEMO_OFFICERS.find(o => o.username === body.username && o.password === body.password);
    if (officer) {
      return makeJsonRes({ success: true, token: "mock_token_" + Date.now(), user: officer, message: `Welcome, ${officer.full_name}` });
    }
    return makeJsonRes({ success: false, error: "Invalid username or password" }, 401);
  }

  // 5. Search Phone
  if (path.endsWith("/api/search-phone")) {
    const phone = parsedUrl.searchParams.get("phone") || "";
    const list = getLocalStore();
    const matching = list.filter(c => c.citizen_phone && c.citizen_phone.includes(phone));
    return makeJsonRes({ success: true, complaints: matching });
  }

  // 6. Complaint Status Update
  if (path.includes("/api/complaints/") && path.endsWith("/status") && method === "POST") {
    const id = path.split("/").slice(-2, -1)[0];
    const body = JSON.parse(init.body || "{}");
    const list = getLocalStore();
    const item = list.find(c => c.complaint_id === id);
    if (item) {
      item.status = body.status;
      if (body.status === "Resolved") item.resolution_remarks = body.remarks;
      item.timeline = item.timeline || [];
      item.timeline.push({
        action_type: "STATUS_UPDATE",
        status: body.status,
        department: body.department || item.assigned_department,
        officer_name: body.officer_name || "Authorized Officer",
        remarks: body.remarks,
        timestamp: new Date().toISOString().replace("T", " ").substring(0, 19)
      });
      saveLocalStore(list);
      return makeJsonRes({ success: true, message: "Status updated successfully", complaint: item });
    }
  }

  // 7. Complaint Forward
  if (path.includes("/api/complaints/") && path.endsWith("/forward") && method === "POST") {
    const id = path.split("/").slice(-2, -1)[0];
    const body = JSON.parse(init.body || "{}");
    const list = getLocalStore();
    const item = list.find(c => c.complaint_id === id);
    if (item) {
      item.status = "Forwarded to Concerned Department";
      item.assigned_department = body.department;
      item.timeline = item.timeline || [];
      item.timeline.push({
        action_type: "FORWARDED",
        status: "Forwarded to Concerned Department",
        department: body.department,
        officer_name: body.officer_name || "Triage Officer",
        remarks: body.remarks,
        timestamp: new Date().toISOString().replace("T", " ").substring(0, 19)
      });
      saveLocalStore(list);
      return makeJsonRes({ success: true, message: `Forwarded to ${body.department}`, complaint: item });
    }
  }

  // 8. Citizen Feedback
  if (path.includes("/api/complaints/") && path.endsWith("/feedback") && method === "POST") {
    const id = path.split("/").slice(-2, -1)[0];
    const body = JSON.parse(init.body || "{}");
    const list = getLocalStore();
    const item = list.find(c => c.complaint_id === id);
    if (item) {
      item.citizen_rating = body.rating;
      item.citizen_feedback = body.feedback;
      saveLocalStore(list);
      return makeJsonRes({ success: true, message: "Rating recorded" });
    }
  }

  // 9. Get Single Complaint by ID
  if (path.includes("/api/complaints/") && method === "GET") {
    const id = path.split("/").pop();
    const list = getLocalStore();
    const item = list.find(c => c.complaint_id.toLowerCase() === id.toLowerCase());
    if (item) {
      return makeJsonRes({ success: true, complaint: item });
    }
    return makeJsonRes({ success: false, error: `Complaint ${id} not found` }, 404);
  }

  // 10. List or Create Complaints
  if (path.endsWith("/api/complaints")) {
    if (method === "POST") {
      const body = JSON.parse(init.body || "{}");
      const list = getLocalStore();
      const randDigits = Math.floor(10000 + Math.random() * 90000);
      const newId = `GOV-${new Date().getFullYear()}-${randDigits}`;
      const nowStr = new Date().toISOString().replace("T", " ").substring(0, 19);

      const newRecord = {
        complaint_id: newId,
        citizen_name: body.citizen_name || "Citizen",
        citizen_phone: body.citizen_phone || "",
        citizen_email: body.citizen_email || "",
        category: body.category || "General",
        subcategory: body.subcategory || "",
        subject: body.subject || "",
        description: body.description || "",
        state: body.state || "Delhi",
        district: body.district || "Central",
        pincode: body.pincode || "110001",
        incident_address: body.incident_address || "",
        incident_date: body.incident_date || nowStr.substring(0, 10),
        urgency: body.urgency || "Medium",
        status: "Submitted",
        assigned_department: body.category + " Redressal Cell",
        assigned_officer: "Triage Desk",
        created_at: nowStr,
        updated_at: nowStr,
        timeline: [
          { action_type: "SUBMITTED", status: "Submitted", department: "Citizen Portal", officer_name: "Citizen / Self", remarks: "Complaint registered in National Portal.", timestamp: nowStr }
        ],
        attachments: body.file_name ? [{ original_name: body.file_name, stored_filename: "doc.png", file_size: 150000 }] : []
      };

      list.unshift(newRecord);
      saveLocalStore(list);
      return makeJsonRes({ success: true, complaint_id: newId, message: "Registered successfully", status: "Submitted" }, 201);
    } else {
      // GET list with filters
      let list = getLocalStore();
      const status = parsedUrl.searchParams.get("status");
      const category = parsedUrl.searchParams.get("category");
      const urgency = parsedUrl.searchParams.get("urgency");
      const search = (parsedUrl.searchParams.get("search") || "").toLowerCase();

      if (status) list = list.filter(c => c.status === status);
      if (category) list = list.filter(c => c.category === category);
      if (urgency) list = list.filter(c => c.urgency === urgency);
      if (search) list = list.filter(c => 
        (c.complaint_id && c.complaint_id.toLowerCase().includes(search)) ||
        (c.citizen_name && c.citizen_name.toLowerCase().includes(search)) ||
        (c.subject && c.subject.toLowerCase().includes(search))
      );

      return makeJsonRes({ success: true, total: list.length, items: list });
    }
  }

  // Default fallback
  return originalFetch(input, init);
};

// Mobile Menu Toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".mobile-toggle");
  const nav = document.querySelector(".nav-links");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      nav.classList.toggle("open");
    });
  }

  // Load announcements ticker if element exists
  const ticker = document.getElementById("announcement-ticker");
  if (ticker) {
    fetch(`${API_BASE}/api/announcements`)
      .then(res => res.json())
      .then(data => {
        if (data.success && data.announcements.length > 0) {
          ticker.textContent = data.announcements[0].title + " — " + data.announcements[0].content;
        }
      })
      .catch(() => {});
  }
});
