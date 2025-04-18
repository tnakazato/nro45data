import collections
import os
import re
from typing import List, Tuple

from astropy.io.fits.hdu.hdulist import HDUList

FITS_BLOCK_SIZE = 2880
FITS_RECORD_SIZE = 80
FITS_NUM_RECORDS_PER_BLOCK = FITS_BLOCK_SIZE // FITS_RECORD_SIZE


def _is_nro_psw(filename: str) -> bool:
    """Test if given file is in NRO 45m PSW format.

    Args:
        filename: Name of the file

    Returns:
        True if the file is in NRO 45m PSW format, otherwise False.
    """
    expected = "XTENSION='BINTABLE'"
    with open(filename, "rb") as f:
        first_record = f.read(FITS_RECORD_SIZE).decode()

    return first_record.startswith(expected)


def _read_header_and_data(filename: str) -> Tuple[List[str], bytes]:
    """Read given file and return its header and data separately.

    Args:
        filename: Name of the file

    Returns:
        List of header records and binary data
    """
    with open(filename, "rb+") as f:
        # header
        header = []
        is_end_of_header = False
        num_records = 0
        while not is_end_of_header:
            block = f.read(FITS_BLOCK_SIZE)
            for i in range(FITS_NUM_RECORDS_PER_BLOCK):
                s = i * FITS_RECORD_SIZE
                e = s + FITS_RECORD_SIZE
                record_bytes = block[s:e]
                num_records += 1
                record = record_bytes.decode()
                header.append(record)
                is_end_of_header = record.strip() == "END"
                if is_end_of_header:
                    break

        # data
        f.seek(num_records * FITS_RECORD_SIZE, os.SEEK_SET)
        data = f.read()

    return header, data


def _follow_fits_standard(records: List[str]) -> List[str]:
    """Tweak header records to follow FITS standard.

    List of tweaks to be applied is as follows:

        - insert whitespace betweeen "=" and value

    Args:
        records: List of header records of FITS file

    Returns:
        List of tweaked header records
    """

    def __insert_space_before_value(record: str) -> str:
        if record.startswith("END"):
            return record

        fixed_record = re.sub("=", "= ", record, count=1)
        if " /" in fixed_record:
            fixed_record = fixed_record.replace(" /", "/")
        elif fixed_record.endswith(" "):
            fixed_record = fixed_record[:-1]
        return fixed_record

    return list(map(__insert_space_before_value, records))


def _rename_duplicate_types(records: List[str]) -> List[str]:
    """Make binary data keys unique by renaming duplicate keys.

    Args:
        records: List of header records

    Returns:
        List of tweaked header records
    """
    duplicate_rows = collections.defaultdict(list)
    for i, r in enumerate(records):
        if r.startswith("TTYPE"):
            k = re.match(r".*= '([^']+)'.*", r)[1]
            duplicate_rows[k].append(i)
    fixed_records = records[::]
    for k, rows in duplicate_rows.items():
        for row in rows[1:]:
            # print(f'key {k}, row {row}')
            new_key = k[:-1] + chr(ord(k[-1]) + 1)
            # print(f'new key: {new_key}')
            fixed_records[row] = fixed_records[row].replace(k, new_key)
            # print(fixed_records[row])

    return fixed_records


def _read_psw(filename: str) -> HDUList:
    """Read NRO 45m PSW data.

    Args:
        filename: Name of the data
        mode: Observation mode. Either 'psw' or 'otf'.
    """
    if not _is_nro_psw(filename):
        raise RuntimeError("Incompatible data: " f'"{filename}" is not in NRO 45m PSW format.')

    record_list, binary_data = _read_header_and_data(filename)

    record_list = _follow_fits_standard(record_list)

    # rename duplicate TTYPE names
    record_list = _rename_duplicate_types(record_list)
    # for r in record_list:
    #     print(r)

    header = "".join(record_list).encode()

    hdulist = HDUList.fromstring(header + binary_data, ignore_missing_simple=True, lazy_load_hdus=False)

    return hdulist
