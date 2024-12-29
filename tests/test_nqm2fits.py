#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

import os

import astropy.io.fits as fits
import pytest

from nro45data.psw import nqm2fits

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


@pytest.mark.skip(reason='test data not registered yet')
def test_nqm2fits():
    """test nqm2fits"""
    nqmfile = os.path.join(DATA_DIR, 'T12tztu.140321203430.01.nqm')
    fitsfile = 'test.fits'
    status = nqm2fits(nqmfile, fitsfile, overwrite=True)
    assert status is True
    fitsdata = fits.open(fitsfile)
    os.remove(fitsfile)


@pytest.mark.unit
def test_nqm2fits_invalid_nqmfile():
    """test nqm2fits with invalid nqmfile"""
    nqmfile = 'invalid.nqm'
    fitsfile = 'test.fits'
    with pytest.raises(FileNotFoundError):
        nqm2fits(nqmfile, fitsfile, overwrite=True)

