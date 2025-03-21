import logging
from typing import TYPE_CHECKING, Generator

import numpy as np

from .._casa import open_table

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_pointing_row(hdu: "BinTableHDU") -> Generator[dict, None, None]:
    multn = hdu.data["MULTN"]
    arryt = hdu.data["ARRYT"]

    beam_id_list, array_index = np.unique(multn, return_index=True)
    array_id_list = arryt[array_index]

    epoch = hdu.header["EPOCH"]
    if epoch == 1950.0:
        direction_ref = "B1950"
    elif epoch == 2000.0:
        direction_ref = "J2000"
    else:
        LOG.warning("Unknown epoch %f. Fall back to ICRS.", epoch)
        direction_ref = "ICRS"

    mjdst = hdu.data["MJDST"]
    mjdet = hdu.data["MJDET"]
    ra = hdu.data["RA"]
    dec = hdu.data["DEC"]
    dra = hdu.data["DRA"]
    ddec = hdu.data["DDEC"]
    az = hdu.data["AZ"]
    el = hdu.data["EL"]

    for beam_id, array_id in zip(beam_id_list, array_id_list):
        rows = np.where(arryt == array_id)[0]
        for row in rows:
            antenna_id = int(beam_id)
            pointing_start_time = mjdst[row]
            pointing_end_time = mjdet[row]
            pointing_mid_time = (pointing_start_time + pointing_end_time) / 2
            pointing_interval = pointing_end_time - pointing_start_time

            name = ""

            num_poly = 0

            time_origin = pointing_mid_time

            direction = np.array([[ra[row], dec[row]]])
            target = direction
            encoder = np.array([az[row], el[row]])
            source_offset = np.array([[dra[row], ddec[row]]])
            tracking = True

            pointing_row = {
                "ANTENNA_ID": antenna_id,
                "TIME": pointing_mid_time,
                "INTERVAL": pointing_interval,
                "NAME": name,
                "NUM_POLY": num_poly,
                "TIME_ORIGIN": time_origin,
                "DIRECTION_REF": direction_ref,
                "DIRECTION": direction,
                "TARGET": target,
                "ENCODER": encoder,
                "SOURCE_OFFSET": source_offset,
                "TRACKING": tracking,
            }

            yield pointing_row


def fill_pointing(msfile: str, hdu: "BinTableHDU"):
    row_iterator = _get_pointing_row(hdu)
    with open_table(msfile + "/POINTING", read_only=False) as tb:
        for row_id, row in enumerate(row_iterator):
            if tb.nrows() <= row_id:
                tb.addrows(tb.nrows() - row_id + 1)

            for key, value in row.items():
                LOG.info("row %d, key %s", row_id, key)
                if key == "DIRECTION_REF":
                    for col in ("DIRECTION", "TARGET", "SOURCE_OFFSET"):
                        colkeywords = tb.getcolkeywords(col)
                        if colkeywords["MEASINFO"]["Ref"] != value:
                            colkeywords["MEASINFO"]["Ref"] = value
                            tb.putcolkeywords(col, colkeywords)
                else:
                    tb.putcell(key, row_id, value)
            LOG.debug("spw %d row %s", row_id, row)
