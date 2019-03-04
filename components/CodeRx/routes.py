import time
import os

import redis
from flask import url_for, send_from_directory, render_template

from CodeRx import app

cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    count = get_hit_count()
    # return 'Hello World! I have been seen {} times.\n'.format(count)
    return render_template('index.html', title='Home', count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)