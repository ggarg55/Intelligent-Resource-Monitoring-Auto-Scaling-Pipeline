from flask import Flask, request
import os
import time
import subprocess

app = Flask(__name__)

LOCK_FILE = "scaling.lock"
COOLDOWN_SECONDS = 120  # 2 minutes cooldown


def is_scaling_locked():
    if not os.path.exists(LOCK_FILE):
        return False

    last_time = os.path.getmtime(LOCK_FILE)
    return (time.time() - last_time) < COOLDOWN_SECONDS


def lock_scaling():
    with open(LOCK_FILE, "w") as f:
        f.write(str(time.time()))


@app.route('/scale', methods=['POST'])
def scale():
    print(" ALERT RECEIVED")

    payload = request.get_json(silent=True) or {}
    if payload.get("status") == "resolved":
        print("Alert resolved. Ignoring scaling up.")
        return "OK", 200

    if is_scaling_locked():
        print("Cooldown active. Skipping scaling.")
        return "Cooldown active", 200

    instance_name = f"auto-instance-{int(time.time())}"
    print(f" Creating instance: {instance_name}")

    cmd = [
        "gcloud", "compute", "instances", "create", instance_name,
        "--zone=us-central1-a",
        "--machine-type=e2-micro",
        "--image-family=debian-11",
        "--image-project=debian-cloud"
    ]

    try:
        subprocess.run(cmd, check=True)
        lock_scaling()
        print(" Instance created successfully")
    except subprocess.CalledProcessError as e:
        print("Error creating instance:", e)

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
