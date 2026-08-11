from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from database import (
    owner_exists,
    create_owner,
    get_user
)

# Blueprint
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = get_user(username)

    if user is None:

        flash("User not found.", "warning")
        return redirect(url_for("auth.login"))

    if user["password"] != password:

        flash("Incorrect password.", "warning")
        return redirect(url_for("auth.login"))

    session["username"] = username

    flash("Login Successful!", "success")

    return redirect(url_for("home.index"))


@auth_bp.route("/setup", methods=["GET", "POST"])
def setup():

    if request.method == "GET":
        return render_template("setup.html")

    full_name = request.form["full_name"]
    username = request.form["username"]
    email = request.form["email"]
    age = request.form["age"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for("auth.setup"))

    create_owner(
        full_name,
        username,
        email,
        age,
        password
    )

    flash("Owner account created successfully!", "success")

    return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for("auth.login"))


@auth_bp.route("/create-owner")
def create_owner_page():

    if owner_exists():

        flash("Owner account already exists.", "warning")
        return redirect(url_for("home.index"))

    return redirect(url_for("auth.setup"))


@auth_bp.route("/go-login")
def go_login():

    if not owner_exists():

        flash("Please create an owner account first.", "warning")
        return redirect(url_for("home.index"))

    if "username" in session:

        flash("You are already logged in.", "info")
        return redirect(url_for("home.index"))

    return redirect(url_for("auth.login"))