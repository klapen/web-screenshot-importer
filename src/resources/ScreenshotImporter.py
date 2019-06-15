from flask_restful import Resource, reqparse
from config import db
from urllib.request import urlopen
import requests, uploader, tldextract, datetime
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
        if res.status_code != 200:
            return { 'error': 'Problems creating the screenshot' }, res.status_code

        if 'thum_status_code' in res.headers and res.headers['thum_status_code'] == '200':
            tldex = tldextract.extract(url)
            now_text = str(datetime.datetime.now()).replace(' ','_')
            filename = tldex.domain+'.'+tldex.suffix+'/'+tldex.subdomain+'/screenshot-'+now_text+'.png'
            image_url = uploader.send_image(filename, res.content)
            self._saveInLog(url, 'sucessfull', image_url)
            return _getResponse(res.content)
        else:
            return { 'error': 'Could not generate screenshot' }, 204
        
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('url', required=True, help="URL argument is required.")
        
        args = parse.parse_args()
        url = args['url']

        return self.importScreenshot(url)
        
