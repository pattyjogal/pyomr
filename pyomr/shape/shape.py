import copy, math

import cv2

import numpy as np


import os

from pyomr.img.colors import grayscale, binary_img

from pyomr.theory.note import NoteName

π = np.pi

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
            cv2.MORPH_RECT,
            # TODO: Figure out why this has to be super low
            (500, i)
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
    print('Vert')
    cv2.imshow('Vert components', ~v_img)

    return ~ret, ~v_img


def locate_notes(pure_img):
    """
    Using the Hough Circles Transform functions of CV2, find and
    mark all notes.
    :param pure_img: The input image (should be a barline for optimal results)
    :type pure_img: numpy.ndarray
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
                               param1=10, param2=5, minRadius=int(note_width / 2 - 5), maxRadius=int(note_width / 2 + 2))

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

    return pure_img, circles


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


def locate_clef(img, clef):
    """
    Finds the bounds of the specified clef
    :param clef: The kind of clef to locate: treble, alto, or bass
    :type clef: str
    :param img:
    :return:
    """

    if type(img) is str:
        img = cv2.imread(img)

    if clef in ['alto', 'treble', 'bass']:
        dire = os.path.dirname(__file__)
        template = cv2.imread(os.path.join(dire, '../../img/{}.png').format(clef), 0)

    clef_width = specify_width(img)

    w, h = template.shape[::-1]

    ar = h / w

    h = int(ar * clef_width)

    w = clef_width

    template = cv2.resize(template, (w, h))

    cv2.imshow('template', template)
    cv2.waitKey(0)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.5
    loc = np.where(res >= threshold)

    ret = list(zip(*loc[::-1]))

    print(ret)

    for pt in ret:
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv2.imshow('im', img)
    cv2.waitKey(0)
    return img, ret, w, h

def get_clef_ref_note(clef_posns, clef_name, h):
    """
    Given a list of clef bounds and a type of clef, determine the location
    for the reference note, and what note that is.
    :param h:
    :param clef_posns:
    :param clef_name:
    :return:
    """

    ret = []

    if clef_name == 'alto':
        for pt in clef_posns:
            ret.append(int(pt[1] + h / 2))
        return ret, NoteName.C

def slice_notes(circles):
    pass


def get_barlines(img: [np.ndarray, str], sigma: float=0.33, θmax: float=0.3) -> np.ndarray:


    if type(img) is str:
        img = cv2.imread(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    v = np.median(gray)

    l = int(max(0, (1.0 - sigma) * v))
    u = int(min(255, (1.0 + sigma) * v))

    print(l,u)

    edges = cv2.Canny(gray, l, u, apertureSize=3)

    lines = cv2.HoughLines(edges, 1.3, π / 180, 50)

    # This list holds tuples that correspond to a line's endpoints and angle with the horizontal.
    # Format: ( (x1, y1),  (x2, y2), θ )
    line_details = []

    for ln in lines:
        ρ, θ = ln[0]
        a = np.cos(θ)
        b = np.sin(θ)
        x0 = a * ρ
        y0 = b * ρ
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        print(y1, y2, θ)

        # Because this function is just for barlines, no lines that are too vertical will be counted.
        # The most horizontal lines are selected, using the θmax
        if π / 2 + θmax >= θ >= π / 2 - θmax:
            # Uncomment to get the lines drawn on the image

            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
            line_details.append(((x1, y1), (x2, y2), θ))

    # For multiple detected lines, find groupings with a variance of 10 px, and average them into one line.
    avg_detected_lines = map(lambda y: int(sum(y) / len(y)), cluster([y[1] for y in [x[1] for x in line_details]], 10))

    return avg_detected_lines


def get_linespace(lines):
    pass




# From http://stackoverflow.com/questions/14783947/grouping-clustering-numbers-in-python
def cluster(data, maxgap):
    data.sort()
    groups = [[data[0]]]
    for x in data[1:]:
        if abs(x - groups[-1][-1]) <= maxgap:
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups
