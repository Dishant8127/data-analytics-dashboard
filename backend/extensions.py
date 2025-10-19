
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager 
from flask_caching import Cache        
from flask_migrate import Migrate       
from celery import Celery

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
jwt = JWTManager()  
cache = Cache()    
migrate = Migrate() 

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery
