# 🌍 Blockchain-Based Blue Carbon MRV System

A project to build a **transparent, verifiable, and decentralized Monitoring, Reporting & Verification (MRV) system** for **Blue Carbon ecosystems** in India and beyond.  

This project combines:
- ⚡ **Machine Learning** – to verify NGO/panchayat restoration projects using satellite/drone images and estimate CO₂ sequestration.  
- 🔗 **Blockchain** – to immutably store verified data and tokenize carbon credits.  
- 🌱 **Web + Mobile Interfaces** – for NGOs, Admins (NCCR), and Corporates to interact with the registry.  

---

## 🚀 Features

- 📸 **ML-powered verification** of mangrove/coastal restoration projects from satellite/drone imagery.  
- 🌳 **Biomass → Carbon → Carbon Credits** calculation pipeline.  
- 🔐 **Blockchain registry** (via smart contracts) for credit issuance & trading.  
- 👩‍🌾 **NGO / Panchayat portal** to upload project details & evidence.  
- 🏛 **Admin portal (NCCR)** to review, approve, and issue credits.  
- 🏢 **Corporate portal** to purchase verified carbon credits.

---

## Environment variables

The project reads sensitive configuration from a `.env` file at the project root (this file is listed in `.gitignore`). Create a `.env` with at least the following keys:

- `SECRET_KEY` - Django secret key
- `DEBUG` - `True` or `False`
- `DATABASE_URL` - full database URL (e.g. `postgresql://user:pass@host:port/dbname`)
- `ALLOWED_HOSTS` - comma-separated hosts
- `EMAIL_BACKEND` (optional) - email backend, default `django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST` (optional) - SMTP host, default `smtp.gmail.com`
- `EMAIL_PORT` (optional) - SMTP port, default `587`
- `EMAIL_USE_TLS` (optional) - `True`/`False`, default `True`
- `EMAIL_HOST_USER` - SMTP username (email address)
- `EMAIL_HOST_PASSWORD` - SMTP password or app password
- `DEFAULT_FROM_EMAIL` (optional) - default from address
- `ORG_NAME`, `SENDER_NAME`, `SENDER_TITLE`, `SUPPORT_EMAIL` (optional) - branding and contact info

Make sure `.env` is not committed to source control.