from flask import Flask

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    app.run("0.0.0.0", 8081, debug=True)