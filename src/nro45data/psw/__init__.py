import logging

from .io.fits import _read_psw
from .io.fits import _to_fits
from .ms2 import _to_ms2
from .ms4 import _to_ms4


logging.basicConfig(
    format="%(asctime)s\t%(levelname)s\t%(funcName)s\t%(message)s",
    # format='%(levelname)s %(message)s',
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)


def nqm2fits(nqmfile: str, fitsfile: str, overwrite: bool = False) -> bool:
    """Convert NRO45m PSW data (.nqm) to FITS.

    Args:
        nqmfile: Input NRO45m PSW file name
        fitsfile: Output FITS file name
        overwrite: Overwrite existing output file or not.
            Default is False (not overwrite).

    Returns:
        Conversion status. True is successful.
    """
    hdulist = _read_psw(nqmfile)
    return _to_fits(hdulist, fitsfile, overwrite)


def nqm2ms2(nqmfile: str, msfile: str, overwrite: bool = False) -> bool:
    """Convert NRO45m PSW data (.nqm) to MeasurementSet v2.

    Not implemented yet.

    Args:
        nqmfile: Input NRO45m PSW file name
        msfile: Output MSv2 file name
        overwrite: Overwrite existing output file or not.
            Default is False (not overwrite).

    Returns:
        Conversion status. True is successful.
    """
    hdulist = _read_psw(nqmfile)
    return _to_ms2(hdulist, msfile, overwrite)


def nqm2ms4(nqmfile: str, psfile: str, overwrite: bool = False) -> bool:
    """Convert NRO45m PSW data (.nqm) to MeasurementSet v4 (ProcessingSet).

    Not implemented yet.

    Args:
        nqmfile: Input NRO45m PSW file name
        psfile: Output MSv4 (ProcessingSet) file name
        overwrite: Overwrite existing output file or not.
            Default is False (not overwrite).

    Returns:
        Conversion status. True is successful.
    """
    hdulist = _read_psw(nqmfile)
    return _to_ms4(hdulist, psfile, overwrite)
