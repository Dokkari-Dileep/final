/**
 * Multi-Crop Disease Detection System - Main JavaScript
 * Handles file uploads, camera capture, predictions, and feedback form
 */

document.addEventListener("DOMContentLoaded", function () {
  // Initialize EmailJS
  if (typeof emailjs !== "undefined") {
    const emailjsUserId = document.body.getAttribute("data-emailjs-user-id");
    if (emailjsUserId) {
      emailjs.init(emailjsUserId);
      console.log("EmailJS initialized");
    }
  }

  // Global variables
  let currentStream = null;
  let capturedImage = null;
  let currentPrediction = null;

  // Initialize page based on current URL
  initializePage();

  // Set up event listeners
  setupEventListeners();

  // Update copyright year
  updateCopyrightYear();
});

/**
 * Initialize page-specific functionality
 */
function initializePage() {
  const path = window.location.pathname;

  if (path === "/" || path === "/index.html") {
    initializeHomePage();
  } else if (path.includes("feedback")) {
    initializeFeedbackPage();
  } else if (path.includes("dataset")) {
    initializeDatasetPage();
  } else if (path.includes("tutorial")) {
    initializeTutorialPage();
  }
}

/**
 * Initialize home page functionality
 */
function initializeHomePage() {
  console.log("Initializing home page...");

  // Check if browser supports camera
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    document.getElementById("cameraBtn").style.display = "none";
    showAlert(
      "warning",
      "Camera access not supported by your browser. Please upload images instead."
    );
  }

  // Setup drag and drop
  setupDragAndDrop();

  // Setup image preview
  setupImagePreview();

  // Update supported crops display
  updateSupportedCrops();
}

/**
 * Initialize feedback page functionality
 */
function initializeFeedbackPage() {
  console.log("Initializing feedback page...");

  // Setup form validation
  setupFormValidation();

  // Setup form submission
  setupFeedbackSubmission();
}

/**
 * Initialize dataset page functionality
 */
function initializeDatasetPage() {
  console.log("Initializing dataset page...");

  // Animate stats counters
  animateStatsCounters();

  // Setup disease search
  setupDiseaseSearch();
}

/**
 * Initialize tutorial page functionality
 */
function initializeTutorialPage() {
  console.log("Initializing tutorial page...");

  // Setup video player
  setupVideoPlayer();

  // Setup accordion interactions
  setupAccordion();
}

/**
 * Setup all event listeners
 */
