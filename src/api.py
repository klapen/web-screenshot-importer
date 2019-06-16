import os
from flask import Flask
from flask_restful import Resource, Api

from resources.LogHistory import LogHistory
from resources.Maintenance import Maintenance
from resources.ScreenshotImporter import ScreenshotImporter

from config import app

api = Api(app)
api.add_resource(Maintenance, '/api/')
api.add_resource(LogHistory, '/api/log')
api.add_resource(ScreenshotImporter, '/api/screenshot')

if __name__ == '__main__':
    HOST = '127.0.0.1' if os.environ.get('EQ_HOST') == '' else os.environ.get('EQ_HOST')
    HOST_PORT = 5000 if os.environ.get('EQ_PORT') == '' else os.environ.get('EQ_PORT')
    app.run(debug=True, host=HOST, port=HOST_PORT)
