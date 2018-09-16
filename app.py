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

app = Flask(__name__, static_folder='static')
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
        return [ json.loads(m.status)  for m in Message.query.order_by(Message.created.desc()).all() ]

def job():
    print("updating :")
    statuses = twitter.statuses.home_timeline(count = 200)
    print("loading : '%d'",len(statuses))
    for status in statuses:
        created = datetime.strptime(status["created_at"],'%a %b %d %H:%M:%S +0000 %Y')
        id = status['id']
        q = db.session.query(Message).filter(Message.id==id)
        if db.session.query(q.exists()).scalar():
            try:
                msg = Message(id=id,created=created,status=json.dumps(status))
                db.session.add(msg)
                db.session.commit()
            except Exception as e: print(e)

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)

@app.route('/')
def show_entries():
    #return render_template('search.html', query=None, entries=None)
    return app.send_static_file('index.html')


api = Api(app)
api.add_resource(MessageList, '/messages')
if __name__ == '__main__':
    schedule.every(10).minutes.do(job)
    t = Thread(target=run_schedule)
    t.start()
    app.run(debug=True)
