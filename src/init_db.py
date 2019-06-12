import os
from config import db
from models import Log

SAMPLE_DATA = [
    {'url': 'http://test1.com.co', 'status_code': 200},
    {'url': 'http://test2.com.co', 'status_code': 404},
    {'url': 'http://test3.com.co', 'status_code': 200}
]

basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'main.db')

if os.path.exists(dbfile):
    os.remove(dbfile)

db.create_all()

for url in SAMPLE_DATA:
    u = Log(url=url['url'], status_code=url['status_code'])
    db.session.add(u)

db.session.commit()
