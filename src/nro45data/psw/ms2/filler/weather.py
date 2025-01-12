import logging
from typing import TYPE_CHECKING, Generator

import numpy as np

from .._casa import open_table

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_weather_row(hdu: 'BinTableHDU') -> Generator[dict, None, None]:
    # multn = hdu.data['MULTN']
    mjdst = hdu.data['MJDST']
    mjdet = hdu.data['MJDET']
    temp = hdu.data['TEMP']
    patm = hdu.data['PATM']
    vwind = hdu.data['VWIND']
    dwind = hdu.data['DWIND']

    temp_unit = hdu.header['TUNIT56']
    if temp_unit == 'C':
        temp += 273.16

    unique_beams = np.unique(mjdst)

    for beam in unique_beams:
        beam_indices = np.where(mjdst == beam)[0]
        _, _indices = np.unique(mjdst[beam_indices], return_index=True)
        time_indices = beam_indices[_indices]
        for i in time_indices:
            antenna_id = int(beam)
            weather_start_time = mjdst[i]
            weather_end_time = mjdet[i]
            weather_mid_time = (weather_start_time + weather_end_time) / 2
            weather_interval = weather_end_time - weather_start_time

            temperature = temp[i]

            pressure = patm[i]

            wind_speed = vwind[i]
            wind_direction = dwind[i]

            row = {
                'ANTENNA_ID': antenna_id,
                'TIME': weather_mid_time,
                'INTERVAL': weather_interval,
                'TEMPERATURE': temperature,
                'TEMPERATURE_FLAG': False,
                'PRESSURE': pressure,
                'PRESSURE_FLAG': False,
                'REL_HUMIDITY': 0.0,
                'REL_HUMIDITY_FLAG': False,
                'WIND_SPEED': wind_speed,
                'WIND_SPEED_FLAG': False,
                'WIND_DIRECTION': wind_direction,
                'WIND_DIRECTION_FLAG': False
            }

            yield row


def fill_weather(msfile: str, hdu: 'BinTableHDU'):
    row_iterator = _get_weather_row(hdu)
    with open_table(msfile + '/WEATHER', read_only=False) as tb:
        for row_id, row in enumerate(row_iterator):
            if tb.nrows() <= row_id:
                tb.addrows(tb.nrows() - row_id + 1)

            for key, value in row.items():
                tb.putcell(key, row_id, value)
            LOG.debug('weather table %d row %s', row_id, row)
