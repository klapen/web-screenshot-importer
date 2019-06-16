from flask_restful import Resource

from models import (
    Log,
    LogSchema
)

class LogHistory(Resource):
    def get(self):
        try:
            history = Log.query.order_by(Log.timestamp.desc()).limit(50).all()
            return LogSchema(many=True).dump(history).data
        except Exception as err:
            print('LogHistory - Error retrieving data from database: %s' % err)
            return {'error': 'Error getting history log'}, 500
