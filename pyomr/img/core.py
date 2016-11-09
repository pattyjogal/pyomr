import cv2
import numpy


def _(src, flag):
    '''
    Makes sure source input is an ndarray
    :param source: The image source/path
    :type source: str
    :type source: numpy.ndarray
    :return:
    '''
    if type(src) is str:
        img = cv2.imread(src, flag)
    elif type(src) is numpy.ndarray:
        img = src
    else:
        raise TypeError

    return img