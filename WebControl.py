from flask import Flask, render_template, Response

from services.SocketClientService import SocketClientService
from services.CameraService import (
    COMMAND_DOWN,
    COMMAND_LEFT,
    COMMAND_RIGHT,
    COMMAND_STOP,
    PORT,
    COMMAND_UP,
    COMMAND_SHOT,
    CameraService,
)


CAMERA_SERVICE = CameraService()

app = Flask("__name__")


def video_stream():
    while True:
        frame = CAMERA_SERVICE.runAction(COMMAND_SHOT)
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
    CAMERA_SERVICE.runAction(COMMAND_UP)
    return ""


@app.route("/cam_down")
def cam_down():
    CAMERA_SERVICE.runAction(COMMAND_DOWN)
    return ""


@app.route("/cam_left")
def cam_left():
    CAMERA_SERVICE.runAction(COMMAND_LEFT)
    return ""


@app.route("/cam_right")
def cam_right():
    CAMERA_SERVICE.runAction(COMMAND_RIGHT)
    return ""


@app.route("/cam_stop")
def cam_stop():
    CAMERA_SERVICE.runAction(COMMAND_STOP)
    return ""


app.run(host="0.0.0.0", port="5000", debug=False)
