""" from app import db, app

from sqlalchemy.ext.automap import automap_base

with app.app_context():
    Base = automap_base()

    Base.prepare(db.engine, reflect=True)

    User = Base.classes.user
    Department = Base.classes.department """
