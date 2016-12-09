import cv2, numpy
import os
import logging

from pyomr.shape.shape import *
from pyomr.img.filters import *

import matplotlib.pyplot as plt
from scipy.interpolate import spline, splev, splrep
from scipy.signal import argrelextrema

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


def test_kernel(src, name, numstep):

    cv2.imwrite('output/{}.png'.format(name), locate_notes(src))

    img = binary_img(~grayscale(src))
    oimg = cv2.imread(src, 0)
    # To get vertical vs horizontal, we need to clone:
    horz = copy.copy(img)
    vert = copy.copy(img)

    horz_size, _ = horz.shape
    _, vert_size = vert.shape

    last_h_img = None

    x_plot = np.array([0])
    y_plot = np.array([0])
    dpstep = 0
    # Start by extracting the horizontal elements
    for i in range(1, 20):
        print(horz_size)
        h_kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (i, i)
        )

        h_img = cv2.morphologyEx(
            img,
            cv2.MORPH_OPEN,
            h_kernel
        )

        # Continue by extracting the vertical elements

        v_kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            # TODO: Figure out why this has to be super low
            (int(horz_size / 9), 4

             )
        )

        v_img = cv2.morphologyEx(
            img,
            cv2.MORPH_OPEN,
            v_kernel
        )
        dp = 0
        if last_h_img is not None:
            dp = (np.count_nonzero(last_h_img)) - (np.count_nonzero(h_img))
            print('{}: On trial {}, we lost {} px from the last image'.format(name,i, dp))
        last_h_img = h_img

        cv2.imwrite('kernel/' + name + '_' + str(i) + '_kernel_dp_{}.png'.format(dp), h_img)

        if i is numstep:
            dpstep = dp
            good_img = h_img
            cv2.imwrite('{}_ideal.png'.format(name), ~good_img)

        x_plot = np.append(x_plot, i)
        y_plot = np.append(y_plot, dp)

    # Try and find a best fit curve
    x_smooth = np.linspace(x_plot.min(), x_plot.max(), 300)
    y_smooth = spline(x_plot, y_plot, x_smooth)
    minm = argrelextrema(y_smooth, np.less)
    print(minm)


    plt.annotate('Accepted point', xy=(numstep, dpstep), xytext=(numstep + 3, dpstep + 100), arrowprops=dict(facecolor='black', shrink=0.05))
    plt.plot(x_plot, y_plot)
    plt.plot(x_smooth, y_smooth)
    plt.suptitle('{}: Loss of Pixels per Step'.format(name), fontsize=14, fontweight='bold')
    plt.draw()
    plt.savefig('{}_trend.png'.format(name))
    plt.clf()

    # Show keypoints
    pure_img = cv2.imread(src,)
    img = cv2.medianBlur(~good_img, 3)
    bimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    print('Testing Hough Circles')

    # Detect circles
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 5,
                               param1=10, param2=10, minRadius=1, maxRadius=20)
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(pure_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(pure_img, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.imwrite('detected_circle_{}.png'.format(name), pure_img)
    cv2.imshow('detected circles', pure_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

    test_kernel(img_path, 'lily_{}'.format(desc), 4)
    # test_image_components('generated image', img_path)


test_recognition(["b'", "c'", "a'", "g'"], 'small')
test_recognition(["b'", "c'", "a'", "g'", "e'", "c''", "a'"], 'med')
test_recognition(["b'", "c'", "a'", "g'", "e'", "c''", "a'"] + ["b'", "c'", "a'", "g'", "e'", "c''", "a'"] + ["b'", "c'", "a'", "g'", "e'", "c''", "a'"], 'large')
test_kernel(stock_img, 'Scanned Music', 4)
test_kernel(good_q_camera, 'Uneven Barline Music', 9)
test_kernel(mild_music, 'PDF', 2)
test_kernel(mtttp, 'MTTTP On a Computer Screen', 9)
test_kernel(mtttp_crump, 'Crumpled up MTTTP', 9)
test_kernel(mtttp_flash, 'Flash Photo of MTTTP', 9)
test_kernel(mtttp_vanilla, 'Vanilla MTTTP', 9)
test_kernel(russ, 'Russian', 2)
test_kernel(gvb, 'Grande Valse Brillante', 3)
# test_image_components('stock image', stock_img)
# test_image_components('good quality camera image', good_q_camera)
# test_filtered_image_components('stock image', stock_img)
# test_filtered_image_components('good quality camera image', good_q_camera)
