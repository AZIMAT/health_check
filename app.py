from flask import Flask, jsonify
import http.client as httplib
import subprocess
import json

app = Flask(__name__)

health_status = True


@app.route("/health")
def health():
    conn = httplib.HTTPSConnection("radiojavan.com", timeout=5)
    bashCommand = "yes q | docker exec -i any-pass occtl -j show events >> userx.json | head -n-3 userx.json > user.json"
    subprocess.run(bashCommand, shell=True)
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
