from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from database import (
    get_user,
    update_user,
    change_password,
    get_ai_settings,
    update_ai_settings,
    get_voice_settings,
    update_voice_settings
)

# Blueprint
settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():

    if "username" not in session:
        return redirect(url_for("auth.login"))

    username = session["username"]

    if request.method == "POST":

        form_type = request.form["form_type"]

        # -------------------------
        # Profile Form
        # -------------------------
        if form_type == "profile":

            full_name = request.form["full_name"]
            email = request.form["email"]
            age = request.form["age"]

            update_user(
                full_name,
                username,
                email,
                age
            )

            flash(
                "Profile updated successfully!",
                "success"
            )

            return redirect(url_for("settings.settings"))

        # -------------------------
        # Security Form
        # -------------------------
        elif form_type == "security":

            current_password = request.form["current_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]

            user = get_user(username)

            if current_password != user["password"]:

                flash(
                    "Current password is incorrect.",
                    "danger"
                )

                return redirect(url_for("settings.settings"))

            if new_password != confirm_password:

                flash(
                    "New passwords do not match.",
                    "danger"
                )

                return redirect(url_for("settings.settings"))

            change_password(
                username,
                new_password
            )

            flash(
                "Password changed successfully!",
                "success"
            )

            return redirect(url_for("settings.settings"))

        # -------------------------
        # AI Settings
        # -------------------------
        elif form_type == "ai":

            ai_style = request.form["ai_style"]
            response_length = request.form["response_length"]
            memory_enabled = 1 if "memory_enabled" in request.form else 0

            update_ai_settings(
                username,
                ai_style,
                response_length,
                memory_enabled
            )

            flash(
                "AI Settings updated successfully!",
                "success"
            )

            return redirect(url_for("settings.settings"))

        # -------------------------
        # Voice Settings
        # -------------------------
        elif form_type == "voice":

            voice_enabled = 1 if "voice_enabled" in request.form else 0
            voice_speed = request.form["voice_speed"]
            voice_volume = int(request.form["voice_volume"])

            update_voice_settings(
                username,
                voice_enabled,
                voice_speed,
                voice_volume
            )

            flash(
                "Voice Settings updated successfully!",
                "success"
            )

            return redirect(url_for("settings.settings"))

    # -------------------------
    # Load Data
    # -------------------------

    user = get_user(username)

    ai_settings = get_ai_settings(username)

    voice_settings = get_voice_settings(username)

    return render_template(
        "settings.html",
        user=user,
        ai_settings=ai_settings,
        voice_settings=voice_settings,
        page="settings"
    )