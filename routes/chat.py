from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify

from database import save_chat, get_chat_history
from ai_engine import generate_chat_reply

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["GET", "POST"])
def chat():

    if "username" not in session:
        return redirect(url_for("auth.login"))

    username = session["username"]

    if request.method == "POST":

        user_message = request.form["message"]

        save_chat(username, "user", user_message)

        bot_reply = generate_chat_reply(user_message)

        save_chat(username, "astra", bot_reply)

    chats = get_chat_history(username)

    return render_template(
        "chat.html",
        username=username,
        chats=chats,
        page="chat"
    )


@chat_bp.route("/chat-api", methods=["POST"])
def chat_api():

    if "username" not in session:
        return jsonify({"reply": "Please login first."}), 401

    username = session["username"]

    data = request.get_json()

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Empty message."}), 400

    save_chat(username, "user", user_message)

    bot_reply = generate_chat_reply(user_message)

    save_chat(username, "astra", bot_reply)

    return jsonify({
        "reply": bot_reply
    })