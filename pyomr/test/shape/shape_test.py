import cv2
import os
import logging

from pyomr.shape.shape import *

dir = os.path.dirname(__file__)
print(dir)
stock_img = os.path.join(dir, '../../../img/sheet_basic.png')
good_q_camera = os.path.join(dir, '../../../img/good_q_camera.jpg')

def test_image_components(message, src):
    logging.info('Testing a ' + message)
    cv2.imshow('src', cv2.imread(src))
    cv2.waitKey(3000)
    cv2.destroyWindow('src')
    cv2.imshow('horiz', get_shapes_from_barline(src)[0])
    cv2.waitKey(3000)
    cv2.destroyWindow('horiz')
    cv2.imshow('vert', get_shapes_from_barline(src)[1])
    cv2.waitKey(3000)
    cv2.destroyWindow('vert')

test_image_components('stock image', stock_img)
test_image_components('good quality camera image', good_q_camera)




