import logging
from typing import TYPE_CHECKING

import numpy as np

from ._table import open_table

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def fill_observation(msfile: str, hdu: 'BinTableHDU'):
    history_cards = hdu.header['HISTORY']

    #TELESCOPE_NAME
    telescope_name = hdu.header['TELESCOP'].strip()
    LOG.debug('telescope_name: %s', telescope_name)

    # TIME_RANGE
    start_time_card = [x for x in history_cards if x.startswith('NEWSTAR START-TIME')]
    start_time = float(start_time_card[0].split('=')[-1].strip(" '"))
    end_time_card = [x for x in history_cards if x.startswith('NEWSTAR END-TIME')]
    end_time = float(end_time_card[0].split('=')[-1].strip(" '"))
    time_range = np.array([start_time, end_time])
    LOG.debug('time_range: %s', time_range)

    # OBSERVER
    observer = hdu.header['OBSERVER'].strip()
    LOG.debug('observer: %s', observer)

    # LOG
    observing_log = ['']

    # SCHEDULE_TYPE
    schedule_card = [x for x in history_cards if x.startswith('NEWSTAR SCHED')]
    _schedule_type = schedule_card[0].split('=')[-1].strip(" '")
    schedule_type = f'{telescope_name} {_schedule_type}'
    LOG.debug('schedule_type: %s', schedule_type)

    # SCHEDULE
    group_card = [x for x in history_cards if x.startswith('NEWSTAR GROUP')]
    _group = group_card[0].split('=')[-1].strip(" '")
    title1_card = [x for x in history_cards if x.startswith('NEWSTAR TITLE1')]
    _title1 = title1_card[0].split('=')[-1].strip(" '")
    title2_card = [x for x in history_cards if x.startswith('NEWSTAR TITLE2')]
    _title2 = title2_card[0].split('=')[-1].strip(" '")
    schedule = [f'{telescope_name} {_group}']
    if _title1:
        schedule.append(_title1)
    if _title2:
        schedule.append(_title2)
    LOG.debug('schedule: %s', schedule)

    # PROJECT
    project_card = [x for x in history_cards if x.startswith('NEWSTAR PROJECT')]
    project = project_card[0].split('=')[-1].strip(" '")
    LOG.debug('project: %s', project)

    # RELEASE_DATE
    release_date = 0

    # FLAG_ROW
    flag_row = False

    with open_table(msfile + '/OBSERVATION', read_only=False) as tb:
        nrows = tb.nrows()
        if nrows < 1:
            tb.addrows()
        elif nrows > 1:
            tb.removerows(np.arange(1, nrows))
        tb.putcell('TELESCOPE_NAME', 0, telescope_name)
        tb.putcell('TIME_RANGE', 0, time_range)
        tb.putcell('OBSERVER', 0, observer)
        tb.putcell('LOG', 0, observing_log)
        tb.putcell('SCHEDULE_TYPE', 0, schedule_type)
        tb.putcell('SCHEDULE', 0, schedule)
        tb.putcell('PROJECT', 0, project)
        tb.putcell('RELEASE_DATE', 0, release_date)
        tb.putcell('FLAG_ROW', 0, flag_row)
