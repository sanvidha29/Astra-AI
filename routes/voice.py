from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    jsonify
)

from commands.command_handler import execute_command
from ai_engine import generate_voice_reply

voice_bp = Blueprint("voice", __name__)

@voice_bp.route("/voice")
def voice():

    if "username" not in session:
        return redirect(url_for("auth.login"))

    return render_template(
        "voice.html",
        username=session["username"],
        page="voice"
    )

@voice_bp.route("/voice-chat", methods=["POST"])
def voice_chat():

    data = request.get_json()

    user_message = data["message"]

    # Check if it's a desktop command
    command_reply = execute_command(user_message)

    if command_reply:

        return jsonify({
            "reply": command_reply
        })

    # Otherwise ask Gemini
    reply = generate_voice_reply(user_message)

    return jsonify({
        "reply": reply
    })


