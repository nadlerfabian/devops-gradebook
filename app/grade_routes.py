"""Record grades and expose authorized course results."""

import re
from decimal import Decimal

from flask import Blueprint, current_app, g, jsonify, request

from app.auth import login_required

bp = Blueprint("grades", __name__, url_prefix="/api")


def grade_json(grade):
    return {
        "assessment_id": grade.assessment_id,
        "student_id": grade.student_id,
        "value": str(grade.value),
    }


@bp.put("/assessments/<int:assessment_id>/grades/<int:student_id>")
@login_required
def set_grade(assessment_id, student_id):
    payload = request.get_json(silent=True)
    value = payload.get("value") if isinstance(payload, dict) else None
    if (
        not isinstance(value, str)
        or len(value) > 32
        or not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value)
    ):
        return jsonify(error="Provide a decimal grade as text, such as '5.25'"), 400

    repository = current_app.extensions["repository"]
    try:
        grade = repository.set_grade(g.user.id, assessment_id, student_id, Decimal(value))
    except PermissionError:
        return jsonify(error="Only the course owner can record grades"), 403
    except LookupError:
        return jsonify(error="Assessment or student account not found"), 404
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(grade_json(grade))


@bp.get("/courses/<int:course_id>/results/<int:student_id>")
@login_required
def get_result(course_id, student_id):
    repository = current_app.extensions["repository"]
    try:
        grades, average = repository.get_result(g.user.id, course_id, student_id)
    except PermissionError:
        return jsonify(error="You do not have access to this result"), 403
    except LookupError:
        return jsonify(error="Course or student account not found"), 404
    except ValueError as error:
        return jsonify(error=str(error)), 400

    return jsonify(
        course_id=course_id,
        student_id=student_id,
        grades=[grade_json(grade) for grade in grades],
        average=str(average) if average is not None else None,
    )
