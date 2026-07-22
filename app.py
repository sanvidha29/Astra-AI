from ai_engine import (
    generate_chat_reply,
    generate_voice_reply
)
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)
from database import (
    create_database,
    owner_exists,
    create_owner,
    get_user,
    save_chat,
    get_chat_history
)
from flask import jsonify
from commands.command_handler import execute_command
from database import update_user


app = Flask(__name__)

app.secret_key = "astra_ai_secret_key"

@app.route("/voice-chat", methods=["POST"])
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

@app.route("/")
def index():

    logged_in = "username" in session

    return render_template(
        "start.html",
        logged_in=logged_in
    )


@app.route("/start")
def start():

    if not owner_exists():
        return redirect(url_for("setup"))


    if "username" not in session:
        return redirect(url_for("login"))

    return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = get_user(username)

    if user is None:

        flash("User not found.", "warning")
        return redirect(url_for("login"))

    if user["password"] != password:

        flash("Incorrect password.", "warning")
        return redirect(url_for("login"))

    session["username"] = username

    flash("Login Successful!", "success")

    return redirect(url_for("index"))

@app.route("/home")
def home():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "home.html",
        username=session["username"],
        page="home"
    )

@app.route("/setup", methods=["GET", "POST"])
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
        return "passwords do not match."
    
    create_owner(
        full_name,
        username,
        email,
        age,
        password
    )

    return redirect(url_for("login"))

@app.route("/create-owner")
def create_owner_page():

    if owner_exists():

        flash("Owner account already exists.", "warning")
        return redirect(url_for("index"))

    return redirect(url_for("setup"))

@app.route("/go-login")
def go_login():

    if not owner_exists():

        flash("Please create an owner account first.", "warning")
        return redirect(url_for("index"))

    if "username" in session:

        flash("You are already logged in.", "info")
        return redirect(url_for("index"))

    return redirect(url_for("login"))

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

@app.route("/chat", methods=["GET", "POST"])
def chat():

    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    if request.method == "POST":

        user_message = request.form["message"]

        # Save user's message
        save_chat(username, "user", user_message)

       
        bot_reply = generate_chat_reply(user_message)

        # Save bot's reply
        save_chat(username, "astra", bot_reply)

    chats = get_chat_history(username)

    return render_template(
        "chat.html",
        username=username,
        chats=chats,
        page="chat"
    )

@app.route("/notes")
def notes():
    return render_template("notes.html")


@app.route("/voice")
def voice():
    return render_template("voice.html")

@app.route("/settings", methods=["GET", "POST"])
def settings():

    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        age = request.form["age"]

        update_user(
            full_name,
            username,
            email,
            age
        )

        flash("Profile updated successfully!", "success")

        return redirect(url_for("settings"))

    user = get_user(username)

    return render_template(
        "settings.html",
        user=user,
        page="settings"
    )

if __name__ == "__main__":
    create_database()
    from ai_engine import show_models

    show_models()
    app.run(debug=True)


