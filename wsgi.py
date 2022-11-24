from src.flask.flask import app, port

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False, port=port)
    