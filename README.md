# Smart Home Management System

A modern, full-stack Enterprise Smart Home Management Dashboard built with **FastAPI** (Python), **Nuxt 3** (Vue.js), and **PostgreSQL**. This system enables users to monitor hardware network status, securely control IoT device settings asynchronously, and view categorized high-risk security logs originating from IoT hardware.

## 🚀 Features

- **Event-Driven UI (Reactivity):** Seamless real-time state synchronization via Vue 3 proxies (no page refreshes during toggles or parameter adjustments).
- **Relational & JSONB Postgres Modeling:** Devices and Locations linked structurally (SQL), while device metrics and sensor anomalies are managed inside ultra-fast JSONB document columns.
- **JWT-Based Authentication:** Multi-tier authorization logic (System Admin vs User). Endpoints protected natively via FastAPI dependency injection.
- **Glassmorphic UI Engine:** Native Nuxt implementation mimicking modern enterprise dashboard visuals (Blur layers, LED network indicators, animated modals).
- **Hardware Agnostic Control Panel:** Specific capabilities adapted conditionally via component rendering (e.g., thermostat +/- control panels exclusive to "Climate" devices).

##  Tech Stack

### Backend
- **Framework:** FastAPI (High performance asynchronous Python framework)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (Native Postgres UUIDs and JSONB supported)
- **Auth:** PyJWT (Stateless Bearer Tokens)

### Frontend
- **Framework:** Nuxt 3 (SSR & CSR Vue.js Framework)
- **Styling:** Custom CSS3 with responsive Grid/Flex modules and Glassmorphism optics
- **Integration:** Ultra-fast native `$fetch` API pipeline

## Setup & Installation

### 1. Database Configuration
Ensure you have an instance of PostgreSQL running locally. Update connection credentials in `app/core/database.py` if necessary (Default is: `postgresql://postgres:halil123@127.0.0.1:5432/smarthome`).

Run the initialization and seed scripts to build your schemas and inject dummy test data:
```bash
python init_db.py         # Builds database tables based on SQLAlchemy Models
python seed_db.py         # Injects sample Admin Account & Test Devices
python seed_logs.py       # Injects sample JSONB device telemetry logs
```

### 2. Backend Startup
```bash
# Install Python dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pyjwt passlib

# Start the ASGI server (API)
uvicorn main:app --reload
```
*API will run on `http://localhost:8000`*

### 3. Frontend Startup (Nuxt 3)
```bash
cd frontend-nuxt

# Install Node dependencies
npm install

# Start the Vue 3 Development Server
npm run dev
```
*UI will run on `http://localhost:3000`*

##  Default Credentials (Seed Data)
- **Admin Panel Access:** `admin@sirket.com` / `admin123`
- **Standard User Access:** `uye@sirket.com` / `uye123`
