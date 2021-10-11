from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# CONSTRUCTING THE CORE APPLICATION TO MAKE IT COMPATIBLE WITH SQLALCHEMY

def init_app():
    
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

# IMPORTS THE ROUTES FOR THE APP SO THE DATABASE WILL KNOW WHERE ROUTING IS COMING FROM/TO AND CREATES A READBALE TABLE BASED UPON THE MODEL WE CREATE IN THE APP
    
    with app.app_context():
        from . import routes  
        db.create_all()  

        return app
