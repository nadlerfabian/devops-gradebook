# Gradebook

A small web application for lecturers to manage course assessments and grades,
and for students to view their own results. The MVP uses the Swiss 1–6 grading
scale and weighted assessments.

This is the final project for FHGR CDS212 DevOps. Its main objective is to
demonstrate a reproducible workflow from Git and automated tests through
containerization, deployment, and monitoring.

## Current status

The repository currently contains project planning and requirements. The
application, login, database, CI pipeline, and deployment are not implemented
yet. No runnable application quick start is available at this stage.

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

If the repository is already cloned, use the existing checkout. Application
dependencies and verified run/test commands will be documented as they are added.

## Documentation and workflow

- [Project scope](docs/PROJECT_SCOPE.md)
- [Course acceptance criteria](docs/requirements/ACCEPTANCE_CRITERIA.md)
- [Course source review](docs/requirements/SOURCE_REVIEW.md)
- [Contribution and pull request workflow](CONTRIBUTING.md)

Changes use short-lived branches and pull requests into `main`. The project's
course checklist requires at least five merged PRs with meaningful descriptions
and passing CI; workflow configuration and branch protection still need to be
established. Required operational endpoints are `/health`, `/ready`, and
`/metrics` on port 8000.

## Author and AI assistance

GitHub project owner: [nadlerfabian](https://github.com/nadlerfabian).

Codex assisted with reviewing the local course material, compiling the
requirements, and drafting the project scope and repository documentation.
The project owner reviews decisions and performs setup, Git, and operational
steps with explanations. This declaration will be updated as the project grows.

## License

[Apache License 2.0](LICENSE).
