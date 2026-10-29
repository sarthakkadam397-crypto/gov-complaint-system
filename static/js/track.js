/**
 * Complaint Tracking and Timeline Visualization Script
 */

const STANDARD_STAGES = [
  "Submitted",
  "Under Review",
  "Forwarded to Concerned Department",
  "In Progress",
  "Resolved"
];

document.addEventListener("DOMContentLoaded", () => {
  const trackBtn = document.getElementById("trackBtn");
  const trackInput = document.getElementById("trackInput");
  const phoneSearchBtn = document.getElementById("phoneSearchBtn");
  const phoneSearchInput = document.getElementById("phoneSearchInput");

  // Check URL query parameters for direct tracking
  const urlParams = new URLSearchParams(window.location.search);
  const directId = urlParams.get("id");
  if (directId) {
    if (trackInput) trackInput.value = directId;
    fetchAndRenderComplaint(directId);
  }

  if (trackBtn && trackInput) {
    trackBtn.addEventListener("click", () => {
      const id = trackInput.value.trim();
      if (!id) {
        showToast("Please enter a Complaint ID (e.g., GOV-2026-10492)", "error");
        return;
      }
      fetchAndRenderComplaint(id);
    });

    trackInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") trackBtn.click();
    });
  }

  if (phoneSearchBtn && phoneSearchInput) {
    phoneSearchBtn.addEventListener("click", () => {
      const phone = phoneSearchInput.value.trim();
      if (!phone || phone.length < 10) {
        showToast("Please enter a valid 10-digit mobile number", "error");
        return;
      }
      searchComplaintsByPhone(phone);
    });

    phoneSearchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") phoneSearchBtn.click();
    });
  }
});

async function fetchAndRenderComplaint(complaintId) {
  const container = document.getElementById("trackingResultContainer");
  const emptyState = document.getElementById("trackingEmptyState");
  const errorContainer = document.getElementById("trackingErrorContainer");

  if (!container) return;

  container.style.display = "none";
  if (errorContainer) errorContainer.style.display = "none";
  if (emptyState) emptyState.style.display = "none";

  try {
    const res = await fetch(`${API_BASE}/api/complaints/${encodeURIComponent(complaintId)}`);
    const data = await res.json();

    if (!data.success || !data.complaint) {
      if (errorContainer) {
        errorContainer.style.display = "block";
        document.getElementById("errorMessage").textContent =
          data.error || `No grievance record found with ID "${complaintId}". Please verify and retry.`;
      }
      return;
    }

    renderComplaintDetails(data.complaint);
    container.style.display = "block";
    container.scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    if (errorContainer) {
      errorContainer.style.display = "block";
      document.getElementById("errorMessage").textContent = "Unable to connect to grievance registry. Please try again.";
    }
  }
}

function renderComplaintDetails(c) {
  // Populate Header & Metadata
  document.getElementById("detailComplaintId").textContent = c.complaint_id;
  document.getElementById("detailStatusBadge").innerHTML = getStatusBadge(c.status);
  document.getElementById("detailUrgencyBadge").innerHTML = getUrgencyBadge(c.urgency);
  document.getElementById("detailCitizenName").textContent = c.citizen_name;
  document.getElementById("detailPhone").textContent = c.citizen_phone;
  document.getElementById("detailCategory").textContent = c.category;
  document.getElementById("detailSubcategory").textContent = c.subcategory || "General";
  document.getElementById("detailDate").textContent = formatDate(c.created_at);
  document.getElementById("detailAssignedDept").textContent = c.assigned_department || "Central Triage Cell";
  document.getElementById("detailAssignedOfficer").textContent = c.assigned_officer || "Officer on Duty";

  // Incident summary
  document.getElementById("detailSubject").textContent = c.subject;
  document.getElementById("detailDescription").textContent = c.description;
  document.getElementById("detailLocation").textContent = `${c.incident_address ? c.incident_address + ", " : ""}${c.district}, ${c.state} - ${c.pincode}`;

  // Attachments
  const attachmentBox = document.getElementById("detailAttachments");
  if (attachmentBox) {
    if (c.attachments && c.attachments.length > 0) {
      attachmentBox.innerHTML = c.attachments.map(att => `
        <div class="file-preview">
          <div>
            <strong>📎 ${att.original_name}</strong>
            <span style="font-size:0.75rem; color:#64748b; margin-left:8px;">(${formatFileSize(att.file_size)})</span>
          </div>
          <a href="/uploads/${att.stored_filename}" target="_blank" class="btn btn-sm btn-secondary">View / Download</a>
        </div>
      `).join("");
    } else {
      attachmentBox.innerHTML = `<p style="font-size:0.85rem; color:#64748b; font-style:italic;">No documentary evidence was uploaded with this complaint.</p>`;
    }
  }

  // Render Visual Timeline
  renderTimelineStepper(c.status, c.timeline || []);

  // Resolution Banner & Feedback Form
  const resolutionBox = document.getElementById("resolutionBox");
  if (resolutionBox) {
    if (c.status === "Resolved") {
      resolutionBox.style.display = "block";
      document.getElementById("resolutionNote").textContent = c.resolution_remarks || "Grievance has been resolved by the competent authority.";
      
      const feedbackSection = document.getElementById("feedbackSection");
      if (c.citizen_rating) {
        feedbackSection.innerHTML = `
          <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:16px; margin-top:14px;">
            <p style="color:#166534; font-weight:700;">★ Citizen Rating Submitted: ${c.citizen_rating} / 5 Stars</p>
            <p style="color:#15803d; font-size:0.88rem; margin-top:4px;">"${c.citizen_feedback || 'Resolved satisfactorily'}"</p>
          </div>
        `;
      } else {
        setupFeedbackForm(c.complaint_id);
      }
    } else {
      resolutionBox.style.display = "none";
    }
  }
}

