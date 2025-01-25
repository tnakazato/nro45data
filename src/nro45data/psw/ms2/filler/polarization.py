import logging
from typing import TYPE_CHECKING

import numpy as np

from .._casa import open_table
from .utils import fix_nrow_to, get_array_configuration, get_data_description_map

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def pol_str_to_enum(pols: list[str]) -> int:
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


def _get_polarization_columns(hdu: "BinTableHDU") -> dict:
    array_conf = get_array_configuration(hdu)
    _, _, _, pol_map = get_data_description_map(array_conf)
    num_pol = len(pol_map)

    # CORR_TYPE
    corr_type = [np.array(pol_str_to_enum(pol_map[ipol])) for ipol in range(num_pol)]

    # CORR_PRODUCT
    corr_product = []
    for ipol in range(num_pol):
        v = pol_map[ipol]
        if len(v) == 1:
            corr_product.append(np.array([[0], [0]]))
        elif len(v) == 2:
            corr_product.append(np.array([[0, 1], [0, 1]]))
        else:
            AssertionError("number of polarization must be either 1 or 2")

    # NUM_CORR
    num_corr = np.array([len(pol_map[ipol]) for ipol in range(num_pol)])

    # FLAG_ROW
    flag_row = np.zeros(num_pol, dtype=bool)

    columns = {"CORR_TYPE": corr_type, "CORR_PRODUCT": corr_product, "NUM_CORR": num_corr, "FLAG_ROW": flag_row}

    return columns


def _fill_polarization_columns(msfile: str, columns: dict):
    with open_table(msfile + "/POLARIZATION", read_only=False) as tb:
        num_pol = len(columns["NUM_CORR"])
        fix_nrow_to(num_pol, tb)

        tb.putcol("NUM_CORR", columns["NUM_CORR"])
        tb.putcol("FLAG_ROW", columns["FLAG_ROW"])
        for i in range(num_pol):
            tb.putcell("CORR_TYPE", i, columns["CORR_TYPE"][i])
            tb.putcell("CORR_PRODUCT", i, columns["CORR_PRODUCT"][i])
