from flask_restful import Resource
from src.config import db
from urllib.request import urlopen

from src.models import (
    Log,
    LogSchema
)

class ScreenshotImporter(Resource):
    def get(self, url):
        try:
            urlopen(url)
        except:
            return { 'message': 'Not valid URL'}, 400

        return { 'url_requested': url }

