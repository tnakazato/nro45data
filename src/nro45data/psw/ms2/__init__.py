import logging
import os
import shutil
from typing import TYPE_CHECKING

from nro45data.psw.ms2.builder import build_ms2
from nro45data.psw.ms2.filler import fill_ms2

if TYPE_CHECKING:
    from astropy.io.fits.hdu.hdulist import HDUList

LOG = logging.getLogger(__name__)


def _to_ms2(hdulist: "HDUList", msfile: str, overwrite: bool = False) -> bool:
    """Export HDUList to MeasurementSet v2.

    Not implemented yet.

    Args:
        hdulist: HDUList generated from NRO 45m PSW file (.nqm)
        fitsfile: Output MSv2 file name
        overwrite: Overwrite existing output file or not.
            Default is False (not overwrite).

    Returns:
        Export status. True is successful.
    """
    if os.path.exists(msfile) and not overwrite:
        raise FileExistsError(f"Abort since {msfile} exists and overwrite is False")

    if os.path.exists(msfile):
        LOG.info(f'Overwrite existing {msfile}...')
        shutil.rmtree(msfile)

    build_ms2(msfile)
    fill_ms2(msfile, hdulist[0])

    return True
