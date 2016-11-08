'''
This sub-module provides image coloration functions
'''
import cv2
import numpy


def grayscale(src):

    """
    :param src: The input image or image path to be converted to grayscale
    :type src: str
    :type src: numpy.ndarray
    :returns: Grayscale version of src image
    :rtype: numpy.ndarray
    """
    img = None

    if type(src) is str:
        img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    elif type(src) is numpy.ndarray:
        img = src
    else:
        raise TypeError
    # If the file is not found, raise a FileNotFoundError
    if not img.data:
        raise FileNotFoundError

    if img.shape[2] == 3:
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
    return cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        15,
        -2
    )