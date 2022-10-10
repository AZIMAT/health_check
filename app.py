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
VPNCERT = os.getenv('VPNCERT')
VPNUSER = os.getenv('VPNUSER')
VPNPASS = os.getenv('VPNPASS')

print(VPNCERT)

@app.route("/refresh")
def refresh():
    conn = httplib.HTTPSConnection("radiojavan.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        resp = jsonify(connect=1)
        resp.status_code = 200
    except Exception:
        bashCommand = 'sudo kill -2 $(cat "$HOME/.openconnect.pid") && rm -f "$HOME/.openconnect.pid"'
        subprocess.run(bashCommand, shell=True)
        time.sleep(1)
        bashCommand = f"(sleep 15 ; echo '{VPNPASS}') | sudo openconnect {VPNSERVER}:4321 --background --servercert {VPNCERT} --pid-file=$HOME/.openconnect.pid --no-dtls --user={VPNUSER} --passwd-on-stdin"
        subprocess.run(bashCommand, shell=True)
        resp = jsonify(connect=2)
        resp.status_code = 200
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
