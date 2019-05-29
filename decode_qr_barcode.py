from __future__ import print_function
import os
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

@app.route('/')
def main():
    return "Hello qr barcode"

@app.route('/qr-barcode', methods=["GET"])
def qr():
      # Read the URL
    try:
        url = request.get_json()['image_url']
    except TypeError:
        print("TypeError trying get_json(). Trying to load from string.")
        try:
            data = json.loads(request.data.decode('utf-8'), encoding='utf-8')
            url = data['img_url']
        except:
            return jsonify(
                {"error": "Could not get 'image_url' from the request object. Use JSON?",
                 "data": request.data}
            )
    except:
        return jsonify(
            {"error": "Non-TypeError. Did you send {'image_url': 'http://.....'}",
             "data": request.data }
        )

    # Process the image
    print("URL extracted:", url)
    try:
        output = decode(url)
    except OSError:
        return jsonify({"error": "URL not recognized as image.",
                        "url": url})
    except:
        return jsonify(
            {"error": "Unknown processing image.",
             "request": request.data}
        )
    app.logger.info(output)
    return jsonify({"output": output.data})

def decode(im):
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)

  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data, '\n')

  return decodedObjects


# Display barcode and QR code location
def display(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects:
    points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4:
      hull = cv2.convexHull(
          np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else:
      hull = points

    # Number of points in the convex hull
    n = len(hull)

    # Draw the convext hull
    for j in range(0, n):
      cv2.line(im, hull[j], hull[(j+1) % n], (255, 0, 0), 3)

  # Display results
  cv2.imshow("Results", im)
  cv2.waitKey(0)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("Started app.py on port: {port}")
    app.run(host='0.0.0.0', port=port)

# Main
# if __name__ == '__main__':

#   # Read image
#   im = cv2.imread('zbar-location.png')

#   decodedObjects = decode(im)
#   display(im, decodedObjects)
