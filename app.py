from routes.auth import auth_bp
from routes.home import home_bp
from routes.settings import settings_bp
from routes.voice import voice_bp
from routes.chat import chat_bp
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



app = Flask(__name__)

app.secret_key = "astra_ai_secret_key"
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(voice_bp)
app.register_blueprint(chat_bp)





@app.route("/start")
def start():

    if not owner_exists():
        return redirect(url_for("auth.setup"))


    if "username" not in session:
        return redirect(url_for("auth.login"))

    return redirect(url_for("home.home"))


if __name__ == "__main__":
    create_database()
    # from ai_engine import show_models
    # show_models()
    app.run(debug=True)


