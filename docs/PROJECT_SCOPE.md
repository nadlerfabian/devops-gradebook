# Gradebook project scope

Status: agreed MVP requirements; initial application foundation is in progress.
The `/health` foundation passed local and GitHub checks. Weighted-grade
calculation and its validation/rounding tests now pass locally; CI for that
change is pending. Course/student APIs, login, and persistence are not yet
implemented.

This project is a small web application for managing course grades, built for
the FHGR CDS212 DevOps final project. The main deliverable is a reproducible
development, testing, deployment, and monitoring workflow around the application.
See the [course acceptance criteria](requirements/ACCEPTANCE_CRITERIA.md).

## Confirmed decisions

- Use the Swiss grading scale, from 1 to 6.
- Support weighted assessments: each assessment contributes a percentage of the
  course result, such as project 40% and exam 60%.

For a complete set of grades, the weighted average is:

`weighted average = sum(grade × weight percentage / 100)`

Example: project grade 5.0 at 40% and exam grade 4.0 at 60% give
`5.0 × 0.40 + 4.0 × 0.60 = 4.4`.

### Confirmed permissions

| Action | Lecturer | Student |
|---|---|---|
| Configure courses, assessments, and weights | Own courses only | Denied |
| Manage student enrollment | Own courses only | Denied |
| Enter or correct grades | Own courses only | Denied |
| View student grades and course averages | Students in own courses | Own results only |
| View assessment weights | Own courses | Enrolled courses only |

These permissions are agreed requirements, not yet implemented behavior.
Access restrictions must be enforced by the server, including direct API
requests, rather than only by hiding controls in the web interface.
Each student account must be linked to its student record so that the server
can enforce access to that student's own results.

### Confirmed login approach

- Users sign in with a username and password.
- Lecturer and student accounts are pre-created; there is no public registration
  or password-recovery feature in the MVP.
- Passwords are stored as hashes, never as plaintext.
- Demonstration accounts and student data are synthetic. Real passwords and
  deployment secrets must not be committed to Git.
- The server determines a signed-in user's identity and role; a user cannot
  grant themselves lecturer access by changing a request parameter.

Account provisioning and session handling will be specified during technical
design. The login approach above is agreed, not implemented or security-tested.

## MVP capabilities

### Data and capabilities

- Courses group assessments and enrolled students.
- Each assessment has a name and a percentage weight within its course.
- Each student can have one grade per assessment.
- Lecturers can enter and correct grades, and view course results.
- Students can view their own grades, assessment weights, and course results.
- Demonstration data is synthetic.

### Grading rules

- Grades must be numeric and within the inclusive range 1–6.
- Accept grades with up to two decimal places, such as `4.75`; reject excess
  precision instead of silently changing the entered grade.
- Assessment weights must be positive and total 100% for a course result to be
  calculated. Courses may be saved while assessments are configured gradually;
  a weight total other than 100% prevents a final result from being calculated.
- Missing grades are shown as incomplete; they are not treated as zero or
  silently omitted from the final result.
- Calculate a final average only when all required grades exist and the course
  weights total 100%.
- Retain calculation precision and round the displayed average to two decimal
  places. At an exact halfway value, round upward: `4.445` becomes `4.45`.
  Use decimal arithmetic so binary floating-point approximation does not change
  the intended result.
- Do not automatically round a result to a half-grade or apply an institution's
  pass/fail policy without agreeing on that policy.

### Deferred extensions

Public registration and password recovery are excluded from the agreed login
scope. Email notifications, file uploads, exports, and advanced reporting have
not been requested and remain possible extensions after the required DevOps
workflow is complete.

## Acceptance examples to develop into tests

These are expected outcomes to verify once the application exists, not passing
test results.

| Scenario | Expected outcome |
|---|---|
| Grade 5.0 at 40% plus grade 4.0 at 60% | Average 4.4, displayed as 4.40 |
| Grade 4.44 at 50% plus grade 4.45 at 50% | Exact average 4.445, displayed as 4.45 |
| Grade 1 or grade 6 | Accepted |
| Grade below 1 or above 6 | Rejected |
| Entered grade 4.755 | Rejected: more than two decimal places |
| Zero or negative assessment weight | Rejected |
| Missing an assessment grade | Final result is Incomplete |
| Course configured with weights totaling 90% | Configuration can be saved; no final result is calculated |
| Student attempts to change grades | Denied by the server |
| Student requests another student's results | Denied by the server |
| Lecturer requests or changes another lecturer's course grades | Denied by the server |
| Lecturer corrects a grade in their own course | Saved and result recalculated according to completion/weight rules |
| Valid pre-created account signs in | Access according to its assigned role |
| Invalid username/password combination | Access denied |

## Collaboration and attribution

The project owner performs terminal, setup, Git, and operational steps with
explanations and guidance. Code and configuration are reviewed and explained
as the project develops. No completion of a checklist item is claimed without
verification evidence.

AI assistance: Codex helped compile the course requirements and draft this
scope document from the project discussion. Update the project's AI-use
declaration as further work is completed.
