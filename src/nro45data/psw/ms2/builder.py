import logging
import os

from nro45data.psw.ms2.schema.antenna import MsAntennaTable
from nro45data.psw.ms2.schema.data_description import MsDataDescriptionTable
from nro45data.psw.ms2.schema.feed import MsFeedTable
from nro45data.psw.ms2.schema.field import MsFieldTable
from nro45data.psw.ms2.schema.flag_cmd import MsFlagCmdTable
from nro45data.psw.ms2.schema.history import MsHistoryTable
from nro45data.psw.ms2.schema.observation import MsObservationTable
from nro45data.psw.ms2.schema.pointing import MsPointingTable
from nro45data.psw.ms2.schema.polarization import MsPolarizationTable
from nro45data.psw.ms2.schema.processor import MsProcessorTable
from nro45data.psw.ms2.schema.source import MsSourceTable
from nro45data.psw.ms2.schema.spectral_window import MsSpectralWindowTable
from nro45data.psw.ms2.schema.state import MsStateTable
from nro45data.psw.ms2.schema.syscal import MsSyscalTable
from nro45data.psw.ms2.schema.weather import MsWeatherTable
from nro45data.psw.ms2.schema.main import MsMainTable

from ._table import build_table

LOG = logging.getLogger(__name__)


def build_ms2_subtable(msfile: str, subtable_name: str, table_desc: dict):
    assert os.path.exists(msfile), f'{msfile} MAIN table does not exist'
    subtable_path = os.path.join(msfile, subtable_name)
    build_table(subtable_path, table_desc)
    LOG.info('created %s', subtable_name)
    LOG.debug('subtable path is %s', subtable_path)


def build_ms2_main(msfile: str):
    table_desc = MsMainTable.as_dict()
    build_table(msfile, table_desc['coldesc'])
    LOG.info('created %s MAIN', msfile)


def build_ms2(msfile: str):
    LOG.info('Building MS')
    build_ms2_main(msfile)
    subtables = [
        ('ANTENNA', MsAntennaTable),
        ('DATA_DESCRIPTION', MsDataDescriptionTable),
        ('FEED', MsFeedTable),
        ('FIELD', MsFieldTable),
        ('FLAG_CMD', MsFlagCmdTable),
        ('HISTORY', MsHistoryTable),
        ('OBSERVATION', MsObservationTable),
        ('POINTING', MsPointingTable),
        ('POLARIZATION', MsPolarizationTable),
        ('PROCESSOR', MsProcessorTable),
        ('SOURCE', MsSourceTable),
        ('SPECTRAL_WINDOW', MsSpectralWindowTable),
        ('STATE', MsStateTable),
        ('SYSCAL', MsSyscalTable),
        ('WEATHER', MsWeatherTable)
    ]
    for subtable_name, table_schema in subtables:
        build_ms2_subtable(msfile, subtable_name, table_schema.as_dict()['coldesc'])
    LOG.info('created %s', msfile)
