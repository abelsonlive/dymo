from flask import Flask, render_template, request, redirect, url_for
from random import choice
import json, redis, os, sys
from os.path import abspath, dirname
import hashlib

# list of images in the static folder
images = [i.strip() for i in os.listdir('static/images') if i != '' and i is not None]

# create lookup
lookup = {}
for i in images:
  hash_object = hashlib.sha1(i)
  hex_dig = hash_object.hexdigest()
  lookup[i] = hex_dig

print lookup

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

@app.route('/<image>/')
def user_index(image):

  # serve a random image that we haven't labeled yet
  return render_template(
    'home.html',
    image = image.strip()
  )

# form post for label data
@app.route('/label/image/', methods=['POST'])
def label(): 
  
  # parse form
  value = json.loads(request.form['data'])
  
  # extract key
  key = value['image'].strip()

  # lookup
  secret_key = lookup[key]

  # push to redis
  rdb.append(key, json.dumps(value))

  return "<h1>Thanks!</h1><p>Please input <b>%s</b> on Mechanical Turk</p>" % secret_key

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)