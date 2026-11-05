# EB Power Failure Management System

An asynchronous FastAPI application for registering electricity failure complaints, assigning work to linemen, recording repair details, and tracking complaint closure. It provides separate customer and employee authentication, role-protected operations, image upload endpoints, email notifications, and an administrative complaint statistics report.

## Project overview

The EB Power Failure Management System provides a shared workflow for electricity customers, administrators, and linemen. Customers can register, submit an outage complaint, see their own complaints, and update a complaint while it is pending. Administrators manage employee and customer records, review complaints, assign pending work to an active lineman, and close a complaint after repair completion. Linemen can see their assignments, submit repair details, and upload a repair image.

The application uses PostgreSQL through SQLAlchemy's asynchronous ORM. FastAPI exposes the HTTP API, Pydantic validates request data and serializes selected responses, and the service and repository layers separate request handling from business rules and database queries.

## Features and workflow

1. A customer registers and logs in with an email and password.
2. The customer submits a complaint. The service generates a complaint number, stores the complaint with its initial PENDING status, and sends a registration email.
3. An administrator assigns a pending complaint to an active employee with the lineman role. The application sets the complaint status to ASSIGNED and stores an assignment record.
4. The assigned lineman records the issue found and repair description. The application stores a repair record and changes the complaint status to REPAIR_COMPLETED
5. An administrator closes a repair-completed complaint. The application changes its status to CLOSED and sends a closure email.
6. Administrators can request aggregate complaint counts through the complaint statistics report.

The status transitions implemented in the service logic are:

PENDING -> ASSIGNED -> REPAIR_COMPLETED -> CLOSED



## Technology stack

| Area | Verified technology or library | Use in this project |
|---|---|---|
| API | Python, FastAPI, Uvicorn | Asynchronous HTTP API and application server |
| Validation | Pydantic, `email-validator`, `pydantic-settings` | Request/response models, email validation, environment settings |
| Database | PostgreSQL, SQLAlchemy async ORM, `asyncpg` | Persistent records and asynchronous queries/sessions |
| Schema migration | Alembic | Revision-based database schema changes |
| Authentication | PyJWT, FastAPI OAuth2 helpers | Signed access and refresh JWTs, bearer token extraction, form login |
| Password security | `pwdlib[argon2]` | Password hashing and verification through `PasswordHash.recommended()` |
| Uploads | FastAPI `UploadFile`, `python-multipart`, `aiofiles` | Multipart upload handling and asynchronous file writes |
| Email | Python `smtplib`, `email.message.EmailMessage`, Jinja2 | SMTP delivery and rendered HTML templates |
| Testing | pytest, pytest-asyncio, httpx, pytest-cov, mocking | Unit, repository integration, and API tests |

`psycopg` and `python-dotenv` are also listed in `requirements.txt`; application database URLs in the current code use `postgresql+asyncpg`. Dependencies are not version-pinned in that file.

## Roles and access

### Administrator

- Created locally by `scripts/create_admin.py`; application startup checks for an active admin and logs a warning if one is absent.
- Creates and deactivates employee accounts. Employee creation assigns the `lineman` role `admin`.
- Lists, views, and deactivates customers. Customer registration itself is public.
- Views all complaints, assigns pending complaints to active linemen, and closes complaints after repair completion.
- Views all repair details and the complaint statistics report.


### Lineman

- Logs in through the shared login endpoint as an employee.
- Views complaints assigned to that employee.
- Completes an assigned complaint by submitting repair details.
- Uploads a repair image after repair completion.

### Customer

- Registers and logs in through the shared login endpoint.
- Creates complaints and views only their own complaint list.
- Uploads an image for their own pending complaint.
- Updates their own complaint while it remains pending.

Public endpoints are customer registration, login, refresh-token exchange, and health check. Other operations require the role-specific authorization described in the API reference. 

## Architecture


- **Routers** declare HTTP methods, URL paths, request parameters, schemas, and dependencies.
- **Service interfaces** use abstract base classes to declare service contracts. Service implementations contain application rules such as duplicate checks, status checks, and password hashing.
- **Repository interfaces and implementations** declare and execute database operations. Implementations use SQLAlchemy `select`, `add`, `commit`, `flush`, and `refresh` operations.
- **Schemas** validate requests and serialize selected responses. `ConfigDict(from_attributes=True)` enables serialization from ORM-style objects.
- **Dependency providers** construct services and repositories for FastAPI dependency injection. Authentication dependencies resolve the current user and check roles.
- **Core and utility modules** provide settings, JWT and password helpers, file storage, email, and logging.

