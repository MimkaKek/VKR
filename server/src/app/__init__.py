from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
     
def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        
    from app.managers import RepositoryManager
    manager = RepositoryManager()
    manager.Init()
    
    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.main import userBlueprint
    app.register_blueprint(userBlueprint)
    
    return app