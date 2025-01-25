import contextlib
import datetime
from typing import Any

try:
    _is_casacore_available = True
    import casacore.tables as _table
    import casacore.quanta as _quanta
except ImportError:
    _is_casacore_available = False
    _table = None
    _quanta = None


def _test_casacore():
    if not _is_casacore_available:
        raise ModuleNotFoundError("python-casacore is not available")


def build_table(table_name: str, table_desc: dict):
    _test_casacore()

    tb = _table.table(table_name, table_desc)
    tb.close()


@contextlib.contextmanager
def open_table(table_name: str, read_only=True) -> _table:
    _test_casacore()

    try:
        tb = _table.table(table_name, readonly=read_only)
        yield tb
    finally:
        tb.close()


def convert_str_angle_to_rad(angle_str: str) -> float:
    _test_casacore()

    angle_quantity = _quanta.quantity(angle_str)
    return angle_quantity.get("rad").get_value()


def put_table_keyword(table_name: str, keyword: str, value: Any):
    with open_table(table_name, read_only=False) as tb:
        tb.putkeyword(keyword, value)

def datestr2mjd(date_str: str) -> float:
    """Convert datetime string into MJD in sec.

    Args:
        date_str: datetime string YYYY/MM/DD HH:MM:SS

    Returns:
        MJD in sec
    """
    q = _quanta.quantity(date_str)
    return q.get("s").get_value()


def mjd2datetime(mjd: float) -> datetime.datetime:
    """Convert MJD time in sec to datetime object.

    Args:
        mjd: MJD time in sec

    Returns:
        datetime object
    """
    qa = _quanta
    qtime = qa.quantity(mjd, "s")
    dtobj = datetime.datetime.fromtimestamp(qtime.to_unix_time(), datetime.UTC)

    return dtobj
