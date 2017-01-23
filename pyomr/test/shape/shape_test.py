import cv2, numpy
import os
import logging

from pyomr.shape.shape import *
from pyomr.img.filters import *
from pyomr.img.transform import *


dir = os.path.dirname(__file__)
print(dir)
stock_img = os.path.join(dir, '../../../img/sheet_basic.png')
good_q_camera = os.path.join(dir, '../../../img/good_q_camera.jpg')
mild_music = os.path.join(dir, '../../../img/mild_music.jpg')
mtttp = os.path.join(dir, '../../../img/mtttp.jpg')
mtttp_flash = os.path.join(dir, '../../../img/flash.jpg')
mtttp_crump = os.path.join(dir, '../../../img/crumpled.jpg')
mtttp_vanilla = os.path.join(dir, '../../../img/vanilla.jpg')
russ = os.path.join(dir, '../../../img/russ.jpg')
gvb = os.path.join(dir, '../../../img/gvb.jpg')
etude = os.path.join(dir, '../../../img/etude_slice.jpg')


def test_kernel(src, name, numstep):

    cv2.imwrite('output/{}.png'.format(name), locate_notes(src)[0])

    # cimg, posns, w, h = locate_clef(src, 'alto')
    #
    # cv2.imwrite('clefs.png', cimg)
    #
    # for liny in get_clef_ref_note(posns, 'alto', h)[0]:
    #     print(liny)
    #     cimg = cv2.line(cimg, (0,liny), (2000,liny), (0,0,255), 1)
    #
    # cv2.imwrite('output/clefln_{}.png'.format(name), cimg)
    # cv2.imshow('Found clefline', cimg)
    # cv2.waitKey(0)
    #
    # img = cv2.imread(src)

    # cv2.imshow('Transformed', four_point_transform(img, pt_define_quadrangle(img)))
    # cv2.waitKey(0)

    cv2.imshow('Lines', get_barlines(src))
    cv2.waitKey(0)





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

def test_recognition(lily_notes, desc):
    import subprocess

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

    test_kernel(img_path, 'lily_{}'.format(desc), 4)
    # test_image_components('generated image', img_path)


# test_recognition(["b'", "c'", "a'", "g'"], 'small')
# test_recognition(["b'", "c'", "a'", "g'", "e'", "c''", "a'"], 'med')
# test_recognition(["b'", "c'", "a'", "g'", "e'", "c''", "a'"] + ["b'", "c'", "a'", "g'", "e'", "c''", "a'"] + ["b'", "c'", "a'", "g'", "e'", "c''", "a'"], 'large')
# test_kernel(stock_img, 'Scanned Music', 4)
# test_kernel(good_q_camera, 'Uneven Barline Music', 9)
# test_kernel(mild_music, 'PDF', 2)
# test_kernel(mtttp, 'MTTTP On a Computer Screen', 9)
# test_kernel(mtttp_crump, 'Crumpled up MTTTP', 9)
# test_kernel(mtttp_flash, 'Flash Photo of MTTTP', 9)
# test_kernel(mtttp_vanilla, 'Vanilla MTTTP', 9)
test_kernel(etude, 'Etude', 9)
# test_kernel(russ, 'Russian', 2)
# test_kernel(gvb, 'Grande Valse Brillante', 3)
# test_image_components('stock image', stock_img)
# test_image_components('good quality camera image', good_q_camera)
# test_filtered_image_components('stock image', stock_img)
# test_filtered_image_components('good quality camera image', good_q_camera)

