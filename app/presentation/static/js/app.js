// --- Customize these if you want ---
const WEBINAR_DATE_TEXT = "TBA"; // e.g. "March 15, 2026 • 09:00 CET"

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
  // --- Elements ---
  const form = document.getElementById("signupForm");
  const submitBtn = document.getElementById("submitBtn");
  const errorBox = document.getElementById("errorBox");
  const successBox = document.getElementById("successBox");

  document.getElementById("year").textContent = new Date().getFullYear();
  document.getElementById("webinarDate").textContent = WEBINAR_DATE_TEXT;

  function showError(message){
    successBox.style.display = "none";
    errorBox.textContent = message;
    errorBox.style.display = "block";
  }

  function showSuccess(message){
    errorBox.style.display = "none";
    successBox.textContent = message;
    successBox.style.display = "block";
  }

  function isValidEmail(email){
    // Simple, practical validation
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const firstName = document.getElementById("firstName").value.trim();
    const lastName  = document.getElementById("lastName").value.trim();
    const email     = document.getElementById("email").value.trim();
    const consent   = document.getElementById("consent").checked;

    if (!email) return showError("Please enter your email.");
    if (!isValidEmail(email)) return showError("That email doesn't look quite right. Please check it.");
    if (!consent) return showError("Please tick the consent box to sign up.");

    // Fake "submit" (local-only).
    // Later you can replace this block with Firebase/Firestore or an API call.
    submitBtn.disabled = true;
    submitBtn.textContent = "Signing you up...";

    try {
      // Simulate network delay
      await new Promise(r => setTimeout(r, 600));

      // Store locally so you can test "it worked" without a backend
      const payload = { firstName, lastName, email, consent, ts: new Date().toISOString() };
      const key = "webinar_signups";
      const existing = JSON.parse(localStorage.getItem(key) || "[]");
      existing.push(payload);
      localStorage.setItem(key, JSON.stringify(existing));

      form.reset();
      showSuccess("You're signed up! We'll email you webinar updates and a reminder.");
    } catch (err) {
      console.error(err);
      showError("Something went wrong. Please try again.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Sign me up";
    }
  });
});
