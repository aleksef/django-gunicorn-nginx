import cv2
from PIL import Image
import imghdr
import numpy as np


def process_user_image(uploaded_img):
    img = cv2.cvtColor(np.array(Image.open(uploaded_img)), cv2.COLOR_BGR2RGB)

    h = len(img)
    w = len(img[0])
    print(h)
    print(w)
    if h < w:
        img = img[int(0):int(h),
                  int(w/2-h/2):int(w/2+h/2)]
    if h > w:
        img = img[int(h/2-w/2):int(h/2+w/2),
                  int(0):int(w)]
    
    return cv2.resize(img, (150, 150))

def check_image(uploaded_img, min_height, min_width, max_size):
    '''
    "uploaded image" takes in Django uploaded file type from the request
    '''
    def check_img_header(uploaded_img):
        return imghdr.what(uploaded_img) == "jpeg" or imghdr.what(uploaded_img) == "png"
    def check_file_size(uploaded_img):
        return uploaded_img.size <= 2000000 and uploaded_img.size > 0
    def check_img_dims(uploaded_img):
        img = np.array(Image.open(uploaded_img))
        h = len(img)
        w = len(img[0])
        return h >= 150 and w >= 150    
    return check_img_header(uploaded_img) and check_file_size(uploaded_img) and check_img_dims(uploaded_img)
