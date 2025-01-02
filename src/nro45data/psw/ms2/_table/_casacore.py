import contextlib

try:
    _is_casacore_available = True
    import casacore.tables as _table
except ImportError:
    _is_casacore_available = False
    _table = None


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