The report feature has its own service and repository interfaces, implementations, dependency, schema, and router. Other existing service constructors are generally typed with concrete repository classes even though repository interfaces are present.

## Project structure

```text
.
├── alembic/
│   ├── versions/                 # Database revisions
│   ├── env.py                    # Async Alembic configuration
│   └── script.py.mako
├── app/
│   ├── api/
│   │   ├── dependencies/         # Service providers and auth dependencies
│   │   └── routers/              # HTTP endpoint modules
│   ├── core/                     # Settings and security functions
│   ├── database/                 # SQLAlchemy Base, engine, and sessions
│   ├── exceptions/               # Domain exceptions and global handlers
│   ├── middleware/               # Request logging middleware
│   ├── models/                   # SQLAlchemy table definitions
│   ├── repositories/
│   │   ├── interfaces/           # Abstract repository contracts
│   │   └── implementations/      # SQLAlchemy repository queries
│   ├── schemas/                  # Pydantic request/response models
│   ├── services/
│   │   ├── interfaces/           # Abstract service contracts
│   │   └── implementations/      # Business logic
│   ├── templates/                # HTML email templates
│   ├── utils/                    # Upload, email, startup, and logging helpers
│   └── main.py                   # FastAPI app, lifespan, router registration
├── scripts/
│   └── create_admin.py           # Local initial-admin creation script
├── tests/
│   ├── api/                      # HTTP endpoint tests
│   ├── integration/              # Repository tests against PostgreSQL
│   ├── unit/                     # Service and security tests
│   └── conftest.py               # Shared fixtures
├── uploads/                      # Runtime upload storage
├── .env.example                  # Environment variable template
├── alembic.ini
├── pytest.ini
├── requirements.txt
└── readme.md
```

Runtime logs are written under `logs/`. Uploads and logs are generated data, not source modules.

## Database design

The models define five tables. Foreign keys define the database associations; the models do not declare SQLAlchemy `relationship()` properties.

### `employees`

| Column | SQL type | Null | Key, constraint, or default |
|---|---|---:|---|
| `id` | Integer | No | Primary key |
| `employee_code` | `VARCHAR(50)` | No | Unique |
| `username` | `VARCHAR(50)` | No | Unique |
| `email` | `VARCHAR(200)` | No | Unique |
| `password` | `VARCHAR(250)` | No | Stores the password hash |
| `role` | `VARCHAR(20)` | No | Check: `admin` or `lineman` |
| `phone_number` | `VARCHAR(15)` | No | — |
| `door_no` | `VARCHAR(20)` | No | — |
| `street` | `VARCHAR(150)` | No | — |
| `district` | `VARCHAR(100)` | No | — |
| `pincode` | `VARCHAR(10)` | No | — |
| `is_active` | Boolean | No | ORM default `True` |
| `created_at` | Timezone-aware `DateTime` | No | Server default `now()` |

### `customers`

| Column | SQL type | Null | Key, constraint, or default |
|---|---|---:|---|
| `id` | Integer | No | Primary key |
| `customer_code` | `VARCHAR(50)` | No | Unique |
| `username` | `VARCHAR(50)` | No | Unique |
| `email` | `VARCHAR(200)` | No | Unique |
| `password` | `VARCHAR(250)` | No | Stores the password hash |
| `phone_number` | `VARCHAR(15)` | No | — |
| `door_no` | `VARCHAR(20)` | No | — |
| `street` | `VARCHAR(150)` | No | — |
| `district` | `VARCHAR(100)` | No | — |
| `pincode` | `VARCHAR(10)` | No | — |
| `is_active` | Boolean | No | ORM default `True` |
| `created_at` | Timezone-aware `DateTime` | No | Server default `now()` |

### `complaints`

