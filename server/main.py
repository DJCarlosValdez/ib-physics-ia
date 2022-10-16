import os
import pathlib
import socket
import signal
import argparse
import time
from datetime import datetime
import string
import random
import eventlet
import socketio
from multiprocessing import Process
import obd

static_files = {
    '/static': 'app/dist',
    '/static/': 'app/dist/index.html',
    '/assets': 'app/dist/assets',
}

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio, static_files=static_files)
sock = None

refresh_rate = 1.0
obd_connection = None
file = None
session = None
recording = True

commands = [
    obd.commands.SPEED,
    obd.commands.THROTTLE_POS,
    obd.commands.FUEL_LEVEL,
    obd.commands.HYBRID_BATTERY_REMAINING,
    # bms
]


def randomCode(len=4):
    choices = string.ascii_uppercase + string.digits
    return (''.join(random.choice(choices) for i in range(len)))


def newLogFile():
    global file
    if file is not None:
        file.close()

    os.makedirs("logs", exist_ok=True)
    file = open(f"logs/obd_log-{session}.csv", "w")
    file.write("Time,Command,Value\n")


def OBDStatusTranslator(status):
    if status == obd.OBDStatus.NOT_CONNECTED:
        return "Not Connected"
    elif status == obd.OBDStatus.ELM_CONNECTED:
        return "ELM Connected"
    elif status == obd.OBDStatus.ELM_CONNECTED:
        return "OBD Connceted"
    elif status == obd.OBDStatus.ELM_CONNECTED:
        return "Car Connected"


def handler(signum, frame):
    if sock is not None:
        sock.close()

    if obd_connection is not None:
        obd_connection.close()

    if file is not None:
        file.close()

    msg = "\n\n*/*/*/* Stopping OBD Logger */*/*/*\n"
    print(msg, end="", flush=True)
    exit(1)


@sio.event
def connect(sid, environ):
    print(f"Socket connected: {sid}")
    sio.emit("session:res:new", {"session": session}, room=sid)


@sio.on("session:pause")
def pause_session(sid):
    global recording
    recording = False


@sio.on("session:resume")
def resume_session(sid):
    global recording
    recording = True


@sio.on("session:req:new")
def new_session(sid):
    global session
    session = randomCode(4)
    newLogFile()
    sio.emit("session:res:new", {"session": session}, room=sid)


def func1():
    print("\n--- OBD Logger Starting ---")
    print(f"\n*** Refresh Rate: {refresh_rate} seconds\n")

    while True:
        if recording and obd_connection is not None:
            timestamp = time.time()
            timestamp_formatted = datetime.fromtimestamp(
                timestamp).strftime("%H:%M:%S.%f")
            for cmd in commands:
                response = obd_connection.query(cmd)
                response_value = str(response.value)
                if file is not None:
                    file.write(
                        f"{timestamp_formatted},{cmd.name},{response_value}\n")
                sio.emit('data:update', {"datasets": [
                    {"label": cmd.name, "data": response.value}],
                    "time": timestamp})

        sio.sleep(refresh_rate)


def func2():
    global sock
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    print(f"To see the UI open up: http://{ip_addr}:5000/static/")
    sock = eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    session = randomCode(4)

    parser = argparse.ArgumentParser()
    parser.add_argument("--obd-port", type=pathlib.Path, required=True)
    parser.add_argument("--refresh_rate", type=float,
                        required=False, default=refresh_rate)
    parser.add_argument("--baudrate", type=int, required=False, default=38400)
    args = parser.parse_args()

    refresh_rate = args.refresh_rate

    obd_port = str(args.obd_port)
    baudrate = args.baudrate

    obd_connection = obd.OBD(obd_port, baudrate=baudrate)

    newLogFile()

    sio.start_background_task(func1)
    func2()