function setupEventListeners() {
  // File upload
  const fileUpload = document.getElementById("imageUpload");
  if (fileUpload) {
    fileUpload.addEventListener("change", handleFileUpload);
  }

  // Camera buttons
  const cameraBtn = document.getElementById("cameraBtn");
  if (cameraBtn) {
    cameraBtn.addEventListener("click", openCamera);
  }

  const captureBtn = document.getElementById("captureBtn");
  if (captureBtn) {
    captureBtn.addEventListener("click", captureImage);
  }

  const closeCameraBtn = document.getElementById("closeCameraBtn");
  if (closeCameraBtn) {
    closeCameraBtn.addEventListener("click", closeCamera);
  }

  // Prediction button
  const predictBtn = document.getElementById("predictBtn");
  if (predictBtn) {
    predictBtn.addEventListener("click", predictDisease);
  }

  // New detection button
  const newDetectionBtn = document.getElementById("newDetectionBtn");
  if (newDetectionBtn) {
    newDetectionBtn.addEventListener("click", startNewDetection);
  }

  // Print button
  const printBtn = document.getElementById("printBtn");
  if (printBtn) {
    printBtn.addEventListener("click", printResults);
  }

  // Feedback form
  const feedbackForm = document.getElementById("feedbackForm");
  if (feedbackForm) {
    feedbackForm.addEventListener("submit", handleFeedbackSubmit);
  }

  // Mobile menu toggle
  const navbarToggler = document.querySelector(".navbar-toggler");
  if (navbarToggler) {
    navbarToggler.addEventListener("click", function () {
      document.querySelector(".navbar-collapse").classList.toggle("show");
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;

      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Handle window resize
  window.addEventListener("resize", handleWindowResize);

  // Handle scroll for navbar
  window.addEventListener("scroll", handleScroll);
}

/**
 * Setup drag and drop functionality
 */
function setupDragAndDrop() {
  const uploadArea = document.getElementById("uploadArea");
  if (!uploadArea) return;

  uploadArea.addEventListener("dragover", function (e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.add("dragover");
    this.style.borderColor = "#155724";
    this.style.backgroundColor = "rgba(40, 167, 69, 0.1)";
  });

  uploadArea.addEventListener("dragleave", function (e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove("dragover");
    this.style.borderColor = "#28a745";
    this.style.backgroundColor = "rgba(255, 255, 255, 0.95)";
  });

  uploadArea.addEventListener("drop", function (e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove("dragover");
    this.style.borderColor = "#28a745";
    this.style.backgroundColor = "rgba(255, 255, 255, 0.95)";

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file && file.type.startsWith("image/")) {
        if (file.size > 16 * 1024 * 1024) {
          showAlert("error", "File size must be less than 16MB");
          return;
        }
        handleImageFile(file);
      } else {
        showAlert("error", "Please drop an image file (JPG, PNG, JPEG, GIF)");
      }
    }
  });
}

/**
 * Setup image preview functionality
 */
function setupImagePreview() {
  const previewImage = document.getElementById("previewImage");
  if (previewImage) {
    previewImage.addEventListener("error", function () {
      this.src = "/static/images/placeholder.jpg";
      showAlert("warning", "Failed to load image preview");
    });
  }
}

/**
 * Handle file upload
 */
function handleFileUpload(e) {
  const file = e.target.files[0];
  if (file) {
    if (file.size > 16 * 1024 * 1024) {
      showAlert("error", "File size must be less than 16MB");
      return;
    }
    handleImageFile(file);
  }
}

/**
 * Handle image file
 */
function handleImageFile(file) {
  const reader = new FileReader();

  reader.onload = function (event) {
    document.getElementById("previewImage").src = event.target.result;
    document.getElementById("imagePreview").style.display = "block";
    document.getElementById("cameraPreview").style.display = "none";
    document.getElementById("uploadArea").style.display = "none";
    capturedImage = file;

    // Reset any previous results
    document.getElementById("resultSection").style.display = "none";
    document.getElementById("loadingSpinner").style.display = "none";
  };

  reader.onerror = function () {
    showAlert("error", "Failed to read image file");
  };

  reader.readAsDataURL(file);
}

/**
 * Open camera for image capture
 */
async function openCamera() {
  try {
    const constraints = {
      video: {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        facingMode: "environment",
      },
    };

    currentStream = await navigator.mediaDevices.getUserMedia(constraints);
    const videoElement = document.getElementById("cameraStream");
    videoElement.srcObject = currentStream;

    document.getElementById("cameraPreview").style.display = "block";
    document.getElementById("uploadArea").style.display = "none";
    document.getElementById("imagePreview").style.display = "none";

    showAlert("success", 'Camera activated. Click "Capture" to take a photo.');
  } catch (error) {
    console.error("Error accessing camera:", error);
    showAlert(
      "error",
      `Camera error: ${error.message}. Please allow camera access.`
    );
  }
}

/**
 * Capture image from camera
 */
function captureImage() {
  const video = document.getElementById("cameraStream");
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob(
    function (blob) {
      capturedImage = new File([blob], `capture_${Date.now()}.jpg`, {
        type: "image/jpeg",
        lastModified: Date.now(),
      });

      // Display preview
      const previewUrl = URL.createObjectURL(blob);
      document.getElementById("previewImage").src = previewUrl;
      document.getElementById("imagePreview").style.display = "block";
      document.getElementById("cameraPreview").style.display = "none";

      // Close camera stream
      closeCamera();

      // Clean up URL object later
      setTimeout(() => URL.revokeObjectURL(previewUrl), 1000);
    },
    "image/jpeg",
    0.9
  );
}

/**
 * Close camera
 */
function closeCamera() {
  if (currentStream) {
    currentStream.getTracks().forEach((track) => track.stop());
    currentStream = null;
  }
  document.getElementById("cameraPreview").style.display = "none";
  document.getElementById("uploadArea").style.display = "block";
}

/**
 * Predict disease from captured/uploaded image
 */
async function predictDisease() {
  if (!capturedImage) {
    showAlert("warning", "Please select or capture an image first");
    return;
  }

  // Show loading
  document.getElementById("imagePreview").style.display = "none";
  document.getElementById("loadingSpinner").style.display = "flex";

  // Create form data
  const formData = new FormData();
  formData.append("file", capturedImage);

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    // Hide loading
    document.getElementById("loadingSpinner").style.display = "none";

    if (data.success) {
      currentPrediction = data;
      displayResults(data);
    } else {
      showAlert("error", data.error || "Failed to detect disease");
      startNewDetection();
    }
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("loadingSpinner").style.display = "none";
    showAlert(
      "error",
      "Network error. Please check your connection and try again."
    );
    startNewDetection();
  }
}

