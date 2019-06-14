from flask_restful import Resource, reqparse
from config import db
from urllib.request import urlopen
import requests
from flask import make_response

from models import (
    Log,
    LogSchema
)

ALLOWED_STATUS = ['sucessfull', 'failed']

def _getResponse(content):
    response = make_response(content)
    response.headers.set('Content-Type', 'image/png')
    return response

class ScreenshotImporter(Resource):
    def _saveInLog(self, url, status, image_url):
        if status not in ALLOWED_STATUS:
            return False
        try:
            item = Log(url=url, status=status, image_url=image_url)
            db.session.add(item)
            db.session.commit()
            return True
        except Exception as err:
            print('saveInLog - Error saving on DB: %s' % err)
            return False

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
        
