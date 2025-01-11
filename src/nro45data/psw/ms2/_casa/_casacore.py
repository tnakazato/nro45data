import contextlib
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
        raise ModuleNotFoundError('python-casacore is not available')

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
    return angle_quantity.get('rad').get_value()



def put_table_keyword(table_name: str, keyword: str, value: Any):
    with open_table(table_name, read_only=False) as tb:
        tb.putkeyword(keyword, value)
