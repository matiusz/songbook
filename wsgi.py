from src.flask.flask import app, port

if __name__=="__main__":
    app.run(debug=True, port=port)