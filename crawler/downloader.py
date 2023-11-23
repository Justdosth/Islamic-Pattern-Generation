import requests
import numpy as np
from PIL import Image
from io import BytesIO
import json
import time
import base64
from datauri import DataURI
import os

imageUrls = []
with open("/Users/myhouse/Desktop/links/imageUrlsMerged_1614196173.6417174_imgNum_1509.json", "r") as f:
  imageUrls = json.load(f)
folderName = './images_'+str(time.time())
os.mkdir(folderName)

for imageUrl in imageUrls:
  arr = None
  try:
    r = requests.get(imageUrl, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True
        try:
            image = Image.open(BytesIO(r.content))
            grayscale = image.convert("L")
            arr = np.array(grayscale)
        except Exception as e:
            print(e)
  except  requests.exceptions.InvalidSchema:
    try:
        image = Image.open(BytesIO(DataURI(imageUrl).data))
        grayscale = image.convert("L")
        arr = np.array(grayscale)
    except Exception as e:
        print(e)

  #Convert image to black and white:

  for i in range(0, len(arr)):
      for j in range(0, len(arr[i])):
          if arr[i][j] >= 155:
              arr[i][j] = 255
          else:
              arr[i][j] = 0
              
  img = Image.fromarray(arr)
  #img.thumbnail((28,28),Image.ANTIALIAS)
  img.save(folderName+'/'+str(time.time())+'.png')
