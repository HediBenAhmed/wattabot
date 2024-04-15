import time
from flask import Flask, request, Response, abort, render_template, url_for, redirect
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    UserMixin,
    current_user,
)
from collections import defaultdict
from services.CameraService import (
    COMMAND_DOWN as C_DOWN,
    COMMAND_LEFT as C_LEFT,
    COMMAND_RIGHT as C_RIGHT,
    COMMAND_STOP as C_STOP,
    COMMAND_UP as C_UP,
    COMMAND_SHOT as C_SHOT,
    CameraService,
)
from waitress import serve

from services.MotorsService import (
    COMMAND_BACKWARD as M_BACKWARD,
    COMMAND_LEFT as M_LEFT,
    COMMAND_RIGHT as M_RIGHT,
    COMMAND_STOP as M_STOP,
    COMMAND_FORWARD as M_FORWARD,
    MotorsService,
)


CAMERA_SERVICE = CameraService()
MOTORS_SERVICE = MotorsService()

app = Flask(
    "__name__",
    static_folder="/home/hedi/wattabot/static",
    template_folder="/home/hedi/wattabot/templates",
)

login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = "loginexample"


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


users = {1: User(1, "user", "password")}

nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.username]["password"] = i.password
    user_check[i.username]["id"] = i.id


@login_manager.user_loader
def load_user(id):
    return users.get(int(id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        if username in user_check and password == user_check[username]["password"]:
            id = user_check[username]["id"]
            login_user(users.get(id))

            return redirect(url_for("camera"))
        else:
            return abort(401)
    else:
        return render_template("login.html")


def video_stream():
    while True:
        # 20 images /sec
        time.sleep(1 / 20)

        frame = CAMERA_SERVICE.runAction(C_SHOT)
        print(len(frame))
        yield (b" --frame\r\n" b"Content-type: imgae/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/camera")
@login_required
def camera():
    return render_template("camera.html")


@app.route("/video_feed")
@login_required
def video_feed():
    return Response(
        video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/cam_up")
@login_required
def cam_up():
    CAMERA_SERVICE.runAction(C_UP)
    return ""


@app.route("/cam_down")
@login_required
def cam_down():
    CAMERA_SERVICE.runAction(C_DOWN)
    return ""


@app.route("/cam_left")
@login_required
def cam_left():
    CAMERA_SERVICE.runAction(C_LEFT)
    return ""


@app.route("/cam_right")
@login_required
def cam_right():
    CAMERA_SERVICE.runAction(C_RIGHT)
    return ""


@app.route("/cam_stop")
@login_required
def cam_stop():
    CAMERA_SERVICE.runAction(C_STOP)
    return ""


@app.route("/motor_forward")
@login_required
def motor_forward():
    MOTORS_SERVICE.runAction(M_FORWARD)
    return ""


@app.route("/motor_backwoard")
@login_required
def motor_backwoard():
    MOTORS_SERVICE.runAction(M_BACKWARD)
    return ""


@app.route("/motor_left")
@login_required
def motor_left():
    MOTORS_SERVICE.runAction(M_LEFT)
    return ""


@app.route("/motor_right")
@login_required
def motor_right():
    MOTORS_SERVICE.runAction(M_RIGHT)
    return ""


@app.route("/motor_stop")
@login_required
def motor_stop():
    MOTORS_SERVICE.runAction(M_STOP)
    return ""


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
