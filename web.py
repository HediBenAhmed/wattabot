import json
from flask import (
    Flask,
    request,
    Response,
    abort,
    render_template,
    url_for,
    redirect,
)
from flask_login import LoginManager, login_user, login_required
from waitress import serve
from services.Configurations import secretConfig
from services.PrivateApiService import PRIVATE_API_SERVICE
from services.WebService import WEB_SERVICE


app = Flask(
    "__name__",
    static_folder="/home/hedi/wattabot/static",
    template_folder="/home/hedi/wattabot/templates",
)

login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = secretConfig("WEB_SECRET_KEY")


@login_manager.user_loader
def load_user(id):
    return PRIVATE_API_SERVICE.getUser(id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        user = PRIVATE_API_SERVICE.login(username, password)

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
        WEB_SERVICE.videoStream(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/identify_faces")
@login_required
def identify_faces():
    face = WEB_SERVICE.identifyFace()

    result = None
    if face is not None:
        result = {"name": face.name, "confidence": face.confidence}

    return json.dumps(result)


@app.route("/cam_centralize_faces")
@login_required
def cam_centralize_faces():
    WEB_SERVICE.switchCamCentralizeFaces()
    return ""


@app.route("/cam_up")
@login_required
def cam_up():
    WEB_SERVICE.camUp()
    return ""


@app.route("/cam_down")
@login_required
def cam_down():
    WEB_SERVICE.camDown()
    return ""


@app.route("/cam_left")
@login_required
def cam_left():
    WEB_SERVICE.camLeft()
    return ""


@app.route("/cam_right")
@login_required
def cam_right():
    WEB_SERVICE.camRight()
    return ""


@app.route("/cam_save")
@login_required
def cam_save():
    return ""


@app.route("/motor_forward")
@login_required
def motor_forward():
    WEB_SERVICE.motorForward()
    return ""


@app.route("/motor_backwoard")
@login_required
def motor_backwoard():
    WEB_SERVICE.motorBackwoard()
    return ""


@app.route("/motor_left")
@login_required
def motor_left():
    WEB_SERVICE.motorLeft()
    return ""


@app.route("/motor_right")
@login_required
def motor_right():
    WEB_SERVICE.motorRight()
    return ""


@app.route("/motor_stop")
@login_required
def motor_stop():
    WEB_SERVICE.motorStop()
    return ""


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=80)
