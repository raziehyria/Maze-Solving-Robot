import cv2
import numpy as np
import urllib.request as url

def get_image(image_url):
    url_response_image = url.urlopen(image_url)
    image_as_np_array = np.array(bytearray(url_response_image.read()), dtype=np.uint8)
    image = cv2.imdecode(image_as_np_array, -1)
    return image

def has_straight_path(image):
    pass

def has_right_path(image):
    pass

def has_left_path(image):
    pass

def has_reached_end(image):
    pass
