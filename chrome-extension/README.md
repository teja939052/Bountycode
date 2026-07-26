# PlacementPro Apply Copilot — Chrome Extension

## What it does
- Autofill job application forms from your PlacementPro Career Profile.
- Tailor your resume for the current job posting (one click).
- Draft a cover letter for the role/company on the page.
- Log the application into PlacementPro's Application Tracker.
- Launch a "Practice for This Role" session from any job page.

## How to install (dev)
1. Open Chrome and go to `chrome://extensions/`.
2. Enable **Developer mode** (top right).
3. Click **Load unpacked**.
4. Select the `chrome-extension/` folder from this repo.
5. Pin the extension and click the icon to open the popup.

## Setup
1. Open the extension popup and note the API base.
2. You need a running PlacementPro backend with cookies enabled.
3. For cross-origin cookies to work in the extension, set your backend CORS to allow the extension origin, or use the same host as the frontend.
4. Login to PlacementPro in the same browser so the session cookie is present.

## Privacy & Trust
- Nothing is submitted without you clicking a button.
- Demographic / equal-opportunity fields are never touched.
- Filled fields are highlighted so you can verify before submitting.

## Files
- `manifest.json` — Manifest V3 config.
- `popup.html` / `popup.js` — Extension popup UI and actions.
- `content.js` — DOM reader/writer; detects form fields and fills them.
- `background.js` — Service worker for storage/messaging.
- `api.js` — Shared API helpers.

## Roadmap
- Better field mapping per ATS (Workday / Lever / Greenhouse).
- Save tailored resume + cover letter to PlacementPro profile.
- Show matched drive alerts when visiting a company careers page.