/**
 * Display prediction results
 */
function displayResults(data) {
  // Update disease info
  document.getElementById("diseaseName").textContent = formatDiseaseName(
    data.disease
  );
  document.getElementById(
    "confidenceScore"
  ).textContent = `${data.confidence}%`;
  document.getElementById("diseaseDescription").textContent = data.description;

  // Update confidence meter
  const confidenceFill = document.getElementById("confidenceFill");
  confidenceFill.style.width = `${data.confidence}%`;

  // Update confidence color based on percentage
  if (data.confidence >= 90) {
    confidenceFill.style.background =
      "linear-gradient(90deg, #4CAF50, #8BC34A)";
  } else if (data.confidence >= 70) {
    confidenceFill.style.background =
      "linear-gradient(90deg, #FFC107, #FF9800)";
  } else {
    confidenceFill.style.background =
      "linear-gradient(90deg, #F44336, #FF5722)";
  }

  // Update lists
  updateList("diseaseCauses", data.causes);
  updateList("diseasePreventions", data.preventions);
  updateList("diseaseTreatments", data.treatments);
  updateList("organicRemedies", data.organic_remedies);
  updateList("chemicalControls", data.chemical_controls);

  // Show results with animation
  const resultSection = document.getElementById("resultSection");
  resultSection.style.display = "block";
  resultSection.classList.add("fade-in");

  // Scroll to results
  resultSection.scrollIntoView({ behavior: "smooth", block: "start" });

  // Log prediction for analytics
  logPrediction(data);
}

/**
 * Update list items
 */
function updateList(elementId, items) {
  const element = document.getElementById(elementId);
  if (!element) return;

  element.innerHTML = "";

  if (items && Array.isArray(items) && items.length > 0) {
    items.forEach((item) => {
      if (item && item.trim()) {
        const li = document.createElement("li");
        li.textContent = item;
        element.appendChild(li);
      }
    });
  } else {
    const li = document.createElement("li");
    li.textContent = "Information not available";
    li.classList.add("text-muted");
    element.appendChild(li);
  }
}

/**
 * Format disease name for display
 */
function formatDiseaseName(disease) {
  return disease
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase())
    .replace(/\b(And|Or|The|Of|In|On|At|To|For)\b/g, (word) =>
      word.toLowerCase()
    );
}

/**
 * Start new detection
 */
function startNewDetection() {
  document.getElementById("resultSection").style.display = "none";
  document.getElementById("imagePreview").style.display = "none";
  document.getElementById("uploadArea").style.display = "block";
  document.getElementById("imageUpload").value = "";
  capturedImage = null;
  currentPrediction = null;

  // Reset camera if active
  closeCamera();
}

/**
 * Print results
 */
function printResults() {
  window.print();
}

/**
 * Setup form validation
 */
function setupFormValidation() {
  const form = document.getElementById("feedbackForm");
  if (!form) return;

  const fields = form.querySelectorAll("[required]");
  fields.forEach((field) => {
    field.addEventListener("blur", validateField);
    field.addEventListener("input", validateField);
  });

  // Email validation
  const emailField = document.getElementById("email");
  if (emailField) {
    emailField.addEventListener("blur", validateEmail);
  }

  // Phone validation
  const phoneField = document.getElementById("phone");
  if (phoneField) {
    phoneField.addEventListener("blur", validatePhone);
  }
}

/**
 * Validate individual field
 */
function validateField(e) {
  const field = e.target;
  const value = field.value.trim();

  if (field.hasAttribute("required") && !value) {
    field.classList.add("is-invalid");
    field.classList.remove("is-valid");
    showFieldError(field, "This field is required");
  } else {
    field.classList.remove("is-invalid");
    field.classList.add("is-valid");
    hideFieldError(field);
  }
}

/**
 * Validate email field
 */
