/**
 * Administrative Dashboard Client Logic
 */

let authToken = localStorage.getItem("gov_cms_token");
let currentUser = null;
try {
  currentUser = JSON.parse(localStorage.getItem("gov_cms_user"));
} catch (e) {}

let allDepartments = [];
let allCategories = [];

document.addEventListener("DOMContentLoaded", () => {
  initMetadata();
  checkAuth();
  setupEventListeners();
});

async function initMetadata() {
  try {
    const res = await fetch(`${API_BASE}/api/meta`);
    const data = await res.json();
    if (data.success) {
      allDepartments = data.departments;
      allCategories = data.categories;
      populateFilterDropdowns();
    }
  } catch (e) {}
}

function checkAuth() {
  const loginSection = document.getElementById("adminLoginSection");
  const dashboardSection = document.getElementById("adminDashboardSection");

  if (authToken && currentUser) {
    if (loginSection) loginSection.style.display = "none";
    if (dashboardSection) dashboardSection.style.display = "flex";
    renderUserProfile();
    loadDashboardStats();
    loadComplaints();
  } else {
    if (loginSection) loginSection.style.display = "block";
    if (dashboardSection) dashboardSection.style.display = "none";
  }
}

function renderUserProfile() {
  if (!currentUser) return;
  const nameEl = document.getElementById("profileFullName");
  const roleEl = document.getElementById("profileRole");
  const deptEl = document.getElementById("profileDepartment");

  if (nameEl) nameEl.textContent = currentUser.full_name;
  if (roleEl) roleEl.textContent = currentUser.role.toUpperCase() + (currentUser.badge_number ? ` (${currentUser.badge_number})` : "");
  if (deptEl) deptEl.textContent = currentUser.department || "General Public Grievances";
}

function setupEventListeners() {
  // Login Form
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const u = document.getElementById("loginUsername").value.trim();
      const p = document.getElementById("loginPassword").value.trim();
      performLogin(u, p);
    });
  }

  // Logout
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.removeItem("gov_cms_token");
      localStorage.removeItem("gov_cms_user");
      authToken = null;
      currentUser = null;
      checkAuth();
      showToast("Logged out successfully.", "info");
    });
  }

  // Filter toolbar triggers
  const filterStatus = document.getElementById("filterStatus");
  const filterCategory = document.getElementById("filterCategory");
  const filterUrgency = document.getElementById("filterUrgency");
  const searchInput = document.getElementById("searchComplaintsInput");
  const resetBtn = document.getElementById("resetFiltersBtn");

  if (filterStatus) filterStatus.addEventListener("change", () => loadComplaints());
  if (filterCategory) filterCategory.addEventListener("change", () => loadComplaints());
  if (filterUrgency) filterUrgency.addEventListener("change", () => loadComplaints());

  let debounceTimer;
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => loadComplaints(), 300);
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      if (filterStatus) filterStatus.value = "";
      if (filterCategory) filterCategory.value = "";
      if (filterUrgency) filterUrgency.value = "";
      if (searchInput) searchInput.value = "";
      loadComplaints();
    });
  }
}

