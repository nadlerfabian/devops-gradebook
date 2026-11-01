# 0002 — In-memory repository before PostgreSQL

## Status

Accepted, 1 November 2026. Local lint, formatting, and coverage-enabled tests
passed according to the project owner. CI for this change is pending.

## Context

The application needs to connect courses, assessments, enrollments, and student
grades. Individual model validation cannot establish that related records
exist or that the current lecturer owns a course.

The course requires an in-memory mode without `DATABASE_URL`, and PostgreSQL
for persistent storage. We are implementing incrementally so the rules can be
understood and tested before introducing database operations and HTTP routes.

## Decision

Implement `InMemoryGradebookRepository` with explicit operations for account
provisioning, courses, assessments, enrollment, grades, and authorized result
reads. Use the existing immutable models and calculation functions.

Keep records in private dictionaries owned by each repository instance.
Use `(course_id, student_id)` as the enrollment key and
`(assessment_id, student_id)` as the grade key. Repeated enrollment returns the
existing record. A grade correction validates the replacement before storing
it, so an invalid correction cannot erase an existing valid grade.

Apply relationship and role/ownership checks inside the operations. Future
HTTP routes must use these operations and obtain the acting user ID from the
authenticated session. They must not accept a client-supplied actor ID as proof
of identity or access the dictionaries directly.

Return new lists of immutable records and use a reentrant lock to coordinate
operations across threads within one process. Calculate averages from current
assessment/grade records rather than storing a cached average.

PostgreSQL remains required later. Its implementation must preserve these
observable rules; shared policy code may be extracted to avoid maintaining
different authorization behavior in the two backends. A formal storage protocol
and environment-based backend selection are not implemented in this change.

Alternatives considered:

- Persist directly from Flask routes: couples HTTP handling to storage and
  makes relationship/permission tests depend on the web layer.
- Start with PostgreSQL immediately: provides persistence, but introduces
  database setup before the behavioral contract has been exercised locally.
- Use a JSON file: adds file synchronization and durability concerns and does
  not replace the required PostgreSQL implementation.

## Consequences

Positive:

- Core operations and denied-access cases are testable without a live server
  or database.
- Each test can use a fresh repository instance with isolated synthetic data.
- Enrollment and grade keys prevent duplicate relationships within an instance.
- Grade corrections immediately affect results because averages are calculated
  from current records.

Trade-offs and limits:

- Data is lost when the repository instance/process ends. Workers and replicas
  do not share it. In-memory app operation will require one repository instance
  per application and one worker.
- The lock coordinates threads only; it supplies no cross-process protection
  or database transactions.
- The repository checks authorization for the supplied actor but does not
  authenticate that actor. Login/session handling is still needed.
- Account provisioning expects a password hash; it does not generate or verify
  hashes. Model-test placeholders are not usable credentials.
- Usernames currently use exact string equality. Login normalization and safe
  response serialization remain work for the authentication/API implementation.
- The repository is not yet injected into Flask. Readiness, backend selection,
  HTTP error mapping, and PostgreSQL persistence remain separate work.
