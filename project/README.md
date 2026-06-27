# NexForge Automation

Enterprise Django + DRF + PostgreSQL website/platform for NexForge Automation
(industrial automation, IIoT, robotics).

## Stack
Django 6 · Django REST Framework · PostgreSQL · Bootstrap 5 · vanilla JS · WhiteNoise · Gunicorn.

## Apps
| App | Responsibility |
|-----|----------------|
| `core` | Lookups (Industry, Technology, Client), template pages, sitemaps, seed |
| `projects` | Project portfolio + gallery/videos/deliverables |
| `services` | Service catalogue + benefits/deliverables |
| `blog` | Categories + posts |
| `contact` | Enquiry (CRM) + email notification |
| `content` | FAQ, gallery, awards, downloads, testimonials |
| `accounts` | Roles via Django Groups (data migration) |

## Setup
```bash
cd project
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # Windows
cp .env.example .env        # then fill in real values
```

### Environment variables (`.env`)
`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`, email (`EMAIL_HOST`,
`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PORT`, `EMAIL_USE_TLS`,
`DEFAULT_FROM_EMAIL`, `SALES_INBOX`), and `CORS_ALLOWED_ORIGINS` (prod).
See `.env.example`. **Never commit `.env`.**

## Run
```bash
.venv/Scripts/python manage.py migrate
.venv/Scripts/python manage.py seed            # demo data (optional)
.venv/Scripts/python manage.py createsuperuser
.venv/Scripts/python manage.py runserver
```
- Site: `/`  · Admin: `/admin/`  · API: `/api/v1/`  · SEO: `/sitemap.xml`, `/robots.txt`

## Settings
Split: `config/settings/{base,dev,prod}.py`. Default module `config.settings.dev`;
set `DJANGO_SETTINGS_MODULE=config.settings.prod` in production.

## API
Read-only public viewsets: `projects`, `services`, `blog`, `faqs`, `gallery`,
`awards`, `downloads`, `testimonials`. `enquiries` = public create, staff
list/update. Token login: `POST /api/v1/auth/login/`.

## Test
```bash
.venv/Scripts/python manage.py test
```
Tests create a temp database; against a managed Postgres that blocks
`CREATE DATABASE` (e.g. Supabase), run with a local engine:
`DATABASE_URL=sqlite://:memory: .venv/Scripts/python manage.py test`.

## Deploy
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```
Nginx → Gunicorn; serve `/static/` (WhiteNoise) and `/media/`; SSL via Certbot.
