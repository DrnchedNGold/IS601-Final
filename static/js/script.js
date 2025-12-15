// Your JavaScript code can go here.
console.log("JavaScript loaded!");

// Helper: Get JWT token from localStorage (assumes login flow stores it)
function getToken() {
  return localStorage.getItem("access_token");
}

// Fetch and populate user profile data
async function loadProfile() {
  const token = getToken();
  if (!token) return;
  const res = await fetch("/users/me", {
    headers: { Authorization: "Bearer " + token }
  });
  if (res.ok) {
    const user = await res.json();
    document.getElementById("first_name").value = user.first_name || "";
    document.getElementById("last_name").value = user.last_name || "";
    document.getElementById("username").value = user.username || "";
    document.getElementById("email").value = user.email || "";
  }
}

// Profile update form handler
document.getElementById("profile-form")?.addEventListener("submit", async function (e) {
  e.preventDefault();
  const token = getToken();
  if (!token) {
    document.getElementById("profile-message").textContent = "Not authenticated.";
    return;
  }
  const data = {
    first_name: document.getElementById("first_name").value.trim(),
    last_name: document.getElementById("last_name").value.trim(),
    username: document.getElementById("username").value.trim(),
    email: document.getElementById("email").value.trim()
  };
  // Simple validation
  if (!data.first_name || !data.last_name || !data.username || !data.email) {
    document.getElementById("profile-message").textContent = "All fields are required.";
    return;
  }
  const res = await fetch("/users/me", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token
    },
    body: JSON.stringify(data)
  });
  if (res.ok) {
    document.getElementById("profile-message").textContent = "Profile updated successfully.";
    loadProfile();
  } else {
    const err = await res.json();
    document.getElementById("profile-message").textContent = err.detail || "Update failed.";
  }
});

// Password change form handler
document.getElementById("password-form")?.addEventListener("submit", async function (e) {
  e.preventDefault();
  const token = getToken();
  if (!token) {
    document.getElementById("password-message").textContent = "Not authenticated.";
    return;
  }
  const current_password = document.getElementById("current_password").value;
  const new_password = document.getElementById("new_password").value;
  const confirm_new_password = document.getElementById("confirm_new_password").value;
  // Client-side validation
  if (!current_password || !new_password || !confirm_new_password) {
    document.getElementById("password-message").textContent = "All fields are required.";
    return;
  }
  if (new_password !== confirm_new_password) {
    document.getElementById("password-message").textContent = "New passwords do not match.";
    return;
  }
  if (new_password.length < 8) {
    document.getElementById("password-message").textContent = "New password must be at least 8 characters.";
    return;
  }
  const res = await fetch("/users/me/change-password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token
    },
    body: JSON.stringify({ current_password, new_password, confirm_new_password })
  });
  if (res.status === 204) {
    document.getElementById("password-message").textContent = "Password changed successfully.";
    document.getElementById("password-form").reset();
  } else {
    const err = await res.json();
    document.getElementById("password-message").textContent = err.detail || "Password change failed.";
  }
});

// Auto-load profile data on profile page
if (document.getElementById("profile-form")) {
  loadProfile();
}
