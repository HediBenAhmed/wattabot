from flask import Flask, render_template, Response
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


def video_stream():
    while True:
        frame = CAMERA_SERVICE.runAction(C_SHOT)
        yield (b" --frame\r\n" b"Content-type: imgae/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/camera")
def camera():
    return render_template("camera.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/cam_up")
def cam_up():
    CAMERA_SERVICE.runAction(C_UP)
    return ""


@app.route("/cam_down")
def cam_down():
    CAMERA_SERVICE.runAction(C_DOWN)
    return ""


@app.route("/cam_left")
def cam_left():
    CAMERA_SERVICE.runAction(C_LEFT)
    return ""


@app.route("/cam_right")
def cam_right():
    CAMERA_SERVICE.runAction(C_RIGHT)
    return ""


@app.route("/cam_stop")
def cam_stop():
    CAMERA_SERVICE.runAction(C_STOP)
    return ""


@app.route("/motor_forward")
def motor_forward():
    MOTORS_SERVICE.runAction(M_FORWARD)
    return ""


@app.route("/motor_backwoard")
def motor_backwoard():
    MOTORS_SERVICE.runAction(M_BACKWARD)
    return ""


@app.route("/motor_left")
def motor_left():
    MOTORS_SERVICE.runAction(M_LEFT)
    return ""


@app.route("/motor_right")
def motor_right():
    MOTORS_SERVICE.runAction(M_RIGHT)
    return ""


@app.route("/motor_stop")
def motor_stop():
    MOTORS_SERVICE.runAction(M_STOP)
    return ""


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
