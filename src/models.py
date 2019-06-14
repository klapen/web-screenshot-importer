from datetime import datetime
from config import db, ma

class Log(db.Model):
    __tablename__ = 'log'
    req_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    status = db.Column(db.String)
    image_url = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LogSchema(ma.ModelSchema):
    class Meta:
        model = Log
        sqla_session = db.session
