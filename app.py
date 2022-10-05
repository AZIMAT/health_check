from flask import Flask, jsonify
import http.client as httplib
import os
from dotenv import load_dotenv
load_dotenv()
import time
import subprocess
import json

app = Flask(__name__)

VPNSERVER = os.getenv('VPNSERVER')
VPNUSER = os.getenv('VPNUSER')
VPNPASS = os.getenv('VPNPASS')

@app.route("/refresh")
def refresh():
    try:
        bashCommand = 'sudo kill -2 $(cat "$HOME/.openconnect.pid") && rm -f "$HOME/.openconnect.pid"'
        subprocess.run(bashCommand, shell=True)
        time.sleep(1)

        bashCommand = f"(echo 'yes'; sleep 1 ;echo '{VPNPASS}') | sudo openconnect {VPNSERVER} --background --pid-file=$HOME/.openconnect.pid --no-dtls --user={VPNUSER}"
        subprocess.run(bashCommand, shell=True)

        resp = jsonify(refresh=1)
        resp.status_code = 200
    except Exception:
        resp = jsonify(refresh=2)
        resp.status_code = 500

    return resp

@app.route("/health")
def health():
    conn = httplib.HTTPSConnection("radiojavan.com", timeout=5)
    bashCommand = "yes q | docker exec -i any-pass occtl -j show events > userx.json; head -n-3 userx.json > user.json"
    subprocess.run(bashCommand, shell=True)
    time.sleep(1)

    # read file
    with open("user.json", "r") as myfile:
        data = myfile.read()

    # parse file
    obj = json.loads(data)
    print(len(obj))
    try:

        conn.request("HEAD", "/")
        resp = jsonify(health=1, online=len(obj))
        resp.status_code = 200
    except Exception:
        resp = jsonify(health=0, online=len(obj))
        resp.status_code = 500

    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
