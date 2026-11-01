# 0001 — Decimal arithmetic for weighted grades

## Status

Accepted, 1 November 2026. Implements the grading and rounding rules agreed with
the project owner. Local verification is recorded below; CI for this change is
pending.

## Context

Grades use the Swiss 1–6 scale, accept up to two decimal places, and contribute
percentage weights to a course result. A complete result requires all grades
and weights totaling exactly 100%. Displayed averages round to two decimals,
with halfway values rounded upward.

Binary floating-point numbers do not represent every decimal fraction exactly.
Using them can alter a boundary comparison or rounding result. For example, the
agreed rounding example must produce 4.45 from an exact average of 4.445.

## Decision

Use Python's standard-library `Decimal` for grades, percentage weights, and
arithmetic. Construct values from strings rather than binary floats. Use a
local decimal context with sufficient precision for the supplied weights and
summation, and apply `ROUND_HALF_UP` only to the final two-decimal result.

Keep the calculation in `app/grading.py`, separate from HTTP routes and storage.
Each input is an immutable `AssessmentGrade` containing a decimal grade (or
`None` when missing) and a decimal percentage weight.

Invalid grades/weights raise `ValueError`. An empty course, missing grades, or
weights not totaling 100% returns `None` to indicate an incomplete result.
Validate all supplied values before returning an incomplete result so invalid
data is not hidden by an unrelated missing grade or unfinished weight total.

Alternatives considered:

- Binary `float`: convenient, but its representation and default rounding do
  not directly express our exact-decimal and halfway-up requirements.
- Integer hundredths: viable for two-decimal grades, but fractional weights
  need an additional agreed scaling convention and conversion logic.
- Third-party arithmetic library: unnecessary because Python includes decimal
  arithmetic and explicit rounding modes.

## Consequences

Positive:

- Decimal inputs and explicit rounding match the agreed examples.
- The calculation can be tested without running a server or database.
- A local decimal context avoids changing the caller's precision settings.
- Validation, incomplete data, and valid results are distinct outcomes.

Trade-offs and limits:

- Future HTTP/database adapters must deliberately preserve decimal values and
  translate `None`/`ValueError` into appropriate responses.
- The core accepts explicit `Decimal` values, not raw JSON strings or floats;
  input parsing belongs at that future boundary.
- Grade precision is checked as supplied: `4.750` has three decimal places and
  is rejected, while `4.75` is accepted.
- This module does not yet associate results with courses/students, save data,
  or enforce user permissions. Those belong to subsequent changes.

Local verification reported by the project owner: Ruff passed, six Python files
already formatted, and 40 tests passed with 100% line coverage of the current
`app` package. This includes the two existing health tests and 38 grading cases;
it does not imply that all final-project features are implemented or tested.

Reference: [Python Decimal documentation](https://docs.python.org/3.12/library/decimal.html).
