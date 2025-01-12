from ._casa6 import _is_casa6_available
from ._casacore import _is_casacore_available

if _is_casa6_available:
    from ._casa6 import build_table
    from ._casa6 import open_table
    from ._casa6 import _table
    from ._casa6 import convert_str_angle_to_rad
    from ._casa6 import put_table_keyword
elif _is_casacore_available:
    from ._casacore import build_table
    from ._casacore import open_table
    from ._casacore import _table
    from ._casacore import convert_str_angle_to_rad
    from ._casacore import put_table_keyword
else:
    raise ModuleNotFoundError('Neither casatools or python-casacore is available')

__all__ = [
    "build_table",
    "open_table",
    "_table",
    "convert_str_angle_to_rad",
    "put_table_keyword"
]
