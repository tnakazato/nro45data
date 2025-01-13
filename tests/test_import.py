import pytest

from nro45data import psw


def test_psw():
    assert psw is not None
    assert psw.nqm2fits is not None
    assert psw.nqm2ms2 is not None
    assert psw.nqm2ms4 is not None


def test_nqm2fits():
    assert psw.nqm2fits.__name__ == "nqm2fits"
    assert psw.nqm2fits.__module__ == "nro45data.psw"
    assert psw.nqm2fits.__doc__ is not None
    assert psw.nqm2fits.__annotations__ == {"nqmfile": str, "fitsfile": str, "overwrite": bool, "return": bool}
    assert psw.nqm2fits.__module__ == "nro45data.psw"
    assert psw.nqm2fits.__module__ == "nro45data.psw"
    assert psw.nqm2fits.__module__ == "nro45data.psw"
    assert psw.nqm2fits.__module__ == "nro45data.psw"
    assert psw.nqm2fits.__module__ == "nro45data.psw"


def test_nqm2ms2():
    assert psw.nqm2ms2.__name__ == "nqm2ms2"
    assert psw.nqm2ms2.__module__ == "nro45data.psw"
    assert psw.nqm2ms2.__doc__ is not None
    assert psw.nqm2ms2.__annotations__ == {"nqmfile": str, "msfile": str, "overwrite": bool, "return": bool}
    assert psw.nqm2ms2.__module__ == "nro45data.psw"
    assert psw.nqm2ms2.__module__ == "nro45data.psw"
    assert psw.nqm2ms2.__module__ == "nro45data.psw"
    assert psw.nqm2ms2.__module__ == "nro45data.psw"
    assert psw.nqm2ms2.__module__ == "nro45data.psw"


def test_nqm2ms4():
    assert psw.nqm2ms4.__name__ == "nqm2ms4"
    assert psw.nqm2ms4.__module__ == "nro45data.psw"
    assert psw.nqm2ms4.__doc__ is not None
    assert psw.nqm2ms4.__annotations__ == {"nqmfile": str, "psfile": str, "overwrite": bool, "return": bool}
    assert psw.nqm2ms4.__module__ == "nro45data.psw"
    assert psw.nqm2ms4.__module__ == "nro45data.psw"
    assert psw.nqm2ms4.__module__ == "nro45data.psw"
    assert psw.nqm2ms4.__module__ == "nro45data.psw"
    assert psw.nqm2ms4.__module__ == "nro45data.psw"
