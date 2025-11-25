import logging

from ._casa6 import _is_casa6_available
from ._casacore import _is_casacore_available

if _is_casa6_available:
    from ._casa6 import build_table
    from ._casa6 import open_table
    from ._casa6 import _table
    from ._casa6 import convert_str_angle_to_rad
    from ._casa6 import put_table_keyword
    from ._casa6 import datestr2mjd
    from ._casa6 import mjd2datetime
elif _is_casacore_available:
    from ._casacore import build_table
    from ._casacore import open_table
    from ._casacore import _table
    from ._casacore import convert_str_angle_to_rad
    from ._casacore import put_table_keyword
    from ._casacore import datestr2mjd
    from ._casacore import mjd2datetime
else:
    build_table = None
    open_table = None
    _table = None
    convert_str_angle_to_rad = None
    put_table_keyword = None
    datestr2mjd = None
    mjd2datetime = None

__all__ = [
    "build_table",
    "open_table",
    "_table",
    "convert_str_angle_to_rad",
    "put_table_keyword",
    "datestr2mjd",
    "mjd2datetime"
]


LOG = logging.getLogger(__name__)

if build_table is None:
    LOG.warning("Neither casatools nor python-casacore is available. CASA-related functions are disabled.")