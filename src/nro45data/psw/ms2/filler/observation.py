import logging
from typing import TYPE_CHECKING

import numpy as np

from .._casa import open_table, datestr2mjd
from .utils import fix_nrow_to

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_observation_columns(hdu: "BinTableHDU") -> dict:
    history_cards = hdu.header["HISTORY"]

    # TELESCOPE_NAME
    telescope_name = hdu.header["TELESCOP"].strip()
    LOG.debug("telescope_name: %s", telescope_name)

    # TIME_RANGE
    # NOTE: sstr and estr are in JST
    start_time_card = [x for x in history_cards if x.startswith("NEWSTAR START-TIME")]
    sstr = start_time_card[0].split("=")[-1].strip(" '")
    datestr = sstr[0:4] + "/" + sstr[4:6] + "/" + sstr[6:8] + " " + sstr[8:10] + ":" + sstr[10:12] + ":" + sstr[12:14]
    start_time = datestr2mjd(datestr) - 9 * 3600
    end_time_card = [x for x in history_cards if x.startswith("NEWSTAR END-TIME")]
    estr = end_time_card[0].split("=")[-1].strip(" '")
    datestr = estr[0:4] + "/" + estr[4:6] + "/" + estr[6:8] + " " + estr[8:10] + ":" + estr[10:12] + ":" + estr[12:14]
    end_time = datestr2mjd(datestr) - 9 * 3600
    time_range = np.array([start_time, end_time])
    LOG.debug("time_range: %s", time_range)

    # OBSERVER
    observer = hdu.header["OBSERVER"].strip()
    LOG.debug("observer: %s", observer)

    # LOG
    observing_log = [""]

    # SCHEDULE_TYPE
    schedule_card = [x for x in history_cards if x.startswith("NEWSTAR SCHED")]
    _schedule_type = schedule_card[0].split("=")[-1].strip(" '")
    schedule_type = f"{telescope_name} {_schedule_type}"
    LOG.debug("schedule_type: %s", schedule_type)

    # SCHEDULE
    group_card = [x for x in history_cards if x.startswith("NEWSTAR GROUP")]
    _group = group_card[0].split("=")[-1].strip(" '")
    title1_card = [x for x in history_cards if x.startswith("NEWSTAR TITLE1")]
    _title1 = title1_card[0].split("=")[-1].strip(" '")
    title2_card = [x for x in history_cards if x.startswith("NEWSTAR TITLE2")]
    _title2 = title2_card[0].split("=")[-1].strip(" '")
    schedule = [f"{telescope_name} {_group}"]
    if _title1:
        schedule.append(_title1)
    if _title2:
        schedule.append(_title2)
    LOG.debug("schedule: %s", schedule)

    # PROJECT
    project_card = [x for x in history_cards if x.startswith("NEWSTAR PROJECT")]
    project = project_card[0].split("=")[-1].strip(" '")
    LOG.debug("project: %s", project)

    # RELEASE_DATE
    release_date = 0

    # FLAG_ROW
    flag_row = False

    columns = {
        "TELESCOPE_NAME": telescope_name,
        "TIME_RANGE": time_range,
        "OBSERVER": observer,
        "LOG": observing_log,
        "SCHEDULE_TYPE": schedule_type,
        "SCHEDULE": schedule,
        "PROJECT": project,
        "RELEASE_DATE": release_date,
        "FLAG_ROW": flag_row,
    }

    return columns


def _fill_observation_columns(msfile: str, columns: dict):
    with open_table(msfile + "/OBSERVATION", read_only=False) as tb:
        fix_nrow_to(1, tb)

        tb.putcell("TELESCOPE_NAME", 0, columns["TELESCOPE_NAME"])
        tb.putcell("TIME_RANGE", 0, columns["TIME_RANGE"])
        tb.putcell("OBSERVER", 0, columns["OBSERVER"])
        tb.putcell("LOG", 0, columns["LOG"])
        tb.putcell("SCHEDULE_TYPE", 0, columns["SCHEDULE_TYPE"])
        tb.putcell("SCHEDULE", 0, columns["SCHEDULE"])
        tb.putcell("PROJECT", 0, columns["PROJECT"])
        tb.putcell("RELEASE_DATE", 0, columns["RELEASE_DATE"])
        tb.putcell("FLAG_ROW", 0, columns["FLAG_ROW"])
