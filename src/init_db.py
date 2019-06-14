import os
from config import db
from models import Log

SAMPLE_DATA = [
    {'url': 'http://test1.com.co', 'status': 'failed', 'image_url': 'http://s3.aws.com/test1.png'},
    {'url': 'http://test2.com.co', 'status': 'sucessfull', 'image_url': 'http://s3.aws.com/test2.png'},
    {'url': 'http://test3.com.co', 'status': 'sucessfull', 'image_url': 'http://s3.aws.com/test3.png'}
]

basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'main.db')

if os.path.exists(dbfile):
    os.remove(dbfile)

db.create_all()

for url in SAMPLE_DATA:
    u = Log(url=url['url'], status=url['status'], image_url=url['image_url'])
    db.session.add(u)

db.session.commit()
