#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:14:55 2020

@author: patrickmayerhofer

modfied on Mon Jun  3 13:38:32 2024

@author: sabrinalee

This library was created for the use in the open source Wearables Course BPK409, Lab3 - EMG
For more information: 
    https://docs.google.com/document/d/e/2PACX-1vTr1zOyrUedA1yx76olfDe5jn88miCNb3EJcC3INmy8nDmbJ8N5Y0B30EBoOunsWbA2DGOVWpgJzIs9/pub
"""

import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import pandas as pd



""" This function does an FFT and returns the power spectrum of data
    Input: Data, sampling frequency
    Output: Power, the respective frequencies of the power spectrum
   """
def get_power(data, sfreq):
    sig_fft = fftpack.fft(data)
    
    # And the power (sig_fft is of complex dtype)
    power = np.abs(sig_fft)
    
    # The corresponding frequencies
    sample_freq1 = fftpack.fftfreq(data.size, d=1/sfreq)
    frequencies = sample_freq1[sample_freq1 > 0]
    power = power[sample_freq1 > 0]
    return power, frequencies