function renderTimelineStepper(currentStatus, timelineEntries) {
  const container = document.getElementById("timelineStepper");
  if (!container) return;

  const currentIdx = STANDARD_STAGES.indexOf(currentStatus);
  const activeLevel = currentIdx >= 0 ? currentIdx : 0;

  let html = "";
  STANDARD_STAGES.forEach((stage, idx) => {
    let stepClass = "";
    let markerContent = idx + 1;

    if (idx < activeLevel || currentStatus === "Resolved") {
      stepClass = "completed";
      markerContent = "✓";
    } else if (idx === activeLevel) {
      stepClass = "active";
      markerContent = "●";
    }

    // Find latest matching timeline record for this stage
    const matchingLog = timelineEntries.slice().reverse().find(t => t.status.toLowerCase() === stage.toLowerCase());

    html += `
      <div class="timeline-step ${stepClass}">
        <div class="step-marker">${markerContent}</div>
        <div class="step-content">
          <div class="step-content-header">
            <span class="step-title">${stage}</span>
            <span class="step-time">${matchingLog ? formatDate(matchingLog.timestamp) : (stepClass ? "Pending" : "Awaiting")}</span>
          </div>
          ${matchingLog ? `
            <div class="step-dept">${matchingLog.department} &bull; ${matchingLog.officer_name}</div>
            <div class="step-remarks">${matchingLog.remarks}</div>
          ` : `
            <div class="step-remarks" style="color:#94a3b8; font-style:italic;">
              ${idx <= activeLevel ? "Processing step completed." : "Action will commence once preceding stages are fulfilled."}
            </div>
          `}
        </div>
      </div>
    `;
  });

  // Also include any intermediate timeline logs (e.g. forward logs) that might not match exact standard names
  container.innerHTML = html;
}

function setupFeedbackForm(complaintId) {
  const form = document.getElementById("feedbackForm");
  if (!form) return;

  let selectedRating = 5;
  const stars = document.querySelectorAll(".star-rating-btn");
  stars.forEach(btn => {
    btn.onclick = () => {
      selectedRating = parseInt(btn.dataset.val);
      stars.forEach(s => {
        s.style.color = parseInt(s.dataset.val) <= selectedRating ? "#eab308" : "#cbd5e1";
      });
    };
  });

  form.onsubmit = async (e) => {
    e.preventDefault();
    const comment = document.getElementById("feedbackComment").value.trim();

    try {
      const res = await fetch(`${API_BASE}/api/complaints/${complaintId}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rating: selectedRating, feedback: comment })
      });
      const data = await res.json();
      if (data.success) {
        showToast("Citizen satisfaction rating saved. Thank you!", "success");
        fetchAndRenderComplaint(complaintId);
      }
    } catch (err) {
      showToast("Error submitting feedback", "error");
    }
  };
}

async function searchComplaintsByPhone(phone) {
  const phoneResultsBox = document.getElementById("phoneResultsList");
  if (!phoneResultsBox) return;

  phoneResultsBox.innerHTML = "<p>Searching registered complaints for mobile number...</p>";

  try {
    const res = await fetch(`${API_BASE}/api/search-phone?phone=${encodeURIComponent(phone)}`);
    const data = await res.json();

    if (!data.success || !data.complaints || data.complaints.length === 0) {
      phoneResultsBox.innerHTML = `<p style="color:#dc2626; padding:10px;">No complaints found associated with mobile number +91 ${phone}.</p>`;
      return;
    }

    phoneResultsBox.innerHTML = `
      <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; margin-top:16px;">
        <h4 style="margin-bottom:12px; color:#0a2540;">Found ${data.complaints.length} complaint(s) for +91 ${phone}:</h4>
        <div style="display:flex; flex-direction:column; gap:10px;">
          ${data.complaints.map(item => `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:10px; border-bottom:1px solid #f1f5f9;">
              <div>
                <strong style="color:#1e40af; font-family:monospace;">${item.complaint_id}</strong>
                <span style="margin:0 8px; color:#64748b;">•</span>
                <span>${item.category}</span>
                <p style="font-size:0.85rem; color:#475569; margin-top:2px;">${item.subject}</p>
              </div>
              <div style="display:flex; align-items:center; gap:10px;">
                ${getStatusBadge(item.status)}
                <button onclick="fetchAndRenderComplaint('${item.complaint_id}')" class="btn btn-sm btn-primary">Track</button>
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  } catch (err) {
    phoneResultsBox.innerHTML = "<p style='color:#dc2626;'>Error connecting to registry.</p>";
  }
}
