# JobFlow — AI-Powered Job Search Dashboard

A self-contained, local-first job search CRM with **Claude AI integration**. Built as a single HTML file with a lightweight Python server for persistent storage. No backend, no database, no cloud — runs entirely on your machine.

---

## Features

### Job Board & Pipeline
- Card-based job board with fit score bars (color-coded: green ≥80, amber ≥60, red <60)
- Kanban pipeline view: To Apply → Applied → Screening → Interview → Offer → Rejected
- Analytics dashboard: score distribution, status breakdown, skill demand
- Full-text search, filter by status, sort by score or date

### Claude AI Integration
- ** AI Score & Parse JD** — paste a job description, Claude scores your fit 0–100 and auto-fills all fields
- ** Fetch JD from URL** — paste a job link, automatically extracts title, company, salary, and full JD
- **9-Step Application Agent** — full application workflow powered by Claude:

| Step | Output |
|------|--------|
| 1 — Company Research | News, funding, culture, recent signals |
| 2 — Fit Analysis | Score, top 3 reasons, gaps, positioning hook |
| 3 — Contact Research | Hiring manager, LinkedIn, email patterns |
| 4 — CV Tailoring | Headline, keywords to add, bullets to reorder |
| 5 — Cover Letter | Under 300 words, specific hook, no AI clichés |
| 6 — Cold Email + LinkedIn DM | Subject line + connection request |
| 7 — Application Q&A | Form questions answered in your voice |
| 8 — Send Sequence | Day-by-day action plan with timing |
| 9 — Tailored Resume | Full 1-page PDF rewritten for this specific JD |

### Storage
- Runs in browser-only mode by default (localStorage)
- Start the Python server for permanent disk storage (`jobflow_data.json`)
- Auto-merges browser-only jobs to disk when server is started
- CSV and JSON export

---

## Project Structure

```
jobflow/
├── JobSearch_System.html    ← Entire dashboard (single file)
├── jobflow_server.py        ← Python local server for disk storage
├── jobflow_data.json        ← Your job data (auto-created, gitignored)
├── .gitignore
└── README.md
```

---

## Setup

### Option 1 — Browser Only (quickest)
Double-click `JobSearch_System.html` to open in your browser. Jobs save to localStorage.

### Option 2 — With Disk Storage (recommended)
```bash
cd jobflow
python3 jobflow_server.py
```
Dashboard opens automatically at **http://localhost:8765**. Jobs save permanently to `jobflow_data.json`.

Press `Ctrl+C` to stop the server.

---

## Configuration

Open `JobSearch_System.html` in a text editor and update the `PROFILE` object near the top:

```javascript
const PROFILE = {
  name: "Your Name",
  title: "Your Title",
  location: "Your City, State",
  email: "your.email@gmail.com",
  phone: "+1 (000) 000-0000",
  linkedin: "linkedin.com/in/your-profile",
  years: 5,
  proofPoint: "Your top achievement in one sentence",
  skills: ["Python", "SQL", "Spark", ...],
  experience: [...],
  education: [...],
  targets: ["Senior Data Engineer", ...],
};
```

The AI prompts use this profile automatically — every cover letter, cold email, and resume is tailored to your background.

---

## API Key Setup

1. Open the dashboard
2. Click **"No API Key"** in the bottom-left sidebar
3. Paste your Anthropic API key (`sk-ant-api03-…`)
4. Key is stored only in your browser's localStorage and `jobflow_data.json` — never transmitted anywhere except Anthropic's API

Get an API key at [console.anthropic.com](https://console.anthropic.com)

---

## API Credit Usage

| Action | Calls | Approx. Tokens |
|--------|-------|---------------|
| AI Score & Parse JD | 1 | ~800–1,000 |
| Run single step (1–8) | 1 | ~1,000–1,500 |
| Step 9 — Tailored Resume | 1 | ~2,500–3,500 |
| Fetch JD from URL | 1 | ~1,500–2,000 |
| Run All Steps | 9 | ~12,000–18,000 |

**Tip:** Use **Copy Full Prompt** to paste into [claude.ai](https://claude.ai) and use your subscription instead of API tokens.

---

## Privacy

- API key stored only in browser localStorage and local `jobflow_data.json`
- Job data never leaves your machine except when an AI button is clicked (JD text sent to Anthropic API)
- No analytics, no tracking, no third-party services except Google Fonts and Chart.js (CDN)
- `jobflow_data.json` is gitignored — your job search stays private

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vanilla HTML/CSS/JS — zero frameworks |
| AI | Anthropic Claude API (claude-sonnet) |
| Storage | localStorage + Python `http.server` + JSON |
| Server | Python 3 stdlib only — no pip installs needed |
| Fonts | Google Fonts (DM Sans, DM Serif Display) |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Storage shows "Browser only" | Run `python3 jobflow_server.py` |
| No API Key error | Click status dot in sidebar → paste key |
| Deleted job comes back on refresh | Click 💾 Sync to Disk after deleting |
| Fetch JD returns empty | Page requires login — paste JD text manually |
| PDF is 2 pages | Chrome print → Margins → **None** |

---

## 📄 License

MIT — free to use, fork, and adapt for your own job search.
