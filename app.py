import schedule
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime
from twitter import *
import config
from flask_restful import Resource, Api
import json
from threading import Thread

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(500), primary_key=True)

    def __repr__(self):
        return "{ id : '%s' , created : '%s' , status : '%s' }" % (self.id,self.created,self.status)


twitter = Twitter(auth = OAuth(config.access_key,
                  config.access_secret,
                  config.consumer_key,
                  config.consumer_secret))

class MessageList(Resource):
    def get(self):
        return [ json.loads(m.status)  for m in Message.query.all() ]

def job():
    print("start :")
    statuses = twitter.statuses.home_timeline(count = 200)
    print("loading : '%d'",len(statuses))
    for status in statuses:
        created = datetime.strptime(status["created_at"],'%a %b %d %H:%M:%S +0000 %Y')
        id = status['id']
        if Message.query.filter_by(id=id).count() == 0 :
            msg = Message(id=id,created=created,status=json.dumps(status))
            db.session.add(msg)
            db.session.commit()

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


api = Api(app)
api.add_resource(MessageList, '/messages')
if __name__ == '__main__':
    schedule.every(10).minutes.do(job)
    t = Thread(target=run_schedule)
    t.start()
    app.run(debug=True)