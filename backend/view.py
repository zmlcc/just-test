from main import app


@app.route("/info")
def hello_world():
    return 'Hello World!'