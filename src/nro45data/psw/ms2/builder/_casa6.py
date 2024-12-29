try:
    _is_casa6_available = True
    import casatools.table as _table
except ImportError:
    _is_casa6_available = False
    _table = None


def build_table(table_name: str, table_desc: dict):
    if _table is None:
        raise ModuleNotFoundError('casatools is not available')

    tb = _table()
    tb.create(table_name, table_desc)
    tb.close()