function validateEmail(e) {
  const field = e.target;
  const email = field.value.trim();
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (email && !emailRegex.test(email)) {
    field.classList.add("is-invalid");
    field.classList.remove("is-valid");
    showFieldError(field, "Please enter a valid email address");
  } else if (email) {
    field.classList.remove("is-invalid");
    field.classList.add("is-valid");
    hideFieldError(field);
  }
}

/**
 * Validate phone field
 */
function validatePhone(e) {
  const field = e.target;
  const phone = field.value.trim();
  const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;

  if (phone && !phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ""))) {
    field.classList.add("is-invalid");
    field.classList.remove("is-valid");
    showFieldError(field, "Please enter a valid phone number");
  } else if (phone) {
    field.classList.remove("is-invalid");
    field.classList.add("is-valid");
    hideFieldError(field);
  }
}

/**
 * Show field error
 */
function showFieldError(field, message) {
  let errorDiv = field.parentNode.querySelector(".invalid-feedback");
  if (!errorDiv) {
    errorDiv = document.createElement("div");
    errorDiv.className = "invalid-feedback";
    field.parentNode.appendChild(errorDiv);
  }
  errorDiv.textContent = message;
}

/**
 * Hide field error
 */
function hideFieldError(field) {
  const errorDiv = field.parentNode.querySelector(".invalid-feedback");
  if (errorDiv) {
    errorDiv.remove();
  }
}

/**
 * Setup feedback submission
 */
function setupFeedbackSubmission() {
  const form = document.getElementById("feedbackForm");
  if (!form) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // Validate all fields
    const isValid = validateForm();
    if (!isValid) {
      showAlert("warning", "Please fix the errors in the form");
      return;
    }

    // Get form data
    const formData = {
      name: document.getElementById("name").value.trim(),
      email: document.getElementById("email").value.trim(),
      phone: document.getElementById("phone").value.trim() || "Not provided",
      subject: document.getElementById("subject").value,
      message: document.getElementById("message").value.trim(),
      newsletter: document.getElementById("newsletter").checked,
    };

    // Show loading
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML =
      '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
    submitBtn.disabled = true;

    try {
      // Send to backend
      const response = await fetch("/feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams(formData),
      });

      if (response.ok) {
        // Send via EmailJS if available
        if (typeof emailjs !== "undefined") {
          try {
            await emailjs.send(emailjsServiceId, emailjsTemplateId, {
              from_name: formData.name,
              from_email: formData.email,
              phone: formData.phone,
              subject: formData.subject,
              message: formData.message,
              to_email: adminEmail,
              timestamp: new Date().toLocaleString(),
            });
          } catch (emailError) {
            console.warn("EmailJS failed:", emailError);
            // Continue anyway since backend already saved it
          }
        }

        showAlert(
          "success",
          "Thank you for your feedback! We will contact you soon."
        );
        form.reset();
        form.classList.remove("was-validated");

        // Reset validation states
        form.querySelectorAll(".is-valid, .is-invalid").forEach((el) => {
          el.classList.remove("is-valid", "is-invalid");
        });
      } else {
        throw new Error("Server error");
      }
    } catch (error) {
      console.error("Error:", error);
      showAlert(
        "error",
        "Sorry, there was an error sending your message. Please try again."
      );
    } finally {
      // Reset button
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  });
}

/**
 * Validate entire form
 */
function validateForm() {
  const form = document.getElementById("feedbackForm");
  let isValid = true;

  const requiredFields = form.querySelectorAll("[required]");
  requiredFields.forEach((field) => {
    const value = field.value.trim();
    if (!value) {
      field.classList.add("is-invalid");
      showFieldError(field, "This field is required");
      isValid = false;
    } else {
      field.classList.remove("is-invalid");
      field.classList.add("is-valid");
      hideFieldError(field);
    }
  });

  // Validate email
  const emailField = document.getElementById("email");
  if (emailField && emailField.value.trim()) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailField.value.trim())) {
      emailField.classList.add("is-invalid");
      showFieldError(emailField, "Please enter a valid email address");
      isValid = false;
    }
  }

  return isValid;
}

/**
 * Handle feedback form submission
 */
async function handleFeedbackSubmit(e) {
  e.preventDefault();

  if (!validateForm()) {
    showAlert("warning", "Please fill in all required fields correctly");
    return;
  }

  // Implementation continues from setupFeedbackSubmission
  // This is a wrapper for the actual submission logic
}

/**
 * Update supported crops display
 */
