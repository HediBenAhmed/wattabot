import json
from flask import (
    Flask,
    request,
    Response,
    abort,
    render_template,
    stream_with_context,
    url_for,
    redirect,
)
from flask_login import LoginManager, login_user, login_required
import flask_login
from flask_socketio import SocketIO
from services.Configurations import secretConfig
from services.IdentificationService import IdentificationService
from services.PrivateApiService import PrivateApiService
from services.WebService import WebService


app = Flask(
    "__name__",
    static_folder="/home/hedi/wattabot/static",
    template_folder="/home/hedi/wattabot/templates",
)

socket = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = secretConfig("WEB_SECRET_KEY")


@login_manager.user_loader
def load_user(id):
    return PrivateApiService.getInsance().getUser(id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("face", None) is not None:
            user = IdentificationService.getInsance().identification()
        else:

            username = request.form.get("username", None)
            password = request.form.get("password", None)

            user = PrivateApiService.getInsance().login(username, password)

        if user is not None:
            login_user(user)

            return redirect(url_for("camera"))
        else:
            return abort(401)
    else:
        return render_template("login.html")


@app.route("/camera")
@login_required
def camera():
    return render_template("camera.html")


@app.route("/video_feed")
@login_required
def video_feed():

    return Response(
        WebService.getInsance().videoStream(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/identify_faces")
@login_required
def identify_faces():
    face = WebService.getInsance().identifyFace()

    result = None
    if face is not None:
        result = {"name": face.name, "confidence": face.confidence}

    return json.dumps(result)


@app.route("/cam_centralize_faces")
@login_required
def cam_centralize_faces():
    WebService.getInsance().switchCamCentralizeFaces()
    return ""


@socket.on("connect")
def connect():
    print("init", flask_login.current_user)
    WebService.getInsance().init(flask_login.current_user)


@socket.on("disconnect")
def disconnect():
    print("disconnect")
    WebService.getInsance().stop()


@app.route("/command/<feature>/<action>", methods=["GET", "POST"])
def catch_all(feature, action):
    print("You want feature: %s" % feature, action)
    WebService.getInsance().executeCommand(feature, action)
    return ""


if __name__ == "__main__":
    socket.run(app, debug=True, host="0.0.0.0", port=8181)
