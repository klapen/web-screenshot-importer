from flask import Flask
from flask_restful import Resource, Api

from resources.LogHistory import LogHistory
from resources.Maintenance import Maintenance
from resources.ScreenshotImporter import ScreenshotImporter

from config import app

api = Api(app)

api.add_resource(Maintenance, '/api/')
api.add_resource(LogHistory, '/api/log')
api.add_resource(ScreenshotImporter, '/api/screenshot/<string:url>')

if __name__ == '__main__':
    app.run(debug=True)
