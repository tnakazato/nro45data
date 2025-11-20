#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

import os
import time

import astropy.io.fits as fits
import pytest

from nro45data.psw import nqm2fits
from nro45data import nqm2fits as nqm2fits_pkg

def test_nqm2fits(data_dir):
    """test nqm2fits"""
    nqmfile = "nmlh40.240926005833.01.nqm"
    nqmpath = os.path.join(data_dir, nqmfile)
    fitsfile = ".".join([nqmpath, time.strftime("%Y%M%dT%H%M%S"), 'fits'])
    for test_func in [nqm2fits, nqm2fits_pkg]:
        try:
            status = test_func(nqmpath, fitsfile, overwrite=True)
            assert status is True
            fitsdata = fits.open(fitsfile)
            assert isinstance(fitsdata, fits.HDUList)
            assert len(fitsdata) == 2
        finally:
            os.remove(fitsfile)


@pytest.mark.unit
def test_nqm2fits_invalid_nqmfile():
    """test nqm2fits with invalid nqmfile"""
    nqmfile = "invalid.nqm"
    fitsfile = "test.fits"
    with pytest.raises(FileNotFoundError):
        nqm2fits(nqmfile, fitsfile, overwrite=True)
