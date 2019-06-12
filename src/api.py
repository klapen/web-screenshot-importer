from flask import Flask
from flask_restful import Resource, Api

from config import db, app
from models import (
    Log,
    LogSchema,
)

api = Api(app)

class HistoryLog(Resource):
    def get(self):
        history = Log.query.order_by(Log.timestamp).all()
        history_schema = LogSchema(many=True)
        return history_schema.dump(history).data

class ScreenshotImporter(Resource):
    def get(self):
        return { 'status': 'ok', 'version': 'v0.1' }

api.add_resource(ScreenshotImporter, '/')
api.add_resource(HistoryLog, '/log')

if __name__ == '__main__':
    app.run(debug=True)
