// Shared key used by both index and admin pages
const STORAGE_KEY = "webinar_signups_v1";
const WEBINAR_DATE_TEXT = "February 16 • 16:00–18:00 CET";

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById("signupForm");
  const submitBtn = document.getElementById("submitBtn");
  const errorBox = document.getElementById("errorBox");
  const successBox = document.getElementById("successBox");

  document.getElementById("year").textContent = new Date().getFullYear();

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
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function readSignups(){
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]"); }
    catch { return []; }
  }

  function writeSignups(list){
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
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

    submitBtn.disabled = true;
    submitBtn.textContent = "Signing you up...";

    try {
      await new Promise(r => setTimeout(r, 450));

      const list = readSignups();
      const normalizedEmail = email.toLowerCase();

      // Prevent duplicates by email (update name + timestamp if already exists)
      const existingIdx = list.findIndex(x => (x.email || "").toLowerCase() === normalizedEmail);

      const payload = {
        firstName,
        lastName,
        email,
        consent,
        webinar: WEBINAR_DATE_TEXT,
        ts: new Date().toISOString()
      };

      if (existingIdx >= 0) list[existingIdx] = { ...list[existingIdx], ...payload };
      else list.push(payload);

      writeSignups(list);

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
