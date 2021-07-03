from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

import pywavefront


def import_obj(object_file: str = 'model.obj'):
    """Represents object file in matplotlib. """
    object = pywavefront.Wavefront(object_file)


def resize_image():
    pass


def project_image():
    pass

def rotate_image():
    pass
