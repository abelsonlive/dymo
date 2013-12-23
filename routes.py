from flask import Flask, render_template, request, redirect, url_for
from random import choice
import json

from rdb import rdb
from images import images

app = Flask(__name__)

@app.route('/')
def home():

  # serve a random image that we haven't labeled yet
  completed = rdb.keys()
  images_to_label = [i for i in images if i not in frozenset(completed)]
  image = choice(images_to_label)

  return render_template('home.html', image = image, images_left = len(images_to_label))


@app.route('/label', methods=['POST'])
def label_image(): 
  
  # parse form
  value = json.loads(request.form.copy()['data'])

  # extract key
  key = value['image']

  # push ro redis
  rdb.set(key, json.dumps(value))

  # redirect of a new image
  return redirect(url_for('home'))
  
if __name__ == '__main__':
  app.run(debug=True, port=3030)
