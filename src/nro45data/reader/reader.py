from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from astropy.io.fits.hdu.hdulist import HDUList

from .psw import _read_psw


def read(filename: str, mode: str = 'psw') -> 'HDUList':
    """Read NRO 45m data.

    Args:
        filename: Name of the data
        mode: Observation mode. Either 'psw' or 'otf'.

    Returns:
        ``astropy.io.fits.hdu.hdulist.HDUList`` object

        (the same object returned by ``astropy.io.fits.open``)
    """
    if mode.upper() == 'PSW':
        return _read_psw(filename)
    elif mode.upper() == 'OTF':
        raise NotImplementedError('OTF mode is not supported yet.')
    else:
        raise RuntimeError(f'Invalid mode: {mode}.')