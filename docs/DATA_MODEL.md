# Gradebook data model

The records in `app/models.py` define the shape of the app's data. This change
does not yet store records or expose them through HTTP. The project owner
reports that local lint, formatting, and the coverage-enabled test suite passed
after adding these models and extracting shared grading validators. GitHub CI
verification for this change is pending.

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

## Rules for the next storage step

A single record cannot verify whether a related record exists. The repository
and service layer must enforce these rules across the stored records:

- Usernames are unique.
- A course owner exists and is a lecturer.
- An assessment's course exists.
- An enrollment links an existing course to an existing student-role user.
- Duplicate enrollment does not create multiple relationships.
- A grade's student is enrolled in the assessment's course.
- Correcting a grade replaces the value for the same assessment/student pair.
- Only the owning lecturer may manage the course and its records; students
  can read only their own authorized results.

These are expected behavior for later work, not implemented guarantees of the
current dataclasses. The first implementation will use in-memory storage,
followed by PostgreSQL through a compatible storage interface.
