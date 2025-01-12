from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from astropy.io.fits.hdu.hdulist import HDUList


def _to_ms2(
        hdulist: 'HDUList',
        msfile: str,
        overwrite: bool = False
) -> bool:
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
    return False
