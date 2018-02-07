import os
from flask import Flask,request
from redis import Redis

app = Flask(__name__)
redis = Redis(host=os.environ.get('REDIS_HOST') or '0.0.0.0',port=6379)

@app.route('/')
def Hi():
    ip = request.remote_addr
    count = redis.get('touch')

    if redis.ttl(ip):
        return "<h1>Hello {0} from the other side {1} </h1> Last login time is {2}".format(ip,count,redis.ttl(ip))
    else:
        count = redis.incr('touch')
        redis.set(ip,'0',ex=36)  # cache the ip address into redis , set expire time
        return "<h1>Hello {0} from the other side {1} </h1> New Joiner !!!".format(ip,count,redis.get(ip))

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)

