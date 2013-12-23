import os

images = [i.strip() for i in os.listdir('static/images') if i != '' and i is not None]