| Column | SQL type | Null | Key, constraint, or default |
|---|---|---:|---|
| `id` | Integer | No | Primary key |
| `complaint_number` | `VARCHAR(50)` | No | Unique |
| `customer_id` | Integer | No | Foreign key to `customers.id` |
| `door_no` | `VARCHAR(20)` | No | — |
| `street` | `VARCHAR(150)` | No | — |
| `district` | `VARCHAR(100)` | No | — |
| `pincode` | `VARCHAR(10)` | No | — |
| `failure_type` | `VARCHAR(100)` | No | — |
| `description` | Text | No | — |
| `priority` | `VARCHAR(20)` | No | ORM default `NORMAL` |
| `status` | `VARCHAR(30)` | No | ORM default `PENDING`; no database enum/check constraint |
| `image_path` | `VARCHAR(250)` | Yes | — |
| `created_at` | Timezone-aware `DateTime` | No | Server default `now()` |
| `updated_at` | Timezone-aware `DateTime` | No | Server default `now()`; ORM `onupdate=now()` |

### `complaint_assignments`

| Column | SQL type | Null | Key, constraint, or default |
|---|---|---:|---|
| `id` | Integer | No | Primary key |
| `complaint_id` | Integer | No | Foreign key to `complaints.id` |
| `lineman_id` | Integer | No | Foreign key to `employees.id` (assignee) |
| `assigned_by` | Integer | No | Foreign key to `employees.id` (administrator) |
| `assigned_at` | Timezone-aware `DateTime` | No | Server default `now()` |
| `remarks` | Text | Yes | — |

There is no uniqueness constraint on complaint assignment rows, so the table can preserve multiple assignment records.

### `repair_details`

| Column | SQL type | Null | Key, constraint, or default |
|---|---|---:|---|
| `id` | Integer | No | Primary key |
| `complaint_id` | Integer | No | Unique foreign key to `complaints.id` |
| `lineman_id` | Integer | No | Foreign key to `employees.id` |
| `issue_found` | Text | No | — |
| `repair_description` | Text | No | — |
| `repair_completed_at` | Timezone-aware `DateTime` | No | Server default `now()` |
| `repair_image_path` | `VARCHAR(255)` | Yes | — |
| `remarks` | Text | Yes | — |

The unique constraint on `repair_details.complaint_id` permits at most one repair detail record per complaint.


## API reference

All paths below are mounted directly by `app/main.py`. Interactive documentation is available at `/docs` when the service is running.

### Authentication

| Method | Endpoint | Description | Access / request |
|---|---|---|---|
| `POST` | `/auth/login` | Authenticates an employee or customer; returns access and refresh tokens. The form `username` field is used as the email. | Public; OAuth2 form fields `username`, `password` |
| `POST` | `/auth/refresh` | Exchanges a refresh token for a new access token. | Public endpoint; JSON body `{ "refresh_token": "..." }` |

### Employees

| Method | Endpoint | Description | Access / request |
|---|---|---|---|
| `POST` | `/employees/` | Creates a lineman employee. | Admin; `EmployeeCreate` JSON |
| `GET` | `/employees/` | Lists employees. | Admin; `limit` defaults to 10 (1–100), `offset` defaults to 0 (minimum 0) |
| `GET` | `/employees/{employee_id}` | Gets an employee by numeric ID. | Admin |
| `DELETE` | `/employees/{employee_id}` | Deactivates an employee (soft deactivation). | Admin |

### Customers

| Method | Endpoint | Description | Access / request |
|---|---|---|---|
| `POST` | `/customers/` | Registers a customer. | Public; `CustomerCreate` JSON |
| `GET` | `/customers/` | Lists customers. | Admin; `limit` defaults to 10 (1–100), `offset` defaults to 0 (minimum 0) |
| `GET` | `/customers/{customer_id}` | Gets a customer by numeric ID. | Admin |
| `DELETE` | `/customers/{customer_id}` | Deactivates a customer (soft deactivation). | Admin |

### Complaints

