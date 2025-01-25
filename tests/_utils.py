import datetime
import os
import uuid

import nro45data.psw.ms2._casa as _casa


def _get_data_dir():
    tests_module_path = os.path.dirname(__file__)
    return os.path.join(tests_module_path, "data")

def _generate_random_name(suffix='ms'):
    gen_limit = 10
    for _ in range(gen_limit):
        prefix = uuid.uuid4().hex
        msfile = f"{prefix}.{suffix}"
        if not os.path.exists(msfile):
            return msfile
    else:
        raise RuntimeError("Failed to generate random name")


def mjd2datetime(mjd: float) -> datetime.datetime:
    """Convert MJD time in sec to datetime object.

    Args:
        mjd: MJD time in sec

    Returns:
        datetime object
    """
    if _casa._is_casa6_available:
        qa = _casa._casa6._quanta
        qtime = qa.quantity(mjd, "s")
        dtdict = qa.splitdate(qtime)
        dtobj = datetime.datetime(
            dtdict["year"],
            dtdict["month"],
            dtdict["monthday"],
            dtdict["hour"],
            dtdict["min"],
            dtdict["sec"],
            dtdict["usec"]
        )
    elif _casa._is_casacore_available:
        qa = _casa._casacore._quanta
        qtime = qa.quantity(mjd, "s")
        dtobj = datetime.datetime.fromtimestamp(qtime.to_unix_time())
    else:
        raise ModuleNotFoundError("Neither casatools or python-casacore is available")

    return dtobj
