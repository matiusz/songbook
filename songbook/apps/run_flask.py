from ..src.flask.flask_app import app

def main(port):
    app.run(host='0.0.0.0', debug=True, port=port)

if __name__=="__main__":
    main(8808)
    