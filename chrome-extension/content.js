/* Content script for Apply Copilot.
   - Detects likely application form fields
   - Receives messages from popup/background and acts on the page
   - Never auto-submits forms
*/

const FIELD_HINTS = [
  ["name", "fullName", "full_name", "firstName", "first_name", "lastName", "last_name"],
  ["email", "e-mail", "mail"],
  ["phone", "mobile", "contact"],
  ["location", "city", "address"],
  ["linkedin", "linkedIn"],
  ["github"],
  ["summary", "about", "bio", "objective"],
  ["company", "organization", "employer"],
  ["title", "role", "position", "jobTitle"],
  ["startDate", "start_date", "from"],
  ["endDate", "end_date", "to"],
  ["description", "bullets", "details"],
];

function bestMatch(field) {
  const name = (field.name || "").toLowerCase();
  const id = (field.id || "").toLowerCase();
  const label = (field.getAttribute("aria-label") || "").toLowerCase();
  const text = [name, id, label].join(" ");

  for (const hints of FIELD_HINTS) {
    for (const hint of hints) {
      if (text.includes(hint)) {
        return hints[0];
      }
    }
  }
  return null;
}

function findFields() {
  const candidates = Array.from(document.querySelectorAll("input, textarea, select"));
  const mapped = new Map();
  for (const field of candidates) {
    if (field.disabled || field.readOnly) continue;
    if (["submit", "button", "reset", "checkbox", "radio"].includes((field.type || "").toLowerCase())) continue;
    const key = bestMatch(field);
    if (key && !mapped.has(key)) mapped.set(key, field);
  }
  return mapped;
}

function highlightField(field) {
  field.style.outline = "2px solid #2563eb";
  field.style.outlineOffset = "2px";
}

function fillField(field, value) {
  if (!value || !field) return false;
  const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set;
  const nativeTextSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value")?.set;
  const tag = field.tagName.toLowerCase();
  if (tag === "input" || tag === "textarea") {
    if (nativeSetter) nativeSetter.call(field, value);
    else field.value = value;
    field.dispatchEvent(new Event("input", { bubbles: true }));
    field.dispatchEvent(new Event("change", { bubbles: true }));
  } else if (tag === "select") {
    const options = Array.from(field.options);
    const match = options.find((o) => o.text.trim().toLowerCase() === value.toLowerCase());
    if (match) { field.value = match.value; field.dispatchEvent(new Event("change", { bubbles: true })); }
  }
  highlightField(field);
  return true;
}

async function getProfileFromApi(apiBase) {
  const res = await fetch(`${apiBase}/api/profile`, { credentials: "include" });
  if (!res.ok) throw new Error("Failed to fetch profile");
  return await res.json();
}

async function getTailoredResume(apiBase, jobDescription) {
  const profileRes = await getProfileFromApi(apiBase);
  const profile = profileRes || {};
  const resumeText = profile.summary || "";

  const res = await fetch(`${apiBase}/api/resume/optimize`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription }),
  });
  if (!res.ok) throw new Error("Tailor failed");
  return await res.json();
}

async function getCoverLetter(apiBase, companyName = "") {
  const profileRes = await getProfileFromApi(apiBase);
  const profile = profileRes || {};
  const resumeText = profile.summary || "";
  const res = await fetch(`${apiBase}/api/tools/cover-letter`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ resume_text: resumeText, job_description: "", company_name: companyName }),
  });
  if (!res.ok) throw new Error("Cover letter failed");
  return await res.json();
}

async function trackApplicationApi(apiBase, payload) {
  const res = await fetch(`${apiBase}/api/student/applications`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Track failed");
  return await res.json();
}

async function startPracticeForRole(apiBase, company, role = "SDE") {
  const res = await fetch(`${apiBase}/api/practice/session`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ company, role }),
  });
  if (!res.ok) throw new Error("Practice session failed");
  return await res.json();
}

function extractJobDescription() {
  const body = document.body.innerText || "";
  return body.slice(0, 6000);
}

function extractCompanyName() {
  const text = document.body.innerText || "";
  const m = text.match(/(?:at|@)\s+([A-Z][A-Za-z0-9 &().,-]{2,40})/);
  return m ? m[1].trim() : "";
}

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  (async () => {
    try {
      const apiBase = await (async () => {
        const data = await chrome.storage.local.get(["apiBase"]);
        return data.apiBase || "";
      })();

      if (!apiBase) {
        sendResponse({ ok: false, error: "Missing API base in extension options." });
        return;
      }

      if (msg.action === "autofill") {
        const profile = await getProfileFromApi(apiBase);
        const contact = profile.contact || {};
        const fields = findFields();
        const map = {
          name: profile.full_name || "",
          email: contact.email || "",
          phone: contact.phone || "",
          location: contact.location || "",
          linkedin: contact.linkedin || "",
          github: contact.github || "",
          summary: profile.summary || "",
        };
        const filled = [];
        for (const [key, field] of fields.entries()) {
          if (fillField(field, map[key] || "")) filled.push(key);
        }
        sendResponse({ ok: true, filled });
        return;
      }

      if (msg.action === "tailor_resume") {
        const jd = extractJobDescription();
        const data = await getTailoredResume(apiBase, jd);
        sendResponse({ ok: true, data });
        return;
      }

      if (msg.action === "cover_letter") {
        const company = extractCompanyName();
        const data = await getCoverLetter(apiBase, company);
        sendResponse({ ok: true, data, company });
        return;
      }

      if (msg.action === "track_application") {
        const company = extractCompanyName();
        const title = document.title || "";
        const data = await trackApplicationApi(apiBase, {
          company: company || "Unknown",
          role: title,
          job_url: window.location.href,
          notes: "Added via Apply Copilot",
        });
        sendResponse({ ok: true, data });
        return;
      }

      if (msg.action === "practice_for_role") {
        const company = extractCompanyName();
        const data = await startPracticeForRole(apiBase, company || "general", "SDE");
        sendResponse({ ok: true, data });
        return;
      }

      sendResponse({ ok: false, error: "Unknown action" });
    } catch (err) {
      sendResponse({ ok: false, error: err?.message || "Unknown error" });
    }
  })();

  return true;
});
