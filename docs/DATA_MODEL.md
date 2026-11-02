# Gradebook data model

The records in `app/models.py` define the shape of the app's data. The models
were merged in PR #4 after the owner reported green CI. In-memory storage is
now implemented in `app/repository.py`. The owner reports that local lint,
formatting, and coverage-enabled tests passed, and PR #5 was merged.
The operational-endpoints branch connects storage to Flask readiness checking;
login sessions and gradebook HTTP routes are not yet implemented.

## Records and identifiers

| Record | Fields | Relationship |
|---|---|---|
| User | id, username, role, password_hash | Role is lecturer or student |
| Course | id, name, lecturer_id | Owned by a lecturer user |
| Assessment | id, course_id, name, weight | Belongs to one course |
| Enrollment | course_id, student_id | Connects a student user to a course |
| Grade | assessment_id, student_id, value | One value per student/assessment pair |

A student uses their account's user ID as their student ID. A separate student
profile is unnecessary for this MVP: enrollment and grades refer directly to
that account. Course ownership similarly references a lecturer account's ID.

Assessment weights are shared by the enrolled students; grade values belong to
individual students. A missing grade is represented by no Grade record, and
will be translated to `None` for the calculation function. It is not a zero.

## Validation in each record

All records are immutable Python dataclasses. `__post_init__` validates them
when constructed. Changes will replace a stored record with a validated new
record rather than bypassing checks by assigning fields afterward.

- IDs must be positive integers; booleans and numeric strings are rejected.
- Usernames, course/assessment names, and password-hash fields cannot be blank.
- The core requires explicit `Role` values and explicit `Decimal` values.
- Grades and assessment weights reuse `validate_grade` and `validate_weight`
  from `app/grading.py`, avoiding a second implementation of those rules.
- Assessment weights need not yet total 100% when creating individual records;
  the calculation decides whether a final result is available.
- User object representations omit the password-hash field. This is not a safe
  public serialization format: future responses must explicitly select fields.

The User model holds a hash but does not generate or verify one. Future account
provisioning must generate real password hashes. Model-test placeholders are
not usable login credentials. Login and session handling remain unimplemented.

## Relationship and access rules in storage

A single record cannot verify whether a related record exists. The in-memory
repository implements these rules across the stored records:

- Usernames are unique.
- A course owner exists and is a lecturer.
- An assessment's course exists.
- An enrollment links an existing course to an existing student-role user.
- Duplicate enrollment does not create multiple relationships.
- A grade's student is enrolled in the assessment's course.
- Correcting a grade replaces the value for the same assessment/student pair.
- Only the owning lecturer may manage the course and its records; students
  can read only their own authorized results.

These guarantees come from repository operations, not the dataclasses alone.
Tests exercise successful operations, denied operations, cross-course isolation,
duplicate enrollment, and grade correction; the owner reports local tests pass.

## In-memory repository

`InMemoryGradebookRepository` keeps records in private Python dictionaries.
It allocates user/course/assessment IDs. Enrollment keys are `(course_id,
student_id)`; grade keys are `(assessment_id, student_id)`. Re-enrollment returns
the existing enrollment, while a valid correction replaces a grade under the
same key. Invalid corrections leave the previous grade intact.

Public application operations include creating/listing courses and assessments,
enrolling students, listing enrollments, recording/correcting grades, reading
authorized grade lists, and calculating a student's average. The average is
computed from current records using the existing calculation function; it is
not a separately stored value that could become stale after correction.

Names/IDs/grade values are validated through the existing models. Usernames are
unique by exact string equality in this internal implementation. Username
normalization and login lookup will be specified with authentication.

Internal account provisioning uses `create_user` and accepts an already created
password hash; it does not hash passwords or expose public registration. Tests
use placeholder hashes, not usable credentials.

Operations take an `actor_id`. This must come from a trusted authenticated
session in future HTTP routes. Accepting a client-supplied actor ID would let a
caller impersonate another user; permission checks alone are not authentication.
Login, sessions, and safe response serialization are not yet implemented.

A reentrant lock keeps operations coherent between threads in one process.
Returned records are immutable, and returned lists are new lists, so callers
cannot change stored records by editing a list result. Private storage is an
internal implementation detail, not an API for routes to access directly.

Errors distinguish missing records (`LookupError`), forbidden operations
(`PermissionError`), and invalid/conflicting input (`ValueError`). HTTP routes
will map these to appropriate status codes without exposing internal data.

Every repository instance starts empty. All records disappear when that
instance/process ends; separate workers or replicas do not share records.
Use a single shared repository instance per application while developing in
memory, and one worker. PostgreSQL will later supply shared persistent storage
behind compatible operations. The `healthy()` method currently returns True
because there is no external database. The operational-endpoints branch wires
one repository into `app.extensions["repository"]` per Flask app. `/ready` calls
its `healthy()` method, returning 503 for an unavailable dependency or exception;
`/health` remains independent of storage. The owner reports passing local tests,
lint, formatting, and browser checks; GitHub CI for this integration is pending.

See [ADR 0002](adr/0002-in-memory-repository.md) for alternatives and limitations.
