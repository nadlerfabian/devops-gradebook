"""Check agreed grading rules, validation, and rounding boundaries."""

from decimal import Decimal, localcontext

import pytest

from app.grading import AssessmentGrade, calculate_weighted_average


@pytest.mark.parametrize(
    ("grades_and_weights", "expected"),
    [
        ([("5.0", "40"), ("4.0", "60")], "4.40"),
        ([("4.44", "50"), ("4.45", "50")], "4.45"),
        ([("4.44", "60"), ("4.45", "40")], "4.44"),
        ([("1", "100")], "1.00"),
        ([("6", "100")], "6.00"),
        ([("4.75", "100")], "4.75"),
        ([("5", "33.33"), ("4", "66.67")], "4.33"),
    ],
)
def test_complete_results(grades_and_weights, expected):
    assessments = [
        AssessmentGrade(Decimal(grade), Decimal(weight)) for grade, weight in grades_and_weights
    ]

    result = calculate_weighted_average(assessments)

    assert result is not None
    assert str(result) == expected


@pytest.mark.parametrize(
    "assessments",
    [
        [],
        [AssessmentGrade(None, Decimal("100"))],
        [AssessmentGrade(Decimal("5"), Decimal("40")), AssessmentGrade(None, Decimal("60"))],
        [AssessmentGrade(Decimal("5"), Decimal("90"))],
        [AssessmentGrade(Decimal("5"), Decimal("110"))],
        [
            AssessmentGrade(Decimal("5"), Decimal("60")),
            AssessmentGrade(Decimal("4"), Decimal("50")),
        ],
    ],
)
def test_incomplete_results_have_no_final_average(assessments):
    assert calculate_weighted_average(assessments) is None


@pytest.mark.parametrize("grade", ["0.99", "6.01", "4.755", "4.750"])
def test_invalid_grade_is_rejected(grade):
    assessments = [AssessmentGrade(Decimal(grade), Decimal("100"))]

    with pytest.raises(ValueError, match="Grade"):
        calculate_weighted_average(assessments)


@pytest.mark.parametrize("weight", ["0", "-1"])
def test_nonpositive_weight_is_rejected(weight):
    with pytest.raises(ValueError, match="Weight must be greater than zero"):
        calculate_weighted_average([AssessmentGrade(Decimal("5"), Decimal(weight))])


@pytest.mark.parametrize("invalid", ["NaN", "sNaN", "Infinity", "-Infinity"])
@pytest.mark.parametrize("field", ["grade", "weight"])
def test_nonfinite_values_are_rejected(invalid, field):
    grade = Decimal(invalid) if field == "grade" else Decimal("5")
    weight = Decimal(invalid) if field == "weight" else Decimal("100")

    with pytest.raises(ValueError, match="finite Decimal"):
        calculate_weighted_average([AssessmentGrade(grade, weight)])


@pytest.mark.parametrize("invalid", [4.75, "4.75", True, 5])
@pytest.mark.parametrize("field", ["grade", "weight"])
def test_core_requires_explicit_decimal_inputs(invalid, field):
    grade = invalid if field == "grade" else Decimal("5")
    weight = invalid if field == "weight" else Decimal("100")

    with pytest.raises(ValueError, match="finite Decimal"):
        calculate_weighted_average([AssessmentGrade(grade, weight)])


def test_invalid_grade_is_rejected_even_when_course_weights_are_incomplete():
    assessments = [
        AssessmentGrade(None, Decimal("40")),
        AssessmentGrade(Decimal("7"), Decimal("50")),
    ]

    with pytest.raises(ValueError, match="Grade must be between 1 and 6"):
        calculate_weighted_average(assessments)


def test_high_precision_weights_are_not_rounded_to_a_complete_course():
    assessments = [
        AssessmentGrade(Decimal("5"), Decimal("50")),
        AssessmentGrade(Decimal("4"), Decimal("49.99999999999999999999999999999")),
    ]

    assert calculate_weighted_average(assessments) is None


def test_result_does_not_depend_on_callers_decimal_precision():
    assessments = [
        AssessmentGrade(Decimal("4.44"), Decimal("50")),
        AssessmentGrade(Decimal("4.45"), Decimal("50")),
    ]

    with localcontext() as context:
        context.prec = 3
        assert str(calculate_weighted_average(assessments)) == "4.45"
        assert context.prec == 3
