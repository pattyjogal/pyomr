import numpy as np
import cv2

from pyomr.img.core import _
from pyomr.img.colors import grayscale

def histo_equal(src):
    '''
    This function takes an image and performs
    an adaptive histogram equalization on it
    for smoother lighting.
    :param src: The image to be smoothed
    :type src: str
    :type src: numpy.ndarray
    :return:
    '''
    img = grayscale(src)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    ret = clahe.apply(img)

    return ret