# Student Project Topic Approval System — Flask Backend

Production-oriented Flask API and relational database backend for the supplied React/Vite Student Project Topic Approval System (SPTAS).

## What this replaces

The frontend currently stores lecturers, students, submissions and the lecturer password in browser `localStorage`. This backend moves those records to a real relational database and provides authenticated API endpoints.

## Architecture

- Flask 3 application factory
- SQLAlchemy ORM
- PostgreSQL for production; SQLite for local development
- Flask-Migrate/Alembic-ready schema management
- JWT authentication for lecturers
- Werkzeug password hashing — passwords are never stored in plaintext
- CORS restricted to configured frontend origins
- Database indexes for lecturer/status and student/submission lookups
- Audit log for submission creation and review decisions
- Validation and authorization around review operations

## Database entities

### `lecturers`
Stores lecturer identity, department, email, password hash and active state.

### `students`
Stores matric number and student name.

### `topic_submissions`
Stores each proposed topic, assigned lecturer, status, feedback and timestamps. A rejected topic can be resubmitted as a new submission, matching the current frontend workflow.

### `audit_logs`
Records important submission events and the lecturer who performed review actions.

## API

### Public
- `GET /api/health`
- `GET /api/lecturers`
- `GET /api/lecturers/<lecturerId>`
- `POST /api/students`
- `GET /api/students/<matricNumber>`
- `POST /api/auth/lecturer/login`
- `POST /api/submissions`
- `GET /api/submissions`
- `GET /api/submissions/<submissionId>`

### Authenticated lecturer
- `PATCH /api/submissions/<submissionId>/decision`

Examples:

```json
POST /api/auth/lecturer/login
{
  "lecturerId": "lec001",
  "password": "your-password"
}
```

```json
POST /api/submissions
{
  "studentMatric": "CSC/001/2026",
  "studentName": "Jane Doe",
  "lecturerId": "lec001",
  "topic": "Design and implementation of a student project approval system"
}
```

```json
PATCH /api/submissions/sub_xxx/decision
Authorization: Bearer <accessToken>

{
  "status": "approved",
  "comment": "Approved. Proceed to chapter one."
}
```

List/filter submissions with query parameters:

`GET /api/submissions?lecturerId=lec001&status=pending&search=Jane`

or:

`GET /api/submissions?studentMatric=CSC/001/2026`

## Local setup

Python 3.11+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```

Set a real `SECRET_KEY` and `JWT_SECRET_KEY` in `.env`.

For a quick local SQLite database:

```bash
python seed.py
python run.py
```

The API runs at `http://localhost:5000`.

## PostgreSQL production

Set:

```env
DATABASE_URL=postgresql+psycopg://username:password@host:5432/sptas
```

Then initialize/migrate the schema with Flask-Migrate in your deployment environment. For the initial project state, `python seed.py` also creates the tables; for an established production database, use migrations rather than `db.create_all()`.

## Frontend integration

Replace the current `src/services/storage.ts` localStorage implementation with HTTP calls to this API. Recommended mapping:

- `getLecturers()` → `GET /api/lecturers`
- `createSubmission()` → `POST /api/submissions`
- `getSubmissionsByStudent()` → `GET /api/submissions?studentMatric=...`
- `getSubmissionsByLecturer()` → `GET /api/submissions?lecturerId=...`
- `approveSubmission()` → `PATCH /api/submissions/<id>/decision` with `status=approved`
- `rejectSubmission()` → same endpoint with `status=rejected`
- `authenticateLecturer()` → `POST /api/auth/lecturer/login`
- `saveStudent()` → `POST /api/students`

The backend intentionally preserves the JSON field names already used by the React application (`studentMatric`, `studentName`, `lecturerId`, `submittedAt`, etc.), minimizing frontend changes.

## Security notes

The password that was embedded in the original frontend has deliberately been removed from application code. Demo credentials are controlled through `DEMO_LECTURER_PASSWORD`. Change this value before deployment and use a strong secret. In production, also put the API behind HTTPS, use a managed PostgreSQL database, restrict CORS to the deployed frontend origin, and configure proper backup/monitoring.
