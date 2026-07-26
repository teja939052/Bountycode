/* Extension API bridge helpers (optional shared helpers for content/popup) */
export async function apiBase() {
  const data = await chrome.storage.local.get(["apiBase"]);
  return data.apiBase || "";
}

export async function autofillRequest(endpoint, body) {
  const base = await apiBase();
  const res = await fetch(`${base}${endpoint}`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}
