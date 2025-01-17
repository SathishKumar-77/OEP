// Toggle between view and edit mode for profile
function editProfile(field) {
    // Show the form and hide the display
    document.getElementById("profileForm").classList.remove("d-none");
    document.querySelector(".profile-info").classList.add("d-none");

    // Pre-fill the form with current values
    document.getElementById("inputName").value = document.getElementById("profileName").textContent;
    document.getElementById("inputEmail").value = document.getElementById("profileEmail").textContent;
    document.getElementById("inputPhone").value = document.getElementById("profilePhone").textContent;

    // On form submit, update the profile information
    document.getElementById("profileForm").onsubmit = function (event) {
        event.preventDefault();
        updateProfile();
    };
}

// Update profile data and revert back to view mode
function updateProfile() {
    // Get the updated values from the form
    const updatedName = document.getElementById("inputName").value;
    const updatedEmail = document.getElementById("inputEmail").value;
    const updatedPhone = document.getElementById("inputPhone").value;

    // Update the profile display with the new values
    document.getElementById("profileName").textContent = updatedName;
    document.getElementById("profileEmail").textContent = updatedEmail;
    document.getElementById("profilePhone").textContent = updatedPhone;

    // Hide the form and show the updated profile
    document.getElementById("profileForm").classList.add("d-none");
    document.querySelector(".profile-info").classList.remove("d-none");
}

// Password Strength Checker
document.getElementById("newPassword").addEventListener("input", function() {
    const password = this.value;
    const strengthText = document.getElementById("passwordStrength");
    let strength = "Weak";

    if (password.length >= 8) {
        strength = "Medium";
    }
    if (password.length >= 12 && /[A-Z]/.test(password) && /[0-9]/.test(password)) {
        strength = "Strong";
    }

    strengthText.textContent = "Password Strength: " + strength;
});

// Handle password change form submission
document.getElementById("passwordForm").onsubmit = function(event) {
    event.preventDefault();
    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (newPassword === confirmPassword) {
        alert("Password updated successfully!");
    } else {
        alert("Passwords do not match!");
    }
};

// Open modal to upload profile photo
function openProfileUpload() {
    const modal = new bootstrap.Modal(document.getElementById('profileUploadModal'));
    modal.show();
}

// Save the new profile photo after upload
function saveProfilePhoto() {
    const fileInput = document.getElementById("profilePhotoInput");
    const newPhoto = URL.createObjectURL(fileInput.files[0]);
    document.getElementById("profilePhoto").src = newPhoto;
    const modal = bootstrap.Modal.getInstance(document.getElementById('profileUploadModal'));
    modal.hide();
};