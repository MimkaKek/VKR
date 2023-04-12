from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
     
def create_app(config_class = Config):
    app = Flask(__name__, template_folder="/var/vkr/projects")
    app.config.from_object(config_class)

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    db.init_app(app)

    from app.models import ProjectModel, UserModel

    with app.app_context():
        db.create_all()
        
        from app.managers import RepositoryManager, UserManager
        repManager = RepositoryManager()
        repManager.Init()

        usrManager = UserManager()
        usrManager.CreateAdmin()

    from app.routes import projectBlueprint
    app.register_blueprint(projectBlueprint)

    from app.routes import userBlueprint
    app.register_blueprint(userBlueprint)
    
    return app