| Method | Endpoint | Description | Access / request |
|---|---|---|---|
| `POST` | `/complaints/` | Registers a complaint for the authenticated customer and sends a registration email. | Customer; `ComplaintCreate` JSON |
| `GET` | `/complaints/my` | Lists complaints belonging to the authenticated customer. | Customer |
| `GET` | `/complaints/` | Lists all complaints. | Admin |
| `POST` | `/complaints/assign` | Assigns a pending complaint to an active lineman. | Admin; `AssignmentCreate` JSON |
| `GET` | `/complaints/assigned` | Lists complaints assigned to the authenticated lineman. | Lineman |
| `PATCH` | `/complaints/{complaint_id}/close` | Closes a complaint after repair completion and sends a closure email. | Admin |
| `POST` | `/complaints/{complaint_id}/image` | Uploads an image to the authenticated customer's pending complaint. | Customer; multipart field `image` |
| `PATCH` | `/complaints/{complaint_id}` | Updates an authenticated customer's pending complaint. | Customer; `ComplaintUpdate` JSON |

### Repairs

| Method | Endpoint | Description | Access / request |
|---|---|---|---|
| `POST` | `/repairs/{complaint_id}/complete` | Records repair details for a complaint assigned to the lineman. | Lineman; `RepairCreate` JSON |
| `POST` | `/repairs/{complaint_id}/image` | Uploads an image for a completed repair. | Lineman; multipart field `image` |
| `GET` | `/repairs/` | Lists all repair details. | Admin |

### Reports and health

| Method | Endpoint | Description | Access / request |
|---|---|---|---|
| `GET` | `/reports/complaints/statistics` | Returns total complaint count and counts for pending, assigned, repair-completed, closed, and rejected statuses. | Admin |
| `GET` | `/health/` | Executes `SELECT 1` and reports application/database status. | Public |

The statistics response is shaped as follows; values are calculated from the database:

```json
{
  "total_complaints": 0,
  "pending": 0,
  "assigned": 0,
  "repair_completed": 0,
  "closed": 0,
}
```

## Authentication and security

- Login uses FastAPI's `OAuth2PasswordRequestForm` and `OAuth2PasswordBearer`. The login `username` is treated as an email address. Employee lookup is attempted first; if no employee is found, the service tries customer login.
- Passwords are hashed and checked using `pwdlib.PasswordHash.recommended()`. Raw passwords are not returned by the response schemas.
- PyJWT creates signed access and refresh tokens using `JWT_SECRET_KEY` and `JWT_ALGORITHM` from settings. Tokens contain `sub`, `user_type`, `token_type`, and `exp`; employee tokens also contain `role`.
- Access-token expiration uses `ACCESS_TOKEN_EXPIRE_MINUTES`; refresh-token expiration uses `REFRESH_TOKEN_EXPIRE_DAYS`. Token decoding verifies the signature, algorithm, and expiration.
- `get_current_employee` and `get_current_customer` check token type, user type, account existence, and `is_active`. `required_admin` and `required_lineman` then check the employee role.
- Pydantic validates request fields such as email, phone number, pincode, minimum string lengths, and positive assignment IDs.
- Customer and employee deactivation updates `is_active`; it does not delete the record.
- Secrets and database connection fields are read by `pydantic-settings` from environment variables and `.env`. Do not commit a populated `.env` file or copy credentials into documentation.

Example decoded token claims (illustrative only):

```json
{
  "sub": "42",
  "user_type": "employee",
  "token_type": "access",
  "role": "lineman",
  "exp": 1999999999
}
```

## File uploads and email

### Image uploads

`app/utils/file_upload.py` accepts the filename extensions `.jpg`, `.jpeg`, and `.png`, generates a UUID filename, reads in 1 MiB chunks, and rejects files larger than the configured `MAX_FILE_SIZE`. It uses `aiofiles` for writing and FastAPI's `UploadFile` for multipart data. The stored path is written to `complaints.image_path` or `repair_details.repair_image_path` by the corresponding service/repository.

There are two configuration values, `COMPLAINT_UPLOAD_DIR` and `REPAIR_UPLOAD_DIR`, but the current upload utility builds its output path from the complaint directory global even when called with the repair directory. It creates the passed directory but still writes the file to the complaint directory. The extension is checked, but the implementation does not inspect the file's actual MIME type or decode its image contents. The upload error message says 5 MB while the enforced size is determined by `MAX_FILE_SIZE`; set that value in bytes and keep the setting and message aligned operationally.

### Email notifications

