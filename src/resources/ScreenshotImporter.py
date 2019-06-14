from flask_restful import Resource, reqparse
from config import db
from urllib.request import urlopen
import requests
from flask import make_response

from models import (
    Log,
    LogSchema
)

def _getResponse(content):
    response = make_response(content)
    response.headers.set('Content-Type', 'image/png')
    return response

class ScreenshotImporter(Resource):
    def importScreenshot(self, url):
        if url == '':
            return {'error': 'URL cannot be blank'}, 400
        
        try:
            urlopen(url)
        except:
            return { 'error': 'Not valid URL' }, 400

        res = requests.get('https://image.thum.io/get/%s' % url)
        return _getResponse(res.content)
        
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('url', required=True, help="URL argument is required.")
        
        args = parse.parse_args()
        url = args['url']

        return self.importScreenshot(url)
        
