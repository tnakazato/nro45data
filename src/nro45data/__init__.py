from __future__ import annotations

from . import psw

__version__ = "1.2.1"
__all__ = ["nqm2fits", "nqm2ms2"]


def nqm2fits(nqmfile: str, fitsfile: str, overwrite: bool = False) -> bool:
    return psw.nqm2fits(nqmfile, fitsfile, overwrite)


nqm2fits.__doc__ = psw.nqm2fits.__doc__


def nqm2ms2(nqmfile: str, msfile: str, overwrite: bool = False) -> bool:
    return psw.nqm2ms2(nqmfile, msfile, overwrite)


nqm2ms2.__doc__ = psw.nqm2ms2.__doc__
