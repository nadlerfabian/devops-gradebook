"""Internal account provisioning; there is no public registration endpoint."""

from werkzeug.security import generate_password_hash

from app.models import Role


def provision_account(repository, username: str, password: str, role: Role, *, if_missing=False):
    """Hash a password before passing it to storage."""
    if not isinstance(username, str) or not username.strip() or len(username) > 200:
        raise ValueError("Username must contain between 1 and 200 characters")
    if not isinstance(password, str) or not password or len(password) > 1024:
        raise ValueError("Password must contain between 1 and 1024 characters")
    return repository.create_user(
        username, role, generate_password_hash(password), if_missing=if_missing
    )


def provision_demo_accounts(app):
    """Create the two configured synthetic accounts if they do not exist yet."""
    lecturer_password = app.config["DEMO_LECTURER_PASSWORD"]
    student_password = app.config["DEMO_STUDENT_PASSWORD"]
    if lecturer_password is None and student_password is None:
        return
    if not lecturer_password or not student_password or not app.config["SECRET_KEY"]:
        raise ValueError("Demo accounts require SECRET_KEY and both demo passwords")
    repository = app.extensions["repository"]
    provision_account(repository, "lecturer", lecturer_password, Role.LECTURER, if_missing=True)
    provision_account(repository, "student", student_password, Role.STUDENT, if_missing=True)
