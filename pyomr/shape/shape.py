import copy

import cv2

import numpy as np

from pyomr.img.colors import grayscale, binary_img


def get_shapes_from_barline(img):
    """
    :param img: The input image (should be a barline for optimal results)
    :type img: numpy.ndarray
    :type img: str
    :returns: Stripped version of original image
    :rtype: tuple (numpy.ndarray, numpy.ndarray)
    """
    img = binary_img(~grayscale(img))

    # To get vertical vs horizontal, we need to clone:
    horz = copy.copy(img)
    vert = copy.copy(img)

    horz_size, _ = horz.shape
    _, vert_size = vert.shape

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

        # For now, the user can choose the appropriate step
        cv2.imshow('Step {}'.format(i), h_img)
        if cv2.waitKey(0) == 13:
            cv2.destroyAllWindows()
            print('Ideal image selected')
            ret = h_img
            break

    return ~ret, ~v_img


def locate_notes(pure_img):
    """
    Using the Hough Circles Transform functions of CV2, find and
    mark all notes.
    :param img: The input image (should be a barline for optimal results)
    :type img: numpy.ndarray
    :type img: str
    :return:
    """

    if type(pure_img) is str:
        pure_img = cv2.imread(pure_img)

    note_width = specify_width(pure_img)

    img = get_shapes_from_barline(pure_img)[0]
    img = cv2.medianBlur(img, 3)
    bimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Detect circles
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, note_width,
                               param1=10, param2=8, minRadius=int(note_width / 2 - 10), maxRadius=int(note_width / 2 + 1))

    try:
        circles = np.uint16(np.around(circles))
    except AttributeError:
        circles = []
    else:
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(pure_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(pure_img, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.namedWindow('detected circles', cv2.WINDOW_NORMAL)
    cv2.imshow('detected circles', pure_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return pure_img


def specify_width(img):
    """

    :param img: A numpy ndarray representing the target image
    :returns: Width of note
    """
    coord = []

    def on_mouse(event, x, y, flags, param):

        nonlocal coord

        if event == cv2.EVENT_LBUTTONDOWN:
            coord.append(x)

    cv2.namedWindow('Select the bound of a note', cv2.WINDOW_NORMAL)

    cv2.setMouseCallback('Select the bound of a note', on_mouse)

    while len(coord) is not 2:
        cv2.imshow('Select the bound of a note', img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()

    return abs(coord[1] - coord[0])