async function performLogin(username, password) {
  try {
    const res = await fetch(`${API_BASE}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (data.success) {
      authToken = data.token;
      currentUser = data.user;
      localStorage.setItem("gov_cms_token", authToken);
      localStorage.setItem("gov_cms_user", JSON.stringify(currentUser));
      showToast(data.message, "success");
      checkAuth();
    } else {
      showToast(data.error || "Login failed", "error");
    }
  } catch (err) {
    showToast("Server error during login", "error");
  }
}

// Convenient Demo Login Shortcut
function quickLogin(username, password) {
  document.getElementById("loginUsername").value = username;
  document.getElementById("loginPassword").value = password;
  performLogin(username, password);
}

function populateFilterDropdowns() {
  const catFilter = document.getElementById("filterCategory");
  if (catFilter) {
    allCategories.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c;
      opt.textContent = c;
      catFilter.appendChild(opt);
    });
  }

  const forwardDeptSelect = document.getElementById("forwardDeptSelect");
  if (forwardDeptSelect) {
    forwardDeptSelect.innerHTML = `<option value="">-- Choose Department --</option>`;
    allDepartments.forEach(d => {
      const opt = document.createElement("option");
      opt.value = d.name;
      opt.textContent = `${d.name} (${d.head})`;
      forwardDeptSelect.appendChild(opt);
    });
  }
}

async function loadDashboardStats() {
  try {
    const res = await fetch(`${API_BASE}/api/stats`);
    const data = await res.json();
    if (data.success && data.stats) {
      const s = data.stats;
      document.getElementById("statTotalComplaints").textContent = s.total;
      document.getElementById("statPending").textContent = s.pending;
      document.getElementById("statInProgress").textContent = s.in_progress;
      document.getElementById("statResolved").textContent = s.resolved;
      document.getElementById("statResolutionRate").textContent = s.resolution_rate + "%";
    }
  } catch (e) {}
}

async function loadComplaints() {
  const tbody = document.getElementById("complaintsTableBody");
  if (!tbody) return;

  tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:20px; color:#64748b;">Loading registered grievances...</td></tr>`;

  const status = document.getElementById("filterStatus")?.value || "";
  const category = document.getElementById("filterCategory")?.value || "";
  const urgency = document.getElementById("filterUrgency")?.value || "";
  const search = document.getElementById("searchComplaintsInput")?.value || "";

  const queryParams = new URLSearchParams();
  if (status) queryParams.append("status", status);
  if (category) queryParams.append("category", category);
  if (urgency) queryParams.append("urgency", urgency);
  if (search) queryParams.append("search", search);
  queryParams.append("limit", "100");

  try {
    const res = await fetch(`${API_BASE}/api/complaints?${queryParams.toString()}`);
    const data = await res.json();

    if (!data.success || !data.items || data.items.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:30px; color:#64748b;">No complaints found matching current filter criteria.</td></tr>`;
      return;
    }

    tbody.innerHTML = data.items.map(c => `
      <tr>
        <td class="complaint-cell-id">${c.complaint_id}</td>
        <td>
          <div style="font-weight:600;">${c.citizen_name}</div>
          <div style="font-size:0.78rem; color:#64748b;">📱 ${c.citizen_phone}</div>
        </td>
        <td>
          <div style="font-weight:600; font-size:0.85rem;">${c.category}</div>
          <div style="font-size:0.8rem; color:#475569; max-width:280px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${c.subject}</div>
        </td>
        <td>${getUrgencyBadge(c.urgency)}</td>
        <td>${getStatusBadge(c.status)}</td>
        <td style="font-size:0.82rem; color:#334155;">${c.assigned_department || 'Triage Cell'}</td>
        <td>
          <div class="table-actions">
            <button onclick="openAuditModal('${c.complaint_id}')" class="btn btn-sm btn-secondary" title="View Full Details">Audit</button>
            <button onclick="openStatusModal('${c.complaint_id}', '${c.status}')" class="btn btn-sm btn-primary" title="Update Status">Update</button>
            <button onclick="openForwardModal('${c.complaint_id}')" class="btn btn-sm btn-saffron" title="Forward to Another Department">Forward</button>
          </div>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:#dc2626;">Error retrieving complaint data.</td></tr>`;
  }
}

// ------------------- AUDIT / VIEW MODAL -------------------
async function openAuditModal(complaintId) {
  try {
    const res = await fetch(`${API_BASE}/api/complaints/${complaintId}`);
    const data = await res.json();
    if (!data.success) return showToast("Could not load details", "error");

    const c = data.complaint;
    document.getElementById("auditModalId").textContent = c.complaint_id;
    document.getElementById("auditCitizen").textContent = `${c.citizen_name} (${c.citizen_phone}) ${c.citizen_email ? '| ' + c.citizen_email : ''}`;
    document.getElementById("auditSubject").textContent = c.subject;
    document.getElementById("auditDesc").textContent = c.description;
    document.getElementById("auditLocation").textContent = `${c.incident_address || ''}, ${c.district}, ${c.state} - ${c.pincode}`;
    document.getElementById("auditStatus").innerHTML = getStatusBadge(c.status) + " " + getUrgencyBadge(c.urgency);

    // Audit logs timeline
    const auditTimeline = document.getElementById("auditTimelineList");
    if (auditTimeline) {
      auditTimeline.innerHTML = (c.timeline || []).map(t => `
        <div style="border-left: 3px solid #2563eb; padding-left: 12px; margin-bottom: 14px;">
          <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:#64748b;">
            <strong>${t.action_type} &bull; ${t.status}</strong>
            <span>${formatDate(t.timestamp)}</span>
          </div>
          <div style="font-size:0.85rem; color:#0f172a; margin-top:2px;">${t.remarks}</div>
          <div style="font-size:0.75rem; color:#475569;">By: ${t.officer_name} (${t.department})</div>
        </div>
      `).join("");
    }

    document.getElementById("auditModal").classList.add("active");
  } catch (e) {
    showToast("Error opening modal", "error");
  }
}

function closeAuditModal() {
  document.getElementById("auditModal").classList.remove("active");
}

// ------------------- STATUS UPDATE MODAL -------------------
let currentActionComplaintId = null;

function openStatusModal(complaintId, currentStatus) {
  currentActionComplaintId = complaintId;
  document.getElementById("statusModalId").textContent = complaintId;
  document.getElementById("modalStatusSelect").value = currentStatus;
  document.getElementById("modalRemarks").value = "";
  document.getElementById("statusModal").classList.add("active");
}

function closeStatusModal() {
  document.getElementById("statusModal").classList.remove("active");
}

async function submitStatusUpdate() {
  if (!currentActionComplaintId) return;

  const newStatus = document.getElementById("modalStatusSelect").value;
  const remarks = document.getElementById("modalRemarks").value.trim();

  if (!remarks) {
    showToast("Please enter official remarks explaining this status change.", "error");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/complaints/${currentActionComplaintId}/status`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        status: newStatus,
        remarks: remarks,
        officer_name: currentUser ? currentUser.full_name : "Authorized Officer",
        department: currentUser ? currentUser.department : "Central Grievance Redressal"
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast("Complaint status updated successfully!", "success");
      closeStatusModal();
      loadDashboardStats();
      loadComplaints();
    } else {
      showToast(data.error || "Update failed", "error");
    }
  } catch (e) {
    showToast("Server error during update", "error");
  }
}

// ------------------- FORWARD MODAL -------------------
function openForwardModal(complaintId) {
  currentActionComplaintId = complaintId;
  document.getElementById("forwardModalId").textContent = complaintId;
  document.getElementById("forwardDeptSelect").value = "";
  document.getElementById("forwardRemarks").value = "";
  document.getElementById("forwardModal").classList.add("active");
}

function closeForwardModal() {
  document.getElementById("forwardModal").classList.remove("active");
}

async function submitForward() {
  if (!currentActionComplaintId) return;

  const targetDept = document.getElementById("forwardDeptSelect").value;
  const remarks = document.getElementById("forwardRemarks").value.trim();

  if (!targetDept) {
    showToast("Please select the target department.", "error");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/complaints/${currentActionComplaintId}/forward`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        department: targetDept,
        remarks: remarks || "Forwarded for field inspection and statutory resolution.",
        officer_name: currentUser ? currentUser.full_name : "Central Triage Desk"
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Complaint forwarded to ${targetDept}`, "success");
      closeForwardModal();
      loadDashboardStats();
      loadComplaints();
    } else {
      showToast(data.error || "Forwarding failed", "error");
    }
  } catch (e) {
    showToast("Server error during forward", "error");
  }
}
