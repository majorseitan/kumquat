mv config.py.sample config.py

from app import db
db.create_all()
