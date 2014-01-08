from flask import Flask, render_template, request, redirect, url_for
from random import choice
import json, redis, os, sys
from os.path import abspath, dirname

# list of images in the static folder
images = [i.strip() for i in os.listdir('static/images') if i != '' and i is not None]

# # initialize redis
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
rdb = redis.from_url(redis_url)

# intitialize app
app = Flask(__name__)
app.root_path = abspath(dirname(__file__))

# index page
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/<username>')
def user_index(username):

  # serve a random image that we haven't labeled yet
  completed = rdb.keys()
  images_to_label = [i for i in images if i not in completed]
  image = choice(images_to_label)

  return render_template(
    'home.html',
    user = username, 
    image = image, 
    images_left = len(images_to_label)
  )

# form post for label data
@app.route('/label/image/', methods=['POST'])
def label(): 
  
  # parse form
  value = json.loads(request.form['data'])
  
  # extract key
  key = value['image'].strip()

  # push to redis
  rdb.set(key, json.dumps(value))

  # redirect to a new image for this user
  user_url = url_for('user_index', username=value['user'])

  return redirect(user_url)

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)