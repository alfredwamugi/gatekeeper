# gatekeeper

gatekeeper is a vehicle Gate audit and reconciliation system for tracking entries/exits, recording dwell times, and generating end-of-day summaries.

## Features

- YOLO-based vehicle detection
- ByteTrack-based ID tracking
- SQLite audit persistence
- EOD revenue and anomaly reporting
- SMS alert integration via Africa's Talking

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the tracker:
   `python main.py`
4. Run the regression tests:
   `python -m unittest discover -s tests -v`

## Configuration & Secrets

gatekeeper reads runtime overrides and secrets from environment variables (or a local `.env` file). Copy `.env.example` to `.env` and update values before running locally or in Docker. Do NOT commit real secrets.

Required env variables (example):

- `AFRICASTALKING_USERNAME` â€” Africa's Talking username (use `sandbox` for testing)
- `AFRICASTALKING_API_KEY` â€” Africa's Talking API key (keep secret)
- `AFRICASTALKING_RECIPIENT_PHONE` â€” Phone number to receive alerts
- `DB_PATH` — Optional SQLite path override (default: `gatekeeper.db`)

Run locally after creating `.env`:

```bash
cp .env.example .env
# edit .env and fill secrets
python main.py
```

Run with Docker Compose. The helper script falls back to `docker-compose` if the v2 plugin is not installed:

```bash
./deploy/compose.sh up --build
```

## Production notes

- Configure `config.json` for your production Gate geometry and thresholds.
- Ensure your vehicle detection model is aligned with the camera perspective.
- Review anomaly thresholds before deployment.

## Reporting exports and automation

Generate the daily summary and export the report files to the `reports/` folder:

```bash
python scripts/generate_report.py
```

This writes both JSON and CSV files alongside the console summary. To export only a specific format, use the helper in Python:

```python
from scripts.generate_report import generate_daily_report, export_summary_report

summary = generate_daily_report("gatekeeper.db")
export_summary_report(summary, "reports", format="json")
export_summary_report(summary, "reports", format="csv")
```

For scheduled automation on Linux or WSL, add a cron job such as:

```bash
0 0 * * * cd /path/to/gatekeeper && ./scripts/daily_report_cron.sh
```

## Docker packaging

Build the image locally:

```bash
docker build -t gatekeeper:latest .
```

Or run the app using Docker Compose:

```bash
./deploy/compose.sh up --build
```

This container is intended for edge-style deployment and runs the tracker entrypoint defined in `main.py`.

## Windows deployment and automation

Create a Task Scheduler entry for the daily report script on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_windows_task.ps1
```

This creates a daily scheduled task named `gatekeeperDailyReport` that runs the report script at midnight by default.

## Health monitoring for container edge deployment

A lightweight HTTP health endpoint is available in `src/health.py`.

```bash
python -m gatekeeper.health
```

Then check:

```bash
curl http://localhost:8080/healthz
curl http://localhost:8080/readyz
```

Expected response includes:

```json
{"status": "ok", "service": "gatekeeper", "database": {"connected": true, "database": "gatekeeper.db"}}
```

## Build and publish

Build the source distribution and wheel locally:

```bash
python -m build
```

Or, using the included helper:

```bash
make build
```

To publish to PyPI or a private package index, use the workflow in `.github/workflows/release.yml`.
