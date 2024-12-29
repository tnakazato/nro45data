try:
    _is_casacore_available = True
    import casacore.tables as _table
except ImportError:
    _is_casacore_available = False
    _table = None


def build_table(table_name: str, table_desc: dict):
    if _table is None:
        raise ModuleNotFoundError('python-casacore is not available')

    tb = _table.table(table_name, table_desc)
    tb.close()
