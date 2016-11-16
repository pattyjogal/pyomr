import cv2, numpy
import os
import logging

from pyomr.shape.shape import *
from pyomr.img.filters import *

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

def test_filtered_image_components(message, src):
    logging.info('Testing a ' + message)
    cv2.imshow('src', histo_equal(src))
    cv2.waitKey(3000)
    cv2.destroyWindow('src')
    cv2.imshow('horiz', get_shapes_from_barline(histo_equal(src))[0])
    cv2.waitKey(3000)
    cv2.destroyWindow('horiz')
    cv2.imshow('vert', get_shapes_from_barline(histo_equal(src))[1])
    cv2.waitKey(3000)
    cv2.destroyWindow('vert')

def test_recognition(lily_notes):
    import subprocess
    from PIL import Image

    lily_string = '{\n'

    for note in lily_notes:
        lily_string += note + ' '

    lily_string += '\n}'
    bytes(lily_string, 'utf8')
    with open('current_sheet_test.ly', 'w') as f:
        f.write(lily_string)
        path = f.name
        f.close()

    command = ('lilypond', '-fpng', '-dpreview', path)
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               shell=True,
                               env={'PATH':
                                    'C:\\Program Files (x86)\\LilyPond\\usr\\bin'})

    (out, err) = process.communicate()
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))

    img_path = dir_path + '\\' + path[:-2] + 'preview.png'

    test_image_components('generated image', img_path)


test_recognition(["b'", "c'", "a'", "g'"])
test_recognition(["b'", "c'", "a'", "g'", "e'", "c''", "a'"])
test_recognition(["b'", "c'", "a'", "g'", "e'", "c''", "a'"] + ["b'", "c'", "a'", "g'", "e'", "c''", "a'"] + ["b'", "c'", "a'", "g'", "e'", "c''", "a'"])

test_image_components('stock image', stock_img)
test_image_components('good quality camera image', good_q_camera)
# test_filtered_image_components('stock image', stock_img)
# test_filtered_image_components('good quality camera image', good_q_camera)

