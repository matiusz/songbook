from src.flask.flask_app import app, port

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True, port=port)
    