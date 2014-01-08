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

# # test index page
# @app.route('/')
# def index():
#   return render_template('index.html')

# index page
@app.route('/')
def index():

  # serve a random image that we haven't labeled yet
  completed = rdb.keys()
  images_to_label = [i for i in images if i not in frozenset(completed)]
  image = choice(images_to_label)

  return render_template('home.html', image = image, images_left = len(images_to_label))

# form post for label data
@app.route('/label', methods=['POST'])
def label_image(): 
  
  # parse form
  value = json.loads(request.form.copy()['data'])
  
  # extract key
  key = value['image']

  # push to redis
  rdb.set(key, json.dumps(value))

  # redirect to a new image
  return redirect(url_for('index'))

@app.after_request
def add_header(responase):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)