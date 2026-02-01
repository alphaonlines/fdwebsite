# Repository Guidelines

## Project Structure & Module Organization
- `dashboard.py` is the only application code. It runs a small HTTP server that renders the HTML files in this repo inside a preview shell and supports CSV-based updates.
- HTML content files live at the repo root: `living room`, `bedrooms`, `dining-room`, `recliners`, `manager-specials`.
- Docker assets: `Dockerfile`, `.dockerignore`. Git settings: `.gitignore`.

## Quick Start
- `python3 dashboard.py` then open `http://localhost:8000` to browse and preview pages.
- To preview from Docker: `docker build -t fdwebsite .` then `docker run -p 8000:8000 fdwebsite`.
- CSV update via API:
  - `curl -X POST http://localhost:8000/upload-csv -H "Content-Type: application/json" -d '{"csv":"section,sku,name,price\\nliving room,123,Sample,999"}'`

## Build, Test, and Development Commands
- `python3 dashboard.py` — start the preview server locally (default `http://0.0.0.0:8000`).
- `HOST=127.0.0.1 PORT=8000 python3 dashboard.py` — override bind host/port.
- `docker build -t fdwebsite .` — build the container image.
- `docker run -p 8000:8000 fdwebsite` — run the preview server in Docker.

## Coding Style & Naming Conventions
- Python: 4-space indentation, standard library only. Keep code compatible with Python 3.12 (Docker base image).
- HTML files are long single-line documents; avoid reformatting unless required.
- Filenames are lower-case and use spaces or hyphens (e.g., `living room`, `dining-room`). Preserve existing names because `dashboard.py` references them directly.

## Testing Guidelines
- No automated tests are currently configured. If adding tests, keep them lightweight and document how to run them.

## Commit & Pull Request Guidelines
- Git history is minimal (single commit), so no established commit message convention exists. Use short, imperative summaries (e.g., “Update recliner layout”).
- PRs should include:
  - A brief description of the change and affected files.
  - Screenshots or a short GIF for visible HTML changes.
  - Notes on any CSV/schema updates, if applicable.

## Configuration & Data Updates
- Environment variables: `HOST` and `PORT` control the server bind settings.
- CSV uploads in the dashboard update sections by keyword (`living room`, `bedroom`, `dining room`, `recliner`) and write `.bak-<timestamp>` backups next to the modified file.

## Server Environment (wolf.discount)
- Reverse proxy: nginx system service binding `:80`/`:443`.
- nginx configs: `/etc/nginx/nginx.conf`, `/etc/nginx/sites-available/wolf.discount`, `/etc/nginx/conf.d/alphapulse.conf`.
- Public web root: `/srv/www/wolf.discount/` (current live landing page at `/srv/www/wolf.discount/index.html`).
- Owner dashboard (static): `/srv/www/wolf/owner/` served at `/owner/`.
- API routes:
  - `/api/*` -> `127.0.0.1:5055` (alphapulse-pos)
  - `/api/server/*` -> `127.0.0.1:5056` (wolf-api)
- Other static routes: `/agents/`, `/showcase/`, `/tf11/`, `/assets/`.
- Reload after nginx edits: `sudo nginx -t` then `sudo systemctl reload nginx`.

## Recent Changes (2026-01-31)
- Moved FD public pages to subdomain: https://furnituredistributors.wolf.discount/
- Added redirects from https://wolf.discount/furnituredistributors/* and /fd/ to the new subdomain.
- Enabled /fd/ app on the subdomain with /fd/api/* routed to :5057.
- Added quick-links index page on the subdomain root with a dashboard button.
- Bedroom page restored with mobile-friendly stacking only (no snow effect).
- Added CSV upload modal button to FD dashboard (/fd/) gated by dashboard unlock; posts to /fd-upload-csv.
- Nginx now listens on 0.0.0.0:80/443 and :443/:80 IPv6; SSL issued for subdomain.
