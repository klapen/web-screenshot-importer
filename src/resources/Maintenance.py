from flask_restful import Resource

class Maintenance(Resource):
    def get(self):
        return { 'status': 'ok', 'version': 'v0.1' }