function updateSupportedCrops() {
  const cropsContainer = document.getElementById("supportedCrops");
  if (!cropsContainer) return;

  const crops = [
    "Apple",
    "Tomato",
    "Potato",
    "Grape",
    "Corn",
    "Cherry",
    "Strawberry",
    "Peach",
    "Pepper",
    "Watermelon",
    "Pomegranate",
    "Eggplant",
    "Custard Apple",
    "Lemon",
  ];

  cropsContainer.innerHTML = "";
  crops.forEach((crop) => {
    const col = document.createElement("div");
    col.className = "col-md-3 col-sm-4 col-6 mb-3";

    col.innerHTML = `
            <div class="crop-card">
                <i class="fas fa-seedling fa-2x text-success mb-2"></i>
                <h6 class="mb-0">${crop}</h6>
            </div>
        `;

    cropsContainer.appendChild(col);
  });
}

/**
 * Animate stats counters
 */
function animateStatsCounters() {
  const counters = document.querySelectorAll(".counter");
  if (!counters.length) return;

  counters.forEach((counter) => {
    const target = parseInt(counter.getAttribute("data-target"));
    const increment = target / 100;
    let current = 0;

    const updateCounter = () => {
      if (current < target) {
        current += increment;
        counter.textContent = Math.ceil(current) + "+";
        setTimeout(updateCounter, 20);
      } else {
        counter.textContent = target + "+";
      }
    };

    // Start animation when element is in viewport
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          updateCounter();
          observer.unobserve(entry.target);
        }
      });
    });

    observer.observe(counter);
  });
}

/**
 * Setup disease search
 */
function setupDiseaseSearch() {
  const searchInput = document.getElementById("diseaseSearch");
  if (!searchInput) return;

  searchInput.addEventListener("input", function () {
    const searchTerm = this.value.toLowerCase();
    const diseaseItems = document.querySelectorAll(".disease-list li");

    diseaseItems.forEach((item) => {
      const text = item.textContent.toLowerCase();
      if (text.includes(searchTerm)) {
        item.style.display = "";
        item.classList.add("fade-in");
      } else {
        item.style.display = "none";
      }
    });
  });
}

/**
 * Setup video player
 */
function setupVideoPlayer() {
  const videoPlaceholder = document.getElementById("videoPlaceholder");
  if (!videoPlaceholder) return;

  // Replace placeholder with actual YouTube embed
  // In production, you would use your actual YouTube video ID
  const videoId = "YOUR_YOUTUBE_VIDEO_ID";
  if (videoId && videoId !== "YOUR_YOUTUBE_VIDEO_ID") {
    videoPlaceholder.innerHTML = `
            <iframe src="https://www.youtube.com/embed/${videoId}" 
                    title="Disease Detection Tutorial" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
            </iframe>
        `;
  }
}

/**
 * Setup accordion interactions
 */
function setupAccordion() {
  const accordionButtons = document.querySelectorAll(".accordion-button");
  accordionButtons.forEach((button) => {
    button.addEventListener("click", function () {
      this.classList.toggle("active");
      const icon = this.querySelector("i");
      if (icon) {
        if (this.classList.contains("active")) {
          icon.classList.remove("fa-plus");
          icon.classList.add("fa-minus");
        } else {
          icon.classList.remove("fa-minus");
          icon.classList.add("fa-plus");
        }
      }
    });
  });
}

/**
 * Handle window resize
 */
function handleWindowResize() {
  // Close camera on small screens if open
  if (window.innerWidth < 768 && currentStream) {
    closeCamera();
    showAlert(
      "info",
      "Camera closed due to screen resize. Please recapture if needed."
    );
  }
}

/**
 * Handle scroll for navbar effects
 */
function handleScroll() {
  const navbar = document.querySelector(".navbar");
  if (window.scrollY > 50) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }

  // Animate elements on scroll
  animateOnScroll();
}

/**
 * Animate elements when they come into view
 */
function animateOnScroll() {
  const animatedElements = document.querySelectorAll(".animate-on-scroll");

  animatedElements.forEach((element) => {
    const elementTop = element.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;

    if (elementTop < windowHeight - 100) {
      element.classList.add("animated");
    }
  });
}

/**
 * Show alert message
 */
