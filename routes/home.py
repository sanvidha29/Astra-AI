from flask import Blueprint, render_template, session, redirect, url_for

home_bp = Blueprint("home", __name__)

# -------------------------------
# Landing Page
# -------------------------------

@home_bp.route("/")
def index():

    logged_in = "username" in session

    return render_template(
        "start.html",
        logged_in=logged_in
    )


# -------------------------------
# Home Page
# -------------------------------

@home_bp.route("/home")
def home():

    if "username" not in session:
        return redirect(url_for("auth.login"))

    return render_template(
        "home.html",
        username=session["username"],
        page="home"
    )