'''
This sub-module provides image coloration functions
'''
import cv2
import numpy

from pyomr.img.core import _

def grayscale(src):

    """
    :param src: The input image or image path to be converted to grayscale
    :type src: str
    :type src: numpy.ndarray
    :returns: Grayscale version of src image
    :rtype: numpy.ndarray
    """
    # If the file is not found, raise a FileNotFoundError

    img = _(src, cv2.IMREAD_UNCHANGED)

    if not img.data:
        raise FileNotFoundError

    if len(img.shape) < 3:
        gray = img
    elif img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    return gray

def binary_img(img):

    """
    :param img: The image to be transformed to binary
    :type img: numpy.ndarray
    :returns: Binary version of image
    :rtype: numpy.ndarray
    """
    return cv2.threshold(
        img,
        240,
        255,
        cv2.THRESH_BINARY+cv2.THRESH_OTSU
    )[1]