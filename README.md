# Gradebook

A small web application for lecturers to manage course assessments and grades,
and for students to view their own results. The MVP uses the Swiss 1–6 grading
scale and weighted assessments.

This is the final project for FHGR CDS212 DevOps. Its main objective is to
demonstrate a reproducible workflow from Git and automated tests through
containerization, deployment, and monitoring.

## Current status

The repository contains project planning, documentation CI, and a minimal Flask
application with a `/health` endpoint. The project owner verified the expected
response in the browser and reported two passing automated tests, including a
temporary failing assertion followed by a successful repair. Python linting and
coverage checks passed locally and on GitHub. The owner supplied screenshots
showing that a failed required lint check blocked merging and that fixing the
violation restored passing checks and an enabled merge button.
The weighted-grade calculation and validated models were merged in PRs #3–#4.
In-memory operations now enforce relationships, course ownership, enrollment,
grade corrections, and access to student results. The owner reports local lint,
formatting, and coverage-enabled tests passed, and PR #5 was merged.
The operational-endpoints branch connects one repository to each Flask app and
adds `/ready` and `/metrics`. The owner reports passing local lint, formatting,
and coverage-enabled tests, and verified all three endpoints in the browser,
including an increasing request counter. PR #6 was merged.
The authentication branch adds a login form, signed sessions, and logout for
demo accounts configured through environment variables. The owner verified both
roles and logout in the browser and reported 99% line coverage. GitHub CI for
authentication is pending. Gradebook HTTP endpoints, database
persistence, and deployment are not implemented.

## Agreed application scope

- Courses, enrolled students, assessments, and grades.
- Assessment weights totaling 100% for a complete course result.
- Grades from 1 to 6 with up to two decimal places.
- Weighted averages displayed to two decimal places, rounding halfway upward.
- Incomplete results when grades are missing; no final result while weights do
  not total 100%.
- Lecturer access to their own courses and student access to their own results.
- Username/password login with pre-created accounts and hashed passwords.
- Synthetic demonstration data; no public registration or password recovery.

See [project scope](docs/PROJECT_SCOPE.md) for detailed rules and acceptance
examples. These describe planned behavior, not already available features.

## Repository setup

Prerequisite: Git. To obtain a local copy:

```text
git clone https://github.com/nadlerfabian/devops-gradebook.git
cd devops-gradebook
```

If the repository is already cloned, use the existing checkout.

### Local development (PowerShell, Python 3.12)

The project owner verified installation and startup in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m flask --app wsgi run --port 8000
```

Create the environment only once; activate it in each new terminal session.
Open `http://127.0.0.1:8000/health`. With no `APP_VERSION` environment variable,
the expected JSON is `{"status":"ok","version":"0.0.0-dev"}`. Press Ctrl+C in
the server terminal to stop it. The Flask development server is for local use;
production startup will be added with containerization.

### Operational endpoints

| Endpoint | Purpose | Response |
|---|---|---|
| `/health` | Process liveness, independent of storage | 200, status and version |
| `/ready` | Storage availability | 200 ready; 503 not_ready on failure |
| `/metrics` | Prometheus HTTP measurements | 200, Prometheus text format |

In-memory storage is ready without a database. The readiness route calls the
repository's `healthy()` method; a later PostgreSQL backend must actually check
database connectivity. Exceptions produce a generic 503 response and log message.

`app/monitoring.py` records `flask_http_request_total` and
`flask_http_request_duration_seconds` (histogram buckets, count, and sum).
Labels identify the HTTP method, route template, and response status. Status
labels allow error rates to be calculated; histogram buckets support latency
percentiles later in Prometheus. Unknown URLs share `unmatched`, unusual methods
share `OTHER`, and raw URLs/query strings are never labels. Metrics scrapes are
excluded from application traffic. Each app instance has its own registry.

Storage and metrics are process-local. Use one worker for the in-memory version;
shared database storage and metrics support for multiple workers need separate
implementation before increasing the worker count.

### Login

See [authentication setup and design](docs/AUTHENTICATION.md) for PowerShell
commands to configure the signing key and synthetic demo passwords. Open
`/auth/login` to sign in and `/auth/me` to see the account's role.

### Automated tests

