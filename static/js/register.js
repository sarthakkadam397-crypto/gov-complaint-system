/**
 * Complaint Registration Client Script
 * Handles category selection, file upload base64 encoding, validation, and submission modal.
 */

let selectedFileBase64 = null;
let selectedFileName = null;
let selectedFileSize = 0;

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("complaintForm");
  const categorySelect = document.getElementById("categorySelect");
  const fileInput = document.getElementById("fileInput");
  const dropzone = document.getElementById("fileDropzone");
  const filePreview = document.getElementById("filePreview");
  const removeFileBtn = document.getElementById("removeFileBtn");

  // Pre-select category if passed in URL query param
  const urlParams = new URLSearchParams(window.location.search);
  const paramCategory = urlParams.get("category");
  if (paramCategory && categorySelect) {
    for (let opt of categorySelect.options) {
      if (opt.value.toLowerCase() === paramCategory.toLowerCase()) {
        opt.selected = true;
        break;
      }
    }
  }

  // File Dropzone Event Listeners
  if (dropzone && fileInput) {
    dropzone.addEventListener("click", () => fileInput.click());

    dropzone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    });

    dropzone.addEventListener("dragleave", () => {
      dropzone.classList.remove("dragover");
    });

    dropzone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        handleFileSelection(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener("change", (e) => {
      if (e.target.files && e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
      }
    });
  }

  if (removeFileBtn) {
    removeFileBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      clearSelectedFile();
    });
  }

  // Handle Form Submission
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const citizen_name = document.getElementById("citizenName").value.trim();
      const citizen_phone = document.getElementById("citizenPhone").value.trim();
      const citizen_email = document.getElementById("citizenEmail").value.trim();
      const citizen_aadhaar = document.getElementById("citizenAadhaar").value.trim();
      const category = document.getElementById("categorySelect").value;
      const subcategory = document.getElementById("subCategory").value.trim();
      const urgency = document.getElementById("urgencySelect").value;
      const subject = document.getElementById("complaintSubject").value.trim();
      const description = document.getElementById("complaintDescription").value.trim();
      const incident_date = document.getElementById("incidentDate").value;
      const incident_address = document.getElementById("incidentAddress").value.trim();
      const state = document.getElementById("stateSelect").value;
      const district = document.getElementById("districtInput").value.trim();
      const pincode = document.getElementById("pincodeInput").value.trim();

      // Validation
      if (!citizen_name || !citizen_phone || !category || !subject || !description) {
        showToast("Please fill in all required fields indicated with (*)", "error");
        return;
      }

      if (citizen_phone.length < 10) {
        showToast("Please enter a valid 10-digit mobile number", "error");
        return;
      }

      const submitBtn = document.getElementById("submitBtn");
      submitBtn.disabled = true;
      submitBtn.innerHTML = "Submitting to National Registry...";

      const payload = {
        citizen_name,
        citizen_phone,
        citizen_email,
        citizen_aadhaar_last4: citizen_aadhaar,
        category,
        subcategory,
        urgency,
        subject,
        description,
        incident_date,
        incident_address,
        state,
        district,
        pincode,
        file_data: selectedFileBase64,
        file_name: selectedFileName
      };

      try {
        const response = await fetch(`${API_BASE}/api/complaints`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        const result = await response.json();
        submitBtn.disabled = false;
        submitBtn.innerHTML = "Submit Official Grievance";

        if (result.success) {
          showSuccessModal(result.complaint_id, citizen_name, category, subject);
          form.reset();
          clearSelectedFile();
        } else {
          showToast(result.error || "Failed to submit complaint.", "error");
        }
      } catch (err) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = "Submit Official Grievance";
        showToast("Server communication error. Please try again.", "error");
      }
    });
  }
});

function handleFileSelection(file) {
  // Max 10MB
  if (file.size > 10 * 1024 * 1024) {
    showToast("File exceeds maximum allowed size of 10 MB", "error");
    return;
  }

  const reader = new FileReader();
  reader.onload = (event) => {
    selectedFileBase64 = event.target.result;
    selectedFileName = file.name;
    selectedFileSize = file.size;

    const preview = document.getElementById("filePreview");
    const filenameLabel = document.getElementById("fileNameLabel");
    const filesizeLabel = document.getElementById("fileSizeLabel");
    const dropzoneContent = document.getElementById("dropzoneContent");

    if (preview && filenameLabel && filesizeLabel) {
      filenameLabel.textContent = file.name;
      filesizeLabel.textContent = formatFileSize(file.size);
      preview.style.display = "flex";
      if (dropzoneContent) dropzoneContent.style.display = "none";
    }
  };
  reader.readAsDataURL(file);
}

function clearSelectedFile() {
  selectedFileBase64 = null;
  selectedFileName = null;
  selectedFileSize = 0;

  const fileInput = document.getElementById("fileInput");
  if (fileInput) fileInput.value = "";

  const preview = document.getElementById("filePreview");
  const dropzoneContent = document.getElementById("dropzoneContent");
  if (preview) preview.style.display = "none";
  if (dropzoneContent) dropzoneContent.style.display = "block";
}

function showSuccessModal(complaintId, name, category, subject) {
  const modal = document.getElementById("successModal");
  if (!modal) return;

  document.getElementById("modalComplaintId").textContent = complaintId;
  document.getElementById("modalCitizenName").textContent = name;
  document.getElementById("modalCategory").textContent = category;
  document.getElementById("modalSubject").textContent = subject;

  const trackBtn = document.getElementById("modalTrackBtn");
  if (trackBtn) {
    trackBtn.onclick = () => {
      window.location.href = `track.html?id=${complaintId}`;
    };
  }

  const copyBtn = document.getElementById("modalCopyBtn");
  if (copyBtn) {
    copyBtn.onclick = () => {
      navigator.clipboard.writeText(complaintId);
      showToast("Complaint ID copied to clipboard!", "success");
    };
  }

  modal.classList.add("active");
}

function closeModal() {
  const modal = document.getElementById("successModal");
  if (modal) modal.classList.remove("active");
}
