# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 10:49:37 2024

@author: logan
"""
import numpy as np
import matplotlib.pyplot as plt
from astropy.io.fits import getdata
from astropy.io import fits
import glob
import os
from scipy import stats
import pandas as pd

img = r"D:\OneDrive - Arizona State University\SPARCS Documents\Logan Working\Phase2\Data\Flats\20240712_flatattempt\20240712_142236_NUV_FFI.fits"
with fits.open(img, mode='readonly') as hdulist:
    header = hdulist[0].header
    data = hdulist[0].data
    
    
#%%
# Astronomy Specific Imports
from astropy.modeling import models, fitting


# Fitting - Polynomial2D
# This example is taken from the Astropy Modeling documentation

# Generate fake data
np.random.seed(0)
y, x = np.mgrid[:1033, :1175]
z = data 

z = z[50:-50,200:1000] #trimming off overscan and bright curve
y, x = np.mgrid[:933, :800] #trimmed x and y

# Fit the data using astropy.modeling
p_init = models.Polynomial2D(degree=9)
fit_p = fitting.LevMarLSQFitter()
p = fit_p(p_init, x, y, z)

#%%
from scipy.ndimage import gaussian_filter

filtered = gaussian_filter(data,sigma=1,radius=25)
plt.imshow(data/filtered)


#%%
# Plot the data with the best-fit model
plt.figure(figsize=(8, 2.5))
plt.subplot(1, 3, 1)
plt.imshow(z, origin='lower', interpolation='nearest', vmin=-1e4, vmax=5e4)
plt.title("Data")
plt.subplot(1, 3, 2)
plt.imshow(p(x, y), origin='lower', interpolation='nearest', vmin=-1e4,
           vmax=5e4)
plt.title("Model")
plt.subplot(1, 3, 3)
plt.imshow(z - p(x, y), origin='lower', interpolation='nearest', vmin=-1e4,
           vmax=5e4)
plt.title("Residual")

data = z - p(x, y)
hdu = fits.PrimaryHDU(data=data/filtered)
hdu.writeto(r'C:\Users\logan\Desktop\residual.fits')





