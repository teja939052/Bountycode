const API_BASE = ""; // filled by background/service worker via chrome.storage

function setStatus(msg, isError = false) {
  const el = document.getElementById("status");
  el.textContent = msg;
  el.style.color = isError ? "#dc2626" : "#374151";
}

async function getApiBase() {
  const data = await chrome.storage.local.get(["apiBase", "sessionCookie"]);
  return data.apiBase || "";
}

async function getAuthHeaders() {
  const data = await chrome.storage.local.get(["sessionCookie"]);
  const cookie = data.sessionCookie || "";
  return {
    "Content-Type": "application/json",
    ...(cookie ? { Cookie: cookie } : {}),
  };
}

async function autofill() {
  setStatus("Reading form fields...");
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  await chrome.tabs.sendMessage(tab.id, { action: "autofill" });
  setStatus("Autofill signal sent to content script.");
}

async function tailorResume() {
  setStatus("Reading job description...");
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  await chrome.tabs.sendMessage(tab.id, { action: "tailor_resume" });
  setStatus("Tailor signal sent.");
}

async function coverLetter() {
  setStatus("Generating cover letter...");
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  await chrome.tabs.sendMessage(tab.id, { action: "cover_letter" });
  setStatus("Cover letter signal sent.");
}

async function trackApplication() {
  setStatus("Saving application...");
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  await chrome.tabs.sendMessage(tab.id, { action: "track_application" });
  setStatus("Application saved.");
}

async function practiceForRole() {
  setStatus("Opening practice session...");
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  await chrome.tabs.sendMessage(tab.id, { action: "practice_for_role" });
  setStatus("Practice signal sent.");
}

document.getElementById("fillBtn").addEventListener("click", autofill);
document.getElementById("tailorBtn").addEventListener("click", tailorResume);
document.getElementById("letterBtn").addEventListener("click", coverLetter);
document.getElementById("trackBtn").addEventListener("click", trackApplication);
document.getElementById("practiceBtn").addEventListener("click", practiceForRole);

(async () => {
  const apiBase = await getApiBase();
  if (!apiBase) setStatus("Set API base in options to connect.", true);
})();
