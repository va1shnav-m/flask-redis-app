from flask import Flask
import redis
import os

app = Flask(__name__)

redis_host=os.environ.get("REDIS_HOST", "redis")

r = redis.Redis(host='redis', port=6379)

@app.route('/')
def home():
    r.incr('counter')
    count = r.get('counter').decode('utf-8')

    return f"Visitor count: {count}"

app.run(host='0.0.0.0', port=5000)