The service sends a registration email after complaint creation and a closure email after closing. `app/utils/email.py` renders `complaint_registered.html` and `complaint_closed.html` with Jinja2, then sends multipart plain-text/HTML email through SMTP using `smtplib` and `EmailMessage`. Calls from the asynchronous complaint service are passed through Starlette's `run_in_threadpool` so synchronous SMTP work does not block the event loop. Email exceptions are caught and logged inside `send_email`; they do not propagate as a failed complaint API operation.

SMTP host, port, username, password, and sender address are environment settings. Their values are intentionally not reproduced here.

## Exceptions, logging, and startup

`BaseCustomException` carries a message and HTTP status. Domain-specific exceptions cover employees, customers, complaints, assignments, and repairs. Registered handlers normalize custom exceptions and HTTP exceptions to a response with `success` and `message`; validation errors include an `errors` array. SQLAlchemy errors and uncaught exceptions return a generic HTTP 500 response, with details logged server-side.

`setup_logging()` configures the root Python logger at `INFO`, with a console handler and a `RotatingFileHandler` at `logs/app.log`. The file rotates at 5 MiB and keeps three backups. `RequestLoggingMiddleware` logs the HTTP method, path, response status, and elapsed time for a returned response. Exception handlers log database and unexpected errors.

The FastAPI lifespan logs startup, checks for an active admin account, yields to serve requests, disposes the SQLAlchemy engine at shutdown, and logs completion. It does not create tables; apply Alembic migrations separately. The health check performs a database query and returns a `503` response if SQLAlchemy raises a database error.

## Configuration and migrations

`Settings` declares required database, JWT, upload, SMTP, and token-expiration fields and reads them from the process environment or `.env`. `TEST_DATABASE_URL` is optional to the application settings but required by the integration test fixture. The main database URL is assembled as `postgresql+asyncpg://...` from `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`.

`app/database/database.py` creates an async SQLAlchemy engine and `AsyncSession` factory (`SessionLocal`). `get_db()` yields a session from an async context manager. The session factory has `expire_on_commit=False` and `autoflush=False`.

Alembic is configured in `alembic.ini`; `alembic/env.py` imports the models, uses `Base.metadata`, reads the database settings, and runs migrations through an async engine. Existing revisions create the core tables and then simplify `repair_details` to match the current model.

From the repository root, the common migration commands are:

```powershell
alembic revision --autogenerate -m "describe schema change"
alembic upgrade head
alembic downgrade -1
```

Review generated migrations before applying them. The latest migration has an unnamed unique constraint and its downgrade attempts to drop that constraint without a name, so that downgrade path should be reviewed before use.

## Testing

The current test tree contains **21 unit test functions, 7 integration test functions, and 28 API test functions**. These are counts of test definitions, not a coverage percentage or a claim that every test has passed.

### Unit tests

Unit tests cover employee and customer service creation/deactivation rules, complaint assignment and update rules, repair completion and upload service behavior, employee/customer login and token refresh, password hashing, and JWT access/refresh token utilities. Repository methods are mocked with `AsyncMock`; the shared `mock_repository` fixture builds these methods. Email calls are replaced with `MagicMock`, and upload utilities with `AsyncMock` through `monkeypatch`.

### Integration tests

Integration tests use actual repository implementations with asynchronous SQLAlchemy sessions against PostgreSQL. They cover employee/customer repository operations, complaint CRUD, assignment queries, repair persistence, report aggregation, and zero counts. The `db_engine` fixture creates the model tables before a test and drops them afterward. `TEST_DATABASE_URL` is checked to ensure it uses PostgreSQL and does not identify the same host, port, and database name as the configured application database. Use a disposable test database: the fixture drops all mapped tables during cleanup.

The test URL is mandatory for integration tests; `tests/conftest.py` fails if it is missing or points to the configured application database. Integration tests are not skipped when the setting is absent.

### API tests

API tests use `httpx.AsyncClient` with `httpx.ASGITransport`. The shared client fixture overrides `get_db`; endpoint tests override service providers and auth dependencies where needed. Tests cover login/refresh, customer registration and validation, employee and customer management, complaint workflows, repair endpoints, health, report counts response shape, and report authorization for admin, lineman, customer, and unauthenticated requests.

The complaint image upload endpoint `/complaints/{complaint_id}/image` currently has no API test. The test suite does not claim complete endpoint coverage.

### Fixtures and commands

