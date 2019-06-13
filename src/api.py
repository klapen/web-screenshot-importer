from flask import Flask
from flask_restful import Resource, Api

from resources.LogHistory import LogHistory
from resources.Maintenance import Maintenance

from config import app

api = Api(app)

api.add_resource(Maintenance, '/')
api.add_resource(LogHistory, '/log')

if __name__ == '__main__':
    app.run(debug=True)
