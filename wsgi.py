from src.flask.flask import app, port

if __name__=="__main__":
    app.run(host='127.0.0.1', debug=True, port=8808)
    