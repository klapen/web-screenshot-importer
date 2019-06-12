from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class ScreenshotImporter(Resource):
    def get(self):
        return { 'status': 'ok', 'version': 'v0.1' }

api.add_resource(ScreenshotImporter,
                 '/')

if __name__ == '__main__':
    app.run(debug=True)
