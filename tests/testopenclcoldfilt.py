import os

import numpy as np
from dtcwt.lowlevel import coldfilt as coldfilt_gold
from dtcwt.opencl.lowlevel import coldfilt
from dtcwt.coeffs import biort, qshift

from nose.tools import raises

from .util import assert_almost_equal

def setup():
    global lena
    lena = np.load(os.path.join(os.path.dirname(__file__), 'lena.npz'))['lena']

def test_lena_loaded():
    assert lena.shape == (512, 512)
    assert lena.min() >= 0
    assert lena.max() <= 1
    assert lena.dtype == np.float32

@raises(ValueError)
def test_odd_filter():
    coldfilt(lena, (-1,2,-1), (-1,2,1))

@raises(ValueError)
def test_different_size():
    coldfilt(lena, (-0.5,-1,2,1,0.5), (-1,2,-1))

@raises(ValueError)
def test_bad_input_size():
    coldfilt(lena[:511,:], (-1,1), (1,-1))

def test_real_wavelet():
    h0a, h0b, g0a, g0b, h1a, h1b, g1a, g1b = qshift('qshift_d')
    A = coldfilt(lena[:,:511], h1b, h1a)
    B = coldfilt_gold(lena[:,:511], h1b, h1a)
    assert_almost_equal(A, B)

def test_good_input_size():
    A = coldfilt(lena[:,:511], (-1,1), (1,-1))
    B = coldfilt_gold(lena[:,:511], (-1,1), (1,-1))
    assert_almost_equal(A, B)

def test_good_input_size_non_orthogonal():
    A = coldfilt(lena[:,:511], (1,1), (1,1))
    B = coldfilt_gold(lena[:,:511], (1,1), (1,1))
    assert_almost_equal(A, B)

def test_output_size():
    Y = coldfilt(lena, (-1,1), (1,-1))
    assert Y.shape == (lena.shape[0]/2, lena.shape[1])

    Z = coldfilt_gold(lena, (-1,1), (1,-1))
    assert_almost_equal(Y, Z)

# vim:sw=4:sts=4:et
