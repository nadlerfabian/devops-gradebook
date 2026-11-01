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
coverage checks passed locally; their GitHub Actions configuration is awaiting
its first run on this branch.
Login, grading, database storage, `/ready`, `/metrics`, and deployment are not
implemented yet.

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
files were already formatted, and both tests passed with 100% line coverage of
the current small `app` package (minimum gate: 80%). This is not evidence of
coverage for future gradebook features. GitHub CI verification is still pending.

The GitHub workflow runs Documentation, Lint (ruff), and Test (Python 3.12) jobs
independently. Python jobs install dependencies on fresh Ubuntu runners using
Python 3.12 and pip caching. A successful test job saves `coverage.xml` as the
downloadable `coverage-report` artifact. Docker build/scanning jobs will be added
when a Dockerfile exists.

## Documentation and workflow

- [Project scope](docs/PROJECT_SCOPE.md)
- [Course acceptance criteria](docs/requirements/ACCEPTANCE_CRITERIA.md)
- [Course source review](docs/requirements/SOURCE_REVIEW.md)
- [Contribution and pull request workflow](CONTRIBUTING.md)

Changes use short-lived branches and pull requests into `main`. The project's
course checklist requires at least five merged PRs with meaningful descriptions
and passing CI. Documentation CI is configured; the owner reports that `main`
protection requires pull requests and the Documentation check. After their first
successful run, add the Lint (ruff) and Test (Python 3.12) checks to branch
protection before merging application changes. Required operational endpoints are
`/health`, `/ready`, and `/metrics` on port 8000.

## Author and AI assistance

GitHub project owner: [nadlerfabian](https://github.com/nadlerfabian).

Codex assisted with reviewing the local course material, compiling the
requirements, drafting repository documentation, and writing the initial Flask
application skeleton for explanation and review.
The project owner reviews decisions and performs setup, Git, and operational
steps with explanations. This declaration will be updated as the project grows.

## License

[Apache License 2.0](LICENSE).