`tests/conftest.py` supplies the app/client, test engine/session, sample admin/lineman/customer, access token, mock repository, and mocked email/upload operations. Fixture cleanup is done with `yield` where a resource needs teardown. Pytest runs in `asyncio_mode=auto`; the current pytest-asyncio version may emit a loop-scope deprecation warning because the default fixture loop scope is not explicitly configured.

```powershell
# All tests (requires TEST_DATABASE_URL because integration tests are included)
pytest
pytest -v
pytest -v -rs

# Individual categories
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/api/ -v


## Python and software engineering concepts

- **Classes and inheritance:** Models, services, repositories, and utilities are classes. Service/repository implementations inherit abstract base-class contracts.
- **Abstraction:** `ABC` and `@abstractmethod` define service and repository interfaces.
- **Constructor dependency injection:** Service constructors receive repository objects. FastAPI dependency provider functions construct and supply the service graph.
- **Type hints and validation:** The code uses annotations, `Annotated`, optional types such as `str | None`, SQLAlchemy `Mapped` columns, and Pydantic `Field` constraints.
- **Asynchronous programming:** Routers, services, repositories, database sessions, and upload functions use `async`/`await`. Async context managers manage sessions and database connections. Synchronous SMTP operations are delegated with `run_in_threadpool`.
- **Decorators:** FastAPI route decorators register endpoints; `Depends` declares dependency resolution; pytest decorators mark asynchronous/category tests.
- **Exception handling:** Domain errors are raised in services and converted centrally into HTTP responses. The repair completion service rolls back the session if its database operation raises.
- **Database transactions:** Repository writes commit and refresh rows; repair creation flushes before the service commits the repair and status change together.
- **Other Python tools:** UUIDs generate employee/customer/complaint identifiers and upload filenames. Context managers manage SMTP and database resources. Logging records operational events. SQLAlchemy filtering, joins, and conditional aggregate expressions perform query work in the database.

## Local setup (Windows PowerShell)

### 1. Create and activate an environment

Use Python 3.10 or newer (the source uses modern union type syntax). From the repository root:

```powershell
python -m venv .myvenv
.\.myvenv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Create a PostgreSQL database

Create a local PostgreSQL database using your preferred PostgreSQL client. For example, in `psql`:

```sql
CREATE DATABASE eb_management;
CREATE DATABASE eb_management_test;
```

The test database must be separate and disposable because the integration fixture creates and drops the model tables.

### 3. Configure environment variables

Copy `.env.example` to `.env` and replace all placeholders with local values. Never commit `.env` or use development credentials in production.

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_development_database
DB_USER=your_postgres_user
DB_PASSWORD=database_password

JWT_SECRET_KEY=secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=integer_minutes
REFRESH_TOKEN_EXPIRE_DAYS=integer_days

COMPLAINT_UPLOAD_DIR=uploads/complaints
REPAIR_UPLOAD_DIR=uploads/repairs
MAX_FILE_SIZE=size_in_bytes

SMTP_HOST=smtp_host
SMTP_PORT=integer_port
SMTP_USERNAME=smtp_username
SMTP_PASSWORD=smtp_password
SMTP_FROM_EMAIL=sender_address

TEST_DATABASE_URL=postgresql+asyncpg://your_postgres_user:replace_with_password@localhost:5432/eb_power_failure_test
```

`TEST_DATABASE_URL` must point to a database distinct from the configured application database.

### 4. Apply migrations and create an administrator

```powershell
alembic upgrade head
```

Review and replace the local default account values in `scripts/create_admin.py`, then run the script from the project root:

```powershell
python -m scripts.create_admin
```

The script checks for an existing employee with its configured admin email or username before inserting. Do not use its embedded defaults outside a controlled local setup.

### 5. Start the API

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI. The health route is `http://127.0.0.1:8000/health/`.

### 6. Run integration tests

Ensure `.env` contains a valid `TEST_DATABASE_URL` for the isolated test database. Then run:

```powershell
pytest tests/integration/ -v
```

### 7. Code Linting and Formatting (Ruff)

## Check for linting issues
```powershell
ruff check .
```

## Automatically fix fixable linting issues
```powershell
ruff check . --fix
```
## Format Python code
```powershell
ruff format .
```
