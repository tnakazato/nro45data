import os

import casacore.tables as tables

import nro45data.psw.ms2.schema.antenna as antenna


def create_ms2_antenna(msfile: str):
    table_desc = antenna.AntennaTable.as_dict()
    if not os.path.exists(msfile):
        os.makedirs(msfile)
    antenna_subtable_name = os.path.join(msfile, 'ANTENNA')
    tb = tables.table(antenna_subtable_name, tabledesc=table_desc['coldesc'])
    tb.close()
    print('created {antenna_subtable_name}')