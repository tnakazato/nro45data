import os

import nro45data.psw.ms2.schema.antenna as antenna

from ._casa6 import _is_casa6_available
from ._casacore import _is_casacore_available

if _is_casa6_available:
    from ._casa6 import build_table
elif _is_casacore_available:
    from ._casacore import build_table
else:
    raise ModuleNotFoundError('Neither casatools or python-casacore is available')


def build_ms2_antenna(msfile: str):
    table_desc = antenna.AntennaTable.as_dict()
    if not os.path.exists(msfile):
        os.makedirs(msfile)
    antenna_subtable_name = os.path.join(msfile, 'ANTENNA')
    build_table(antenna_subtable_name, table_desc['coldesc'])
    print('created {antenna_subtable_name}')


def build_ms2_main(msfile: str):
    pass


def build_ms2(msfile: str):
    build_ms2_antenna(msfile)
    build_ms2_main(msfile)
    print('created {msfile}')
