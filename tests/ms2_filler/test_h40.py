import datetime
import os
import shutil
import time

import numpy as np
import pytest

try:
    from casatools import ms as _ms
except Exception:
    _ms = None

import nro45data.psw as psw
from nro45data.psw.ms2._casa import open_table, mjd2datetime


@pytest.fixture(scope="module")
def msfile(data_dir):
    # input nqm file
    nqmfile = "nmlh40.240926005833.01.nqm"

    # generate MS
    nqmpath = os.path.join(data_dir, nqmfile)
    msfile = ".".join([nqmpath, time.strftime("%Y%M%dT%H%M%S"), 'ms'])
    try:
        psw.nqm2ms2(nqmpath, msfile)
    except Exception as e:
        if os.path.exists(msfile):
            shutil.rmtree(msfile)
        raise e

    yield msfile

    # clean up
    print("cleaning up MS...")
    if os.path.exists(msfile):
        shutil.rmtree(msfile)


# TODO: implement more detailed tests
def test_ms2_structure_h40(msfile):
    print(f"msfile = {msfile}")
    assert os.path.exists(msfile)

    # number of records = 76
    # number of arrays = 4
    # number of spectral windows = 4
    # number of polarizations = 1
    # number of beams = 1

    with open_table(os.path.join(msfile, "STATE")) as tb:
        intents_map = dict((i, v) for i, v in enumerate(tb.getcol("OBS_MODE")))

    with open_table(os.path.join(msfile, "OBSERVATION")) as tb:
        assert tb.nrows() == 1
        time_range = tb.getcell("TIME_RANGE", 0)
        # start time: 2024/09/26 00:58:54
        # end time: 2024/09/26 01:03:50
        start_expected = datetime.datetime(2024, 9, 26, 0, 58, 54)
        start_time = mjd2datetime(time_range[0])
        assert start_time == start_expected

        end_expected = datetime.datetime(2024, 9, 26, 1, 3, 50)
        end_time = mjd2datetime(time_range[1])
        assert end_time == end_expected

    with open_table(os.path.join(msfile, "SPECTRAL_WINDOW")) as tb:
        assert tb.nrows() == 4
        nchan_map = dict((i, v) for i, v in enumerate(tb.getcol("NUM_CHAN")))

    # test polarization setup
    with open_table(os.path.join(msfile, "POLARIZATION")) as tb:
        assert tb.nrows() == 1
        npol = tb.getcell("NUM_CORR", 0)
        corr_type = tb.getcell("CORR_TYPE", 0)
        assert npol == 1
        assert len(corr_type) == npol
        assert corr_type[0] == 8

    # test number of rows in MS MAIN
    with open_table(msfile) as tb:
        # number of MS2 rows = 76
        nrows = tb.nrows()
        assert nrows == 76

        # scans = 0~18
        scans = tb.getcol("SCAN_NUMBER")
        # expected scans are [0, 0, 0, 0, 1, 1, ..., 18, 18, 18, 18]
        num_arrays = 4
        num_scans_expected = 19
        scans_expected = np.concatenate([[i] * num_arrays for i in range(num_scans_expected)])
        assert np.all(scans == scans_expected)

        # intents = ZERO if scan number is 0
        #           ON otherwise
        state_ids = tb.getcol("STATE_ID")
        zero_scans = np.where(scans == 0)
        zero_intents = set(intents_map[i] for i in state_ids[zero_scans])
        assert len(zero_intents) == 1
        assert "ZERO" in zero_intents.pop()

        nonzero_scans = np.where(scans != 0)
        nonzero_intents = set(intents_map[i] for i in state_ids[nonzero_scans])
        assert len(nonzero_intents) == 1
        assert "OBSERVE_TARGET#ON_SOURCE" in nonzero_intents.pop()

        # start time: 2024/9/26 0:59:19, integration time 1sec
        start_expected = datetime.datetime(2024, 9, 26, 0, 59, 19, 500000)
        start_time = mjd2datetime(tb.getcell("TIME", 0))
        assert start_time == start_expected

        # end time: 2024/9/26 1:3:50, integration time 5sec
        end_expected = datetime.datetime(2024, 9, 26, 1, 3, 47, 500000)
        end_time = mjd2datetime(tb.getcell("TIME", nrows - 1))
        assert end_time == end_expected

        # data cell shape
        for irow in range(nrows):
            float_data = tb.getcell("FLOAT_DATA", irow)
            dd_id = tb.getcell("DATA_DESC_ID", irow)
            spw_id = dd_id
            nchan = nchan_map[spw_id]
            shape_expected = (npol, nchan)
            assert float_data.shape == shape_expected


@pytest.mark.skipif(_ms is None, reason="casatools is not available")
def test_listobs(msfile):
    ms = _ms()
    ms.open(msfile)
    try:
        summary = ms.summary()
    except Exception as e:
        pytest.fail(f"ms.summary was failed with the error: {e}")
    finally:
        ms.close()

    assert isinstance(summary, dict)
