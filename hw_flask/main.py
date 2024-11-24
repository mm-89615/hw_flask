from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!!"

@app.route("/status")
def status():
    return jsonify({"status": "OK", "message": "Flask is running with Gunicorn!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0')