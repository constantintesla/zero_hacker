from flask import Flask, render_template
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "matrix-green")
app.permanent_session_lifetime = timedelta(hours=6)

TARGET_HOST = "http://138.124.81.201/"


@app.route("/", methods=["GET"]) 
def index():
    return render_template("index.html", target_host=TARGET_HOST)


@app.route("/run", methods=["GET"]) 
def run_simple():
    return render_template("run.html", target_host=TARGET_HOST)


@app.route("/end", methods=["GET"]) 
def end():
    return render_template("end.html", target_host=TARGET_HOST)


@app.after_request
def security_headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Referrer-Policy", "no-referrer")
    resp.headers.setdefault("Cache-Control", "no-store")
    return resp


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
