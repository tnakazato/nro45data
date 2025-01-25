import contextlib
from typing import Any

try:
    _is_casa6_available = True
    import casatools.table as _table
    import casatools.quanta as _quanta_cls

    _quanta = _quanta_cls()
except ImportError:
    _is_casa6_available = False
    _table = None
    _quanta = None


def _test_casatools():
    if not _is_casa6_available:
        raise ModuleNotFoundError("casatools is not available")


def build_table(table_name: str, table_desc: dict):
    _test_casatools()

    tb = _table()
    tb.create(table_name, table_desc)
    tb.close()


@contextlib.contextmanager
def open_table(table_name: str, read_only=True) -> _table:
    _test_casatools()

    tb = _table()
    try:
        tb.open(table_name, nomodify=read_only)
        yield tb
    finally:
        tb.close()


def convert_str_angle_to_rad(angle_str: str) -> float:
    _test_casatools()

    qa = _quanta
    return qa.convert(qa.quantity(angle_str), "rad")["value"]


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
    return _quanta.convert(q, "s")["value"]