function showAlert(type, message) {
  // Remove existing alerts
  const existingAlerts = document.querySelectorAll(".alert-dismissible");
  existingAlerts.forEach((alert) => alert.remove());

  // Create alert
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
  alertDiv.setAttribute("role", "alert");

  // Set icon based on type
  let icon = "info-circle";
  if (type === "success") icon = "check-circle";
  else if (type === "error" || type === "danger") icon = "exclamation-triangle";
  else if (type === "warning") icon = "exclamation-circle";

  alertDiv.innerHTML = `
        <i class="fas fa-${icon} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  // Add to page
  const container = document.querySelector(".container") || document.body;
  container.insertBefore(alertDiv, container.firstChild);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (alertDiv.parentNode) {
      alertDiv.remove();
    }
  }, 5000);
}

/**
 * Log prediction for analytics
 */
function logPrediction(data) {
  const logEntry = {
    timestamp: new Date().toISOString(),
    disease: data.disease,
    confidence: data.confidence,
    filename: data.filename,
    userAgent: navigator.userAgent,
  };

  // In production, you would send this to your analytics server
  console.log("Prediction logged:", logEntry);

  // Store locally for debugging
  if (localStorage) {
    const logs = JSON.parse(localStorage.getItem("predictionLogs") || "[]");
    logs.push(logEntry);
    if (logs.length > 100) logs.shift(); // Keep only last 100 entries
    localStorage.setItem("predictionLogs", JSON.stringify(logs));
  }
}

/**
 * Update copyright year
 */
function updateCopyrightYear() {
  const yearElements = document.querySelectorAll(".current-year");
  const currentYear = new Date().getFullYear();

  yearElements.forEach((element) => {
    element.textContent = currentYear;
  });
}

/**
 * Export prediction data
 */
function exportPredictionData() {
  if (!currentPrediction) {
    showAlert("warning", "No prediction data to export");
    return;
  }

  const dataStr = JSON.stringify(currentPrediction, null, 2);
  const dataUri =
    "data:application/json;charset=utf-8," + encodeURIComponent(dataStr);

  const exportFileDefaultName = `disease_prediction_${Date.now()}.json`;

  const linkElement = document.createElement("a");
  linkElement.setAttribute("href", dataUri);
  linkElement.setAttribute("download", exportFileDefaultName);
  linkElement.click();

  showAlert("success", "Prediction data exported successfully");
}

/**
 * Share prediction results
 */
function shareResults() {
  if (!navigator.share) {
    showAlert("info", "Sharing is not supported by your browser");
    return;
  }

  if (!currentPrediction) {
    showAlert("warning", "No results to share");
    return;
  }

  navigator
    .share({
      title: `Disease Detection Result: ${formatDiseaseName(
        currentPrediction.disease
      )}`,
      text: `Detected ${formatDiseaseName(currentPrediction.disease)} with ${
        currentPrediction.confidence
      }% confidence. ${currentPrediction.description}`,
      url: window.location.href,
    })
    .then(() => console.log("Share successful"))
    .catch((error) => console.log("Share failed:", error));
}

/**
 * Download image with results overlay
 */
function downloadResultsImage() {
  if (!capturedImage) {
    showAlert("warning", "No image to download");
    return;
  }

  // Create canvas with results overlay
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  const img = new Image();

  img.onload = function () {
    canvas.width = img.width;
    canvas.height = img.height + 100; // Extra space for text

    // Draw original image
    ctx.drawImage(img, 0, 0);

    // Draw overlay
    ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
    ctx.fillRect(0, img.height, canvas.width, 100);

    // Draw text
    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.textAlign = "center";
    ctx.fillText(
      `Disease: ${formatDiseaseName(currentPrediction.disease)}`,
      canvas.width / 2,
      img.height + 30
    );
    ctx.fillText(
      `Confidence: ${currentPrediction.confidence}%`,
      canvas.width / 2,
      img.height + 60
    );
    ctx.fillText(
      `Detected on: ${new Date().toLocaleDateString()}`,
      canvas.width / 2,
      img.height + 90
    );

    // Download
    const link = document.createElement("a");
    link.download = `disease_result_${Date.now()}.png`;
    link.href = canvas.toDataURL("image/png");
    link.click();

    showAlert("success", "Image with results downloaded");
  };

  img.src = URL.createObjectURL(capturedImage);
}

// Make functions available globally
window.exportPredictionData = exportPredictionData;
window.shareResults = shareResults;
window.downloadResultsImage = downloadResultsImage;