With the virtual environment active, install development dependencies and run:

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest
```

`requirements-dev.txt` includes the application's runtime requirements and pytest.
The tests use Flask's test client, so no running server is required. They check
the health response with both the default version and an environment-supplied
version. The project owner reported `2 passed` both before and after coverage
tooling was added, and demonstrated a deliberate assertion failure and repair.
The owner reported 40 passing tests at the weighted-grades milestone. Later
changes add model, repository, readiness, and metrics tests. Run the commands
below for the current count and coverage. The owner reports passing local
operational-endpoint checks, and PR #6 was merged. Authentication adds further
tests. The owner reported 99% line coverage for the application.

### Weighted-grade calculation

`app/grading.py` implements the agreed calculation independently of HTTP and
storage. For example:

```python
from decimal import Decimal

from app.grading import AssessmentGrade, calculate_weighted_average

assessments = [
    AssessmentGrade(grade=Decimal("5.0"), weight=Decimal("40")),
    AssessmentGrade(grade=Decimal("4.0"), weight=Decimal("60")),
]
result = calculate_weighted_average(assessments)
print(result)  # 4.40
```

Invalid grades or weights raise `ValueError`; missing grades, no assessments,
or weights not totaling 100% return `None` (incomplete). Valid results are
rounded to two decimals with halfway values rounded upward. The core requires
explicit decimal inputs; HTTP input parsing will be introduced later.
See [ADR 0001](docs/adr/0001-decimal-grade-calculation.md) for the reasoning and
trade-offs.

### Python quality checks

After installing the updated development dependencies, run:

```powershell
python -m ruff check .
python -m ruff format --check .
python -m pytest --cov=app --cov-report=term-missing
```

Ruff checks Python errors/style and formatting. Coverage measures executed lines
in the `app` package; the test command fails below 80%. This does not measure
whether every requirement is tested or include the `wsgi.py` entry point.
The project owner verified these checks locally: Ruff passed, all four Python
files were already formatted, and both initial health tests passed. The new
grading module's local checks also passed: six Python files already formatted,
40 tests passed, and 100% line coverage of the current `app` package (minimum
gate: 80%). This is not evidence of coverage for future gradebook features.
The owner supplied evidence of passing Documentation, Lint, and Test checks on
GitHub for the foundation PR; subsequent grading, model, and storage PRs were merged.

The GitHub workflow runs Documentation, Lint (ruff), and Test (Python 3.12) jobs
independently. Python jobs install dependencies on fresh Ubuntu runners using
Python 3.12 and pip caching. A successful test job saves `coverage.xml` as the
downloadable `coverage-report` artifact. Docker build/scanning jobs will be added
when a Dockerfile exists.

## Documentation and workflow

- [Project scope](docs/PROJECT_SCOPE.md)
- [Data model and planned relationship rules](docs/DATA_MODEL.md)
- [Authentication setup and design](docs/AUTHENTICATION.md)
- [Course acceptance criteria](docs/requirements/ACCEPTANCE_CRITERIA.md)
- [Course source review](docs/requirements/SOURCE_REVIEW.md)
- [Contribution and pull request workflow](CONTRIBUTING.md)
- [CI gate demonstration evidence](docs/evidence/README.md)
- [ADR 0001: decimal grade calculation](docs/adr/0001-decimal-grade-calculation.md)
- [ADR 0002: in-memory repository](docs/adr/0002-in-memory-repository.md)

Changes use short-lived branches and pull requests into `main`. The project's
course checklist requires at least five merged PRs with meaningful descriptions
and passing CI. The owner's PR screenshots show Documentation, Lint (ruff), and
Test (Python 3.12) as required checks, with merging blocked while lint fails.
Keep these required checks enabled for future application changes.
Required operational endpoints are
`/health`, `/ready`, and `/metrics` on port 8000.

## Author and AI assistance

GitHub project owner: [nadlerfabian](https://github.com/nadlerfabian).

Codex assisted with reviewing the local course material, compiling the
requirements, drafting repository documentation, and writing the initial Flask
application skeleton, grading, validated models, in-memory storage, operational
endpoints, authentication, tests, and
decision records for explanation and review.
The project owner reviews decisions and performs setup, Git, and operational
steps with explanations. This declaration will be updated as the project grows.

## License

[Apache License 2.0](LICENSE).
