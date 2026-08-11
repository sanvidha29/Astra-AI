from routes.auth import auth_bp
from routes.home import home_bp
from routes.settings import settings_bp
from routes.voice import voice_bp
from routes.chat import chat_bp

from flask import (
    Flask,
    redirect,
    url_for,
    session
)

from database import (
    create_database,
    owner_exists
)

from commands.command_handler import execute_command

# Create Flask App
app = Flask(__name__)

# Create database
create_database()

# Secret Key
app.secret_key = "astra_ai_secret_key"

# Register Blueprints
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
    app.run(debug=True)