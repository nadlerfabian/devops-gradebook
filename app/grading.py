"""Calculate Swiss-scale course results without web or database dependencies."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, localcontext


@dataclass(frozen=True)
class AssessmentGrade:
    """One student's grade and its assessment's percentage weight."""

    grade: Decimal | None
    weight: Decimal


def _require_finite_decimal(value: Decimal, field: str) -> None:
    """Reject approximate numbers and special values before arithmetic."""
    if not isinstance(value, Decimal) or not value.is_finite():
        raise ValueError(f"{field} must be a finite Decimal")


def validate_weight(weight: Decimal) -> None:
    """Require a positive decimal percentage; totals are checked separately."""
    _require_finite_decimal(weight, "Weight")
    if weight <= 0:
        raise ValueError("Weight must be greater than zero")


def validate_grade(grade: Decimal) -> None:
    """Require a Swiss-scale grade with at most two decimal places."""
    _require_finite_decimal(grade, "Grade")
    if not Decimal("1") <= grade <= Decimal("6"):
        raise ValueError("Grade must be between 1 and 6")
    if grade.as_tuple().exponent < -2:
        raise ValueError("Grade must have at most two decimal places")


def calculate_weighted_average(assessments: list[AssessmentGrade]) -> Decimal | None:
    """Return a two-decimal result, or None when the course is incomplete.

    Inputs use Decimal values constructed from strings, such as Decimal("4.75").
    None represents a missing grade. Invalid grades/weights raise ValueError;
    missing grades, no assessments, or weights not totaling 100 return None.
    """
    for assessment in assessments:
        validate_weight(assessment.weight)
        if assessment.grade is not None:
            validate_grade(assessment.grade)

    if not assessments:
        return None

    # Positive weights above 100 cannot form a complete 100-percent course.
    if any(assessment.weight > 100 for assessment in assessments):
        return None

    with localcontext() as context:
        # Preserve supplied weight digits, multiplication, and summation before
        # final rounding, independently of the caller's Decimal precision.
        weight_digits = max(
            len(assessment.weight.as_tuple().digits) + abs(assessment.weight.as_tuple().exponent)
            for assessment in assessments
        )
        context.prec = max(28, weight_digits + len(str(len(assessments))) + 6)

        total_weight = sum((assessment.weight for assessment in assessments), Decimal("0"))
        if total_weight != Decimal("100"):
            return None

        weighted_total = Decimal("0")
        for assessment in assessments:
            if assessment.grade is None:
                return None
            weighted_total += assessment.grade * assessment.weight

        average = weighted_total / Decimal("100")
        return average.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
