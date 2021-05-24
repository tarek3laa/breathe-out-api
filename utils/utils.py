import os
import matplotlib.pyplot as plt
from pydicom import dcmread
import numpy as np


def get_view(dcmdir):
    files = []
    for fname in os.listdir(dcmdir):
        files.append(dcmread(dcmdir + fname))
    print("file count: {}".format(len(files)))
    slices = []
    skipcount = 0
    for f in files:
        if hasattr(f, 'SliceLocation'):
            slices.append(f)
        else:
            skipcount = skipcount + 1
    print("skipped, no SliceLocation: {}".format(skipcount))
    # ensure they are in the correct order
    slices = sorted(slices, key=lambda s: s.SliceLocation)

    ps = slices[0].PixelSpacing
    ss = slices[0].SliceThickness
    ax_aspect = ps[1] / ps[0]
    sag_aspect = ps[1] / ss
    cor_aspect = ss / ps[0]

    # create 3D array
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        img3d[:, :, i] = img2d
    return img3d
