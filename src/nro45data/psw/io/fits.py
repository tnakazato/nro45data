from typing import List, Tuple, TYPE_CHECKING

import astropy.io.fits as fits

if TYPE_CHECKING:
    from astropy.io.fits.hdu.hdulist import HDUList


def _to_fits(hdulist: 'HDUList', fitsfile: str, overwrite: bool = False) -> bool:
    """Export HDUList to FITS.

    Args:
        hdulist: HDUList generated from NRO 45m PSW file (.nqm)
        fitsfile: Output FITS file name
        overwrite: Overwrite existing output file or not.
            Default is False (not overwrite).

    Returns:
        Export status. True is successful.
    """
    status = True

    primary_hdu = fits.PrimaryHDU()
    output_hdulist = fits.HDUList([primary_hdu, hdulist[0]])

    try:
        output_hdulist.writeto(
            fitsfile,
            output_verify='fix+warn',
            overwrite=overwrite
        )
    except Exception as e:
        print(e)
        status = False

    return status