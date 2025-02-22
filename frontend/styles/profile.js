// Function to fetch user data from the API
async function fetchUserData() {
    try {
      const response = await fetch("http://127.0.0.1:5000/profile");
      if (!response.ok) {
        throw new Error("Failed to fetch user data");
      }
      const userData = await response.json();
      populateProfile(userData);
    } catch (error) {
      console.error("Error fetching user data:", error);
      alert("Failed to load user data. Please try again later.");
    }
  }
  
  // Function to populate the profile page with user data
  function populateProfile(userData) {
    document.getElementById("username").textContent = userData.username;
    document.getElementById("userId").textContent = userData.id;
    document.getElementById("phoneNumber").textContent = userData.phoneNumber;
    document.getElementById("email").textContent = userData.email;
    document.getElementById("password").textContent = "*********"; // Hide password
    document.getElementById("createdAt").textContent = new Date(
      userData.createdAt
    ).toLocaleDateString();
    document.getElementById("bio").textContent = userData.bio;
  }
  
  // Function to copy User ID
  function copyUserId() {
    const userId = document.getElementById("userId").innerText;
    navigator.clipboard
      .writeText(userId)
      .then(() => {
        alert("User ID copied to clipboard!");
      })
      .catch(() => {
        alert("Failed to copy User ID.");
      });
  }
  
  // Fetch user data when the page loads
  document.addEventListener("DOMContentLoaded", fetchUserData);
  