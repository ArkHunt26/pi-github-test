from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
import os

app = FastAPI()

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application script
SCRIPT = os.path.join(BASE_DIR, "run_app.sh")


@app.get("/")
def home():
    return FileResponse(
        os.path.join(BASE_DIR, "web", "index.html")
    )


@app.get("/status")
def status():

    # Check GitHub for latest commit
    subprocess.run(
        ["git", "fetch", "origin"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    # Current commit on Pi
    local = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=BASE_DIR,
        text=True
    ).strip()

    # Latest commit on GitHub
    remote = subprocess.check_output(
        ["git", "rev-parse", "origin/main"],
        cwd=BASE_DIR,
        text=True
    ).strip()

    update_available = local != remote

    # Check whether our application is running
    running = subprocess.run(
        ["pgrep", "-f", "hello.py"],
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

    # Check if application is already running
    running = subprocess.run(
        ["pgrep", "-f", "hello.py"],
        capture_output=True
    ).returncode == 0

    if running:
        return {
            "success": False,
            "message": "Application is already running."
        }

    subprocess.Popen(
        [SCRIPT],
        cwd=BASE_DIR,
        start_new_session=True
    )

    return {
        "success": True,
        "message": "Application started."
    }


@app.post("/update")
def update():

    # Pull latest code from GitHub
    result = subprocess.run(
        ["git", "pull", "--ff-only", "origin", "main"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return {
            "success": True,
            "message": "Update successful.",
            "output": result.stdout
        }

    return {
        "success": False,
        "message": "Update failed.",
        "output": result.stdout,
        "error": result.stderr
    }
