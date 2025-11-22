from __future__ import annotations

import logging
from typing import Generator, TYPE_CHECKING

import numpy as np

from .utils import fill_ms_table, get_array_configuration, get_data_description_map

if TYPE_CHECKING:
    import astropy.io.fits as fits
    BinTableHDU = fits.BinTableHDU

LOG = logging.getLogger(__name__)


def pol_str_to_enum(pols: list[str]) -> list[int]:
    """Map polarization string to polarization enum.

    See following link for Stokes enumeration:

    https://casacore.github.io/casacore/classcasacore_1_1Stokes.html

    Args:
        pols: List of polarization strings.

    Returns:
        List of polarization enums.

    Raises:
        AssertionError: If polarization string is not any of 'H', 'V', 'R', 'L'.
    """
    if len(pols) == 1:
        pol_type = pols[0][-1]
        if pol_type == "H":
            # XX
            return [9]
        elif pol_type == "V":
            # YY
            return [12]
        elif pol_type == "R":
            # RR
            return [5]
        elif pol_type == "L":
            # LL
            return [8]
        else:
            AssertionError("polarization string must be any of 'H', 'V', 'R', 'L'")
    elif len(pols) == 2:
        enum_list = []
        for v in pols:
            match v[-1]:
                case "H":
                    enum_list.append(9)
                case "V":
                    enum_list.append(12)
                case "R":
                    enum_list.append(5)
                case "L":
                    enum_list.append(8)
                case _:
                    AssertionError("polarization string must be any of 'H', 'V', 'R', 'L'")
        return enum_list
    else:
        AssertionError("number of polarization must be either 1 or 2")


def _get_polarization_row(hdu: BinTableHDU) -> Generator[dict, None, None]:
    """Provide polarization row information.

    Args:
        hdu: NRO45m psw data in the form of BinTableHDU object.

    Yields:
        Dictionary containing polarization row information.

    Raises:
        AssertionError: If number of polarization is not either 1 or 2.
    """
    array_conf = get_array_configuration(hdu)
    _, _, _, pol_map = get_data_description_map(array_conf)
    # num_pol = len(pol_map)

    # CORR_TYPE
    corr_type = np.array(pol_str_to_enum(pol_map[0]))

    # CORR_PRODUCT
    corr_product = None
    v = pol_map[0]
    if len(v) == 1:
        corr_product = np.array([[0], [0]])
    elif len(v) == 2:
        corr_product = np.array([[1, 0], [0, 1]])
    else:
        AssertionError("number of polarization must be either 1 or 2")

    # NUM_CORR
    num_corr = len(pol_map[0])

    # FLAG_ROW
    flag_row = False

    row = {
        "CORR_TYPE": corr_type,
        "CORR_PRODUCT": corr_product,
        "NUM_CORR": num_corr,
        "FLAG_ROW": flag_row
    }

    yield row


def fill_polarization(msfile: str, hdu: BinTableHDU):
    """Fill MS POLARIZATION table.

    Args:
        msfile: Name of MS file.
        hdu: NRO45m psw data in the form of BinTableHDU object.
    """
    fill_ms_table(msfile, hdu, "POLARIZATION", _get_polarization_row)
    # with open_table(msfile + "/POLARIZATION", read_only=False) as tb:
    #     num_pol = len(columns["NUM_CORR"])
    #     fix_nrow_to(num_pol, tb)

    #     tb.putcol("NUM_CORR", columns["NUM_CORR"])
    #     tb.putcol("FLAG_ROW", columns["FLAG_ROW"])
    #     for i in range(num_pol):
    #         tb.putcell("CORR_TYPE", i, columns["CORR_TYPE"][i])
    #         tb.putcell("CORR_PRODUCT", i, columns["CORR_PRODUCT"][i])
