# khowri taoj unwgs dungj Flask

from flask import Flask

def create_app():
    app = Flask(__name__)
    
    #Dang ky cac route tu routes.py
    from .routes import main
    app.register_blueprint(main)

    return app