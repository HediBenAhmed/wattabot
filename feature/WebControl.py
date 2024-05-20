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
from feature.Feature import Feature
from services.Configurations import secretConfig
from services.JobService import startProcess, stopProcess
from services.PrivateApiService import PrivateApiService
from services.WebService import WebService


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
    return PrivateApiService.getInsance().getUser(id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
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


@app.route("/CAM_N")
@login_required
def cam_up():
    WebService.getInsance().camUp()
    return ""


@app.route("/CAM_S")
@login_required
def cam_down():
    WebService.getInsance().camDown()
    return ""


@app.route("/CAM_W")
@login_required
def cam_left():
    WebService.getInsance().camRight()
    return ""


@app.route("/CAM_E")
@login_required
def cam_right():
    WebService.getInsance().camLeft()
    return ""


@app.route("/CAM_NE")
@login_required
def cam_up_left():
    WebService.getInsance().camUpLeft()
    return ""


@app.route("/CAM_NW")
@login_required
def cam_up_right():
    WebService.getInsance().camUpRight()
    return ""


@app.route("/CAM_SW")
@login_required
def cam_down_right():
    WebService.getInsance().camDownRight()
    return ""


@app.route("/CAM_SE")
@login_required
def cam_down_left():
    WebService.getInsance().camDownLeft()
    return ""


@app.route("/CAM_SAVE")
@login_required
def cam_save():
    return ""


@app.route("/MOTOR_N")
@login_required
def motor_forward():
    WebService.getInsance().motorForward()
    return ""


@app.route("/MOTOR_S")
@login_required
def motor_backwoard():
    WebService.getInsance().motorBackwoard()
    return ""


@app.route("/MOTOR_W")
@login_required
def motor_left():
    WebService.getInsance().motorLeft()
    return ""


@app.route("/MOTOR_E")
@login_required
def motor_right():
    WebService.getInsance().motorRight()
    return ""


@app.route("/MOTOR_NE")
@login_required
def motor_forward_right():
    return ""


@app.route("/MOTOR_NW")
@login_required
def motor_forward_left():
    return ""


@app.route("/MOTOR_SW")
@login_required
def motor_backwoard_left():
    return ""


@app.route("/MOTOR_SE")
@login_required
def motor_backwoard_right():
    return ""


@app.route("/MOTOR_C")
@login_required
def motor_stop():
    WebService.getInsance().motorStop()
    return ""


def startServer():
    serve(app, host="0.0.0.0", port=8181, threads=100)


if __name__ == "__main__":
    startServer()


class WebControl(Feature):

    def start(self, sharedDict):
        process, _ = startProcess(startServer, "webControl", sharedDict)
        if process is not None:
            self.process = process

    def stop(self, sharedDict):
        stopProcess(self.process, "webControl", sharedDict)
