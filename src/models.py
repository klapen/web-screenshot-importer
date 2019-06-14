from datetime import datetime
from config import db, ma

class Log(db.Model):
    __tablename__ = 'log'
    req_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    status_code = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LogSchema(ma.ModelSchema):
    class Meta:
        model = Log
        sqla_session = db.session
