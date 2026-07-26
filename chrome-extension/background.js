/* Background service worker for Apply Copilot */

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ apiBase: "" });
});

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg.action === "set_api_base") {
    chrome.storage.local.set({ apiBase: msg.apiBase }).then(() => sendResponse({ ok: true }));
    return true;
  }
  if (msg.action === "get_api_base") {
    chrome.storage.local.get(["apiBase"]).then((data) => sendResponse({ apiBase: data.apiBase || "" }));
    return true;
  }
});
