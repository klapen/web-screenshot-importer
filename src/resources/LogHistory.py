from flask_restful import Resource

from src.models import (
    Log,
    LogSchema
)

class LogHistory(Resource):
    def get(self):
        history = Log.query.order_by(Log.timestamp).all()
        history_schema = LogSchema(many=True)
        return history_schema.dump(history).data
