from flask import Flask, jsonify
import http.client as httplib

app = Flask(__name__)

health_status = True


@app.route("/health")
def health():
    conn = httplib.HTTPSConnection("radiojavan.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        resp = jsonify(health=1)
        resp.status_code = 200
    except Exception:
        resp = jsonify(health=0)
        resp.status_code = 500

    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
