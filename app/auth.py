"""Password login, signed sessions, and CSRF protection."""

from functools import wraps
from secrets import compare_digest, token_urlsafe

from flask import (
    Blueprint,
    current_app,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")
OPERATIONAL_ENDPOINTS = {"main.health", "main.ready", "main.metrics"}


def csrf_token():
    """Generate a token bound to this browser's signed session."""
    if "csrf_token" not in session:
        session["csrf_token"] = token_urlsafe(32)
    return session["csrf_token"]


def register_auth(app):
    app.extensions["dummy_password_hash"] = generate_password_hash(token_urlsafe(32))
    app.jinja_env.globals["csrf_token"] = csrf_token
    app.register_blueprint(bp)


@bp.before_app_request
def load_user_and_check_csrf():
    g.user = None
    if request.endpoint in OPERATIONAL_ENDPOINTS:
        return None
    if request.blueprint == "auth" and not current_app.config["SECRET_KEY"]:
        return jsonify(error="Login is not configured"), 503

    user_id = session.get("user_id")
    if user_id is not None:
        try:
            g.user = current_app.extensions["repository"].get_user(user_id)
        except LookupError:
            session.clear()

    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        expected = session.get("csrf_token")
        supplied = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token")
        if (
            not isinstance(expected, str)
            or not isinstance(supplied, str)
            or not compare_digest(expected.encode("utf-8"), supplied.encode("utf-8"))
        ):
            return jsonify(error="Invalid CSRF token"), 400
    return None


def login_required(view):
    """Require a signed-in user before calling a protected route."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return jsonify(error="Authentication required"), 401
        return view(*args, **kwargs)

    return wrapped


def public_user(user):
    """Select the identity fields exposed by the API."""
    return {"id": user.id, "username": user.username, "role": user.role.value}


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=None)

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not username or len(username) > 200 or not password or len(password) > 1024:
        return render_template("login.html", error="Invalid username or password"), 401

    repository = current_app.extensions["repository"]
    user = repository.find_user_by_username(username)
    password_hash = (
        user.password_hash if user is not None else current_app.extensions["dummy_password_hash"]
    )
    valid = check_password_hash(password_hash, password)
    if user is None or not valid:
        return render_template("login.html", error="Invalid username or password"), 401

    session.clear()
    session["user_id"] = user.id
    session.permanent = True
    csrf_token()
    return redirect(url_for("auth.me"))


@bp.get("/me")
@login_required
def me():
    return jsonify(public_user(g.user))


@bp.post("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.after_app_request
def prevent_auth_caching(response):
    if request.blueprint == "auth":
        response.headers["Cache-Control"] = "no-store"
    return response
