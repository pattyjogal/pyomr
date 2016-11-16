import copy

import cv2

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
    print(horz_size)
    h_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (int(horz_size / 4.33333), 1)
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
        (1, 2)
    )

    v_img = cv2.morphologyEx(
        img,
        cv2.MORPH_OPEN,
        v_kernel
    )

    return (~h_img, ~v_img)
