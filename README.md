# Page Pulse

Page Pulse is a modern Flask-based website analyzer that audits a URL and returns a clean SEO report with key on-page signals and performance details.

## Features

- Modern glassmorphism UI
- Responsive layout
- SEO score with progress bar
- HTTP status and response time
- Page title, meta description, H1 count, and missing alt text
- Word count and improvement suggestions
- Copy report and print/download support
- Local recent report history

## Setup

1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app locally:
   ```bash
   python app.py
   ```
4. Open http://127.0.0.1:5000/

## API contract

### POST /analyze
Request body:
```json
{
  "url": "https://example.com"
}
```

Response example:
```json
{
  "status": 200,
  "response_time": "0.74 sec",
  "title": "Example Domain",
  "meta_description": "No Meta Description",
  "h1_count": 1,
  "missing_alt_images": 0,
  "word_count": 21,
  "favicon": "https://www.google.com/s2/favicons?domain=example.com&sz=128",
  "seo_score": 75,
  "issues": ["Missing meta description", "Content appears short"]
}
```

## Design decisions

1. Flask + vanilla JavaScript
   - I chose Flask for a lightweight backend and plain JavaScript for the frontend so the project stays simple, fast to build, and easy to deploy.

2. Server-side HTML parsing with BeautifulSoup
   - BeautifulSoup keeps the analysis logic readable and makes the implementation easier to maintain while still being effective for SEO checks.

3. Clear user-facing error handling
   - The app returns friendly messages for invalid URLs, timeouts, and non-HTML responses so the user experience stays stable and predictable.

## Testing

Run tests with:
```bash
pytest
```

## Deployment

This app is ready to be deployed on Render.

### Render deployment steps
1. Push the repository to GitHub.
2. Create a new Web Service on Render.
3. Connect the repository and use the following start command:
   ```bash
   gunicorn app:app
   ```
4. Set the Python version to 3.11.

## Loom demo

Record a short Loom walkthrough showing the UI, the analysis flow, and one code section you would improve with more time.
