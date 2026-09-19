from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
import os

app = FastAPI()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SCRIPT = os.path.join(BASE_DIR, "run_app.sh")


@app.get("/")
def home():

    return FileResponse(
        os.path.join(BASE_DIR, "web", "index.html")
    )


@app.get("/status")
def status():

    subprocess.run(
        ["git", "fetch", "origin"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    local = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=BASE_DIR,
        text=True
    ).strip()

    remote = subprocess.check_output(
        ["git", "rev-parse", "origin/main"],
        cwd=BASE_DIR,
        text=True
    ).strip()

    update_available = local != remote

    running = subprocess.run(
        ["pgrep", "-f", "run_app.sh"],
        capture_output=True
    ).returncode == 0

    return {
        "running": running,
        "local_commit": local[:7],
        "remote_commit": remote[:7],
        "update_available": update_available
    }


@app.post("/start")
def start():

    subprocess.Popen(
        [SCRIPT],
        cwd=BASE_DIR,
        start_new_session=True
    )

    return {
        "message": "Script started"
    }
