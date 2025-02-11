import datetime
import itertools
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
    nqmfile = "nmlfr.241001024858.01.nqm"

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

def test_forest_ms2_structure(msfile):
    print(f"msfile = {msfile}")
    assert os.path.exists(msfile)

    num_records = 496
    num_arrays = 16
    num_spws = 2
    num_pols = 2
    num_beams = 4

    with open_table(os.path.join(msfile, "ANTENNA")) as tb:
        assert tb.nrows() == num_beams
        for i in range(num_beams):
            assert tb.getcell("NAME", i) == f"NRO45M-BEAM{i}"
            assert tb.getcell("DISH_DIAMETER", i) == 45.0
            assert tb.getcell("TYPE", i) == "GROUND-BASED"
            assert tb.getcell("MOUNT", i) == "ALT-AZ"
            assert tb.getcell("STATION", i) == "NRO45M"
            offset = tb.getcell("OFFSET", i)
            assert offset.shape == (3,)
            assert np.all(offset == 0.0)
            position = tb.getcell("POSITION", i)
            assert position.shape == (3,)
            assert np.allclose(position, np.array([-3871023.46, 3428106.87, 3724039.47]))
            assert tb.getcell("FLAG_ROW", i) is False

    with open_table(os.path.join(msfile, "DATA_DESCRIPTION")) as tb:
        assert tb.nrows() == num_spws
        for i in range(num_spws):
            assert tb.getcell("SPECTRAL_WINDOW_ID", i) == i
            assert tb.getcell("POLARIZATION_ID", i) == 0
            assert tb.getcell("FLAG_ROW", i) is False

    with open_table(os.path.join(msfile, "FEED")) as tb:
        assert tb.nrows() == num_beams
        # start time: 2024/09/30 17:49:19
        # end time: 2024/09/30 17:57:32
        # ---> mid-time 2024/09/30 17:53:25.5
        #      interval 8min 13sec = 493sec
        time_expected = datetime.datetime(2024, 9, 30, 17, 53, 25, 500000, tzinfo=datetime.timezone.utc)
        interval_expected = 493.0  # sec
        for i in range(num_beams):
            assert tb.getcell("ANTENNA_ID", i) == i
            assert tb.getcell("FEED_ID", i) == 0
            assert tb.getcell("SPECTRAL_WINDOW_ID", i) == -1
            assert tb.getcell("NUM_RECEPTORS", i) == 2
            assert tb.getcell("BEAM_ID", i) == 0
            feed_time = mjd2datetime(tb.getcell("TIME", i))
            assert abs((feed_time - time_expected).total_seconds()) < 1e-3
            assert tb.getcell("INTERVAL", i) == interval_expected
            beam_offset = np.array(tb.getcell("BEAM_OFFSET", i))
            assert beam_offset.shape == (2, 2)
            assert np.all(beam_offset == 0.0)
            pol_type = np.array(tb.getcell("POLARIZATION_TYPE", i))
            assert pol_type.shape == (2,)
            assert pol_type[0] == "X"
            assert pol_type[1] == "Y"
            pol_response = np.array(tb.getcell("POL_RESPONSE", i))
            assert pol_response.shape == (2, 2)
            assert np.all(pol_response == 0.0)
            feed_position = np.array(tb.getcell("POSITION", i))
            assert feed_position.shape == (3,)
            assert np.all(feed_position == 0.0)
            receptor_angle = np.array(tb.getcell("RECEPTOR_ANGLE", i))
            assert receptor_angle.shape == (2,)
            assert np.all(receptor_angle == 0.0)

    with open_table(os.path.join(msfile, "FIELD")) as tb:
        assert tb.nrows() == 1
        assert tb.getcell("NAME", 0) == "NML-Tau"
        assert tb.getcell("CODE", 0) == ""
        # start time: 2024/09/30 17:49:19
        field_time = mjd2datetime(tb.getcell("TIME", 0))
        time_expected = datetime.datetime(2024, 9, 30, 17, 49, 19, tzinfo=datetime.timezone.utc)
        assert abs((field_time - time_expected).total_seconds()) < 1e-3
        assert tb.getcell("NUM_POLY", 0) == 0
        # RA  = 03:53:28.860
        # DEC = +11:24:22.40
        # Epoch = J2000
        ra_expected = 1.0187530477122202  # rad
        dec_expected = 2.9861419948788317  # rad
        for col in ["DELAY_DIR", "PHASE_DIR", "REFERENCE_DIR"]:
            meas_info = tb.getcolkeyword(col, "MEASINFO")
            assert "Ref" in meas_info
            assert meas_info["Ref"] == "J2000"
            direction = tb.getcell(col, 0)
            assert direction.shape == (1, 2)
            assert abs(direction[0, 0] - ra_expected) / ra_expected < 1e-6
            assert abs(direction[0, 1] - dec_expected) / dec_expected < 1e-6
        assert tb.getcell("SOURCE_ID", 0) == 0
        assert tb.getcell("FLAG_ROW", 0) is False

    with open_table(os.path.join(msfile, "SOURCE")) as tb:
        # start time: 2024/09/30 17:49:19
        # end time: 2024/09/30 17:57:32
        # ---> mid-time 2024/09/30 17:53:25.5
        #      interval 8min 13sec = 493sec
        time_expected = datetime.datetime(2024, 9, 30, 17, 53, 25, 500000, tzinfo=datetime.timezone.utc)
        interval_expected = 493.0  # sec
        assert tb.nrows() == 1
        source_time = mjd2datetime(tb.getcell("TIME", 0))
        assert abs((source_time - time_expected).total_seconds()) < 1e-3
        assert tb.getcell("INTERVAL", 0) == interval_expected
        assert tb.getcell("SPECTRAL_WINDOW_ID", 0) == -1
        assert tb.getcell("NUM_LINES", 0) == 0
        assert tb.getcell("NAME", 0) == "NML-Tau"
        assert tb.getcell("CALIBRATION_GROUP", 0) == 0
        assert tb.getcell("CODE", 0) == ""
        direction = tb.getcell("DIRECTION", 0)
        assert direction.shape == (2,)
        assert abs((direction[0] - ra_expected) / ra_expected) < 1e-6
        assert abs((direction[1] - dec_expected) / dec_expected) < 1e-6
        meas_info = tb.getcolkeyword("DIRECTION", "MEASINFO")
        assert "Ref" in meas_info
        assert meas_info["Ref"] == "J2000"
        position = tb.getcell("POSITION", 0)
        assert position.shape == (3,)
        assert np.all(position == 0)
        sysvel = tb.getcell("SYSVEL", 0)
        sysvel_expected = 3.4e4
        assert abs((sysvel - sysvel_expected) / sysvel_expected) < 1e-6
        meas_info = tb.getcolkeyword("SYSVEL", "MEASINFO")
        assert "Ref" in meas_info
        assert meas_info["Ref"] == "LSRK"

    with open_table(os.path.join(msfile, "STATE")) as tb:
        assert tb.nrows() == 2
        # first row is ZERO
        assert tb.getcell("OBS_MODE", 0) == "ZERO"
        assert tb.getcell("REF", 0) is True
        assert tb.getcell("SIG", 0) is False
        assert tb.getcell("SUB_SCAN", 0) == 0
        # second row is ON_SOURCE
        assert tb.getcell("OBS_MODE", 1) == "OBSERVE_TARGET#ON_SOURCE"
        assert tb.getcell("REF", 1) is False
        assert tb.getcell("SIG", 1) is True
        assert tb.getcell("SUB_SCAN", 1) == 1
        # cal and load values are 0
        assert np.all(tb.getcol("CAL") == 0)
        assert np.all(tb.getcol("LOAD") == 0)
        # all rows are valid
        assert np.all(np.logical_not(tb.getcol("FLAG_ROW")))
        intents_map = dict((i, v) for i, v in enumerate(tb.getcol("OBS_MODE")))

    with open_table(os.path.join(msfile, "OBSERVATION")) as tb:
        assert tb.nrows() == 1
        time_range = tb.getcell("TIME_RANGE", 0)
        # start time: 2024/09/30 17:49:19
        # end time: 2024/09/30 17:57:32
        start_expected = datetime.datetime(2024, 9, 30, 17, 49, 19, tzinfo=datetime.timezone.utc)
        start_time = mjd2datetime(time_range[0])
        # impose msec accuracy
        assert abs((start_time - start_expected).total_seconds()) < 1e-3

        end_expected = datetime.datetime(2024, 9, 30, 17, 57, 32, tzinfo=datetime.timezone.utc)
        end_time = mjd2datetime(time_range[1])
        # impose msec accuracy
        assert abs((end_time - end_expected).total_seconds()) < 1e-3
        assert tb.getcell("TELESCOPE_NAME", 0) == "NRO45M"
        assert tb.getcell("OBSERVER", 0) == "csv24"
        log = tb.getcell("LOG", 0)
        assert len(log) == 1
        assert log[0] == ""
        assert tb.getcell("SCHEDULE_TYPE", 0) == "NRO45M nmlfr"
        schedule = tb.getcell("SCHEDULE", 0)
        assert len(schedule) == 2
        assert schedule[0] == "NRO45M csv24"
        assert schedule[1] == "ffix                           z=1 3b= 0"
        assert tb.getcell("PROJECT", 0) == "squint"
        assert tb.getcell("RELEASE_DATE", 0) == 0
        assert tb.getcell("FLAG_ROW", 0) is False

    with open_table(os.path.join(msfile, "SPECTRAL_WINDOW")) as tb:
        assert tb.nrows() == num_spws
        # channel frequency of the first and the last channels
        fcal0 = (86274682430.2, 86212197569.8)  # Hz
        cf0 = tb.getcell("CHAN_FREQ", 0)
        assert np.allclose(cf0[0], fcal0[0])
        assert np.allclose(cf0[-1], fcal0[1])
        cf1 = tb.getcell("CHAN_FREQ", 1)
        assert np.allclose(cf1[0], fcal0[0])
        assert np.allclose(cf1[-1], fcal0[1])
        # channel width, effective_bw, resolution are all the same
        assert np.allclose(tb.getcol("CHAN_WIDTH"), -15258.818168496678)
        assert np.allclose(tb.getcol("EFFECTIVE_BW"), -15258.818168496678)
        assert np.allclose(tb.getcol("RESOLUTION"), -15258.818168496678)
        # spw name should contain array name
        assert tb.getcell("NAME", 0) == "_".join([f"A{i}" for i in range(1, 9)])
        assert tb.getcell("NAME", 1) == "_".join([f"A{i}" for i in range(9, 17)])
        # ref_frequency taken from F0CAL
        ref_freq0 = 86243440000
        assert tb.getcell("REF_FREQUENCY", 0) == ref_freq0
        assert tb.getcell("REF_FREQUENCY", 1) == ref_freq0
        # frequency frame is LSRK
        assert np.all(tb.getcol("MEAS_FREQ_REF") == 1)
        assert np.all(tb.getcol("NET_SIDEBAND") == -1)
        assert np.all(tb.getcol("IF_CONV_CHAIN") == 0)
        # all rows have the same number of channels
        assert np.all(tb.getcol("NUM_CHAN") == 4096)
        # total_bandwidth = chan_width * num_chan
        assert np.allclose(tb.getcol("TOTAL_BANDWIDTH"), 15258.818168496678 * 4096)
        # all rows are valid
        assert np.all(np.logical_not(tb.getcol("FLAG_ROW")))
        nchan_map = dict((i, v) for i, v in enumerate(tb.getcol("NUM_CHAN")))

    # test polarization setup
    with open_table(os.path.join(msfile, "POLARIZATION")) as tb:
        assert tb.nrows() == 1
        npol = tb.getcell("NUM_CORR", 0)
        corr_type = tb.getcell("CORR_TYPE", 0)
        assert npol == num_pols
        assert len(corr_type) == num_pols
        assert corr_type[0] == 9   # XX
        assert corr_type[1] == 12  # YY
        corr_product = tb.getcell("CORR_PRODUCT", 0)
        assert corr_product.shape == (2, num_pols)
        product_expected = np.array([[1, 0], [0, 1]])
        assert np.all(corr_product == product_expected)
        assert tb.getcell("FLAG_ROW", 0) is False

    with open_table(os.path.join(msfile, "PROCESSOR")) as tb:
        assert tb.nrows() == 1
        assert tb.getcell("TYPE", 0) == "SPECTROMETER"
        assert tb.getcell("SUB_TYPE", 0) == "AC45"
        assert tb.getcell("TYPE_ID", 0) == 0
        assert tb.getcell("MODE_ID", 0) == 0
        assert tb.getcell("FLAG_ROW", 0) is False

    with open_table(os.path.join(msfile, "WEATHER")) as tb:
        assert tb.nrows() == num_records // num_pols // num_spws
        antenna_id = tb.getcol("ANTENNA_ID")
        nrow_per_beam = tb.nrows() // num_beams
        assert np.all(antenna_id[0:nrow_per_beam] == 0)
        assert np.all(antenna_id[nrow_per_beam:2 * nrow_per_beam] == 1)
        assert np.all(antenna_id[2 * nrow_per_beam:3 * nrow_per_beam] == 2)
        assert np.all(antenna_id[3 * nrow_per_beam:] == 3)
        weather_time = tb.getcol("TIME")
        weather_time_expected = [
            datetime.datetime(2024, 9, 30, 17, 49, 53, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 50, 27, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 50, 36, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 50, 45, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 51, 12, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 51, 20, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 51, 30, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 51, 57, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 52, 6, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 52, 15, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 52, 41, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 52, 51, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 53, 1, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 53, 27, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 53, 36, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 53, 45, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 54, 11, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 54, 21, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 54, 29, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 54, 54, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 55, 3, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 55, 12, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 55, 38, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 55, 48, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 55, 58, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 56, 24, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 56, 33, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 56, 42, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 57, 9, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 57, 19, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 30, 17, 57, 29, 500000, tzinfo=datetime.timezone.utc)
        ]
        assert tb.nrows() == len(weather_time_expected) * num_beams
        for wt, dt_ex in zip(weather_time, itertools.cycle(weather_time_expected)):
            dt = mjd2datetime(wt)
            assert abs((dt - dt_ex).total_seconds()) < 1e-3
        weather_interval = tb.getcol("INTERVAL")
        assert np.allclose(weather_interval[0::nrow_per_beam], 1)
        assert np.allclose(weather_interval[1:nrow_per_beam], 5)
        assert np.allclose(weather_interval[nrow_per_beam + 1:2 * nrow_per_beam], 5)
        assert np.allclose(weather_interval[2 * nrow_per_beam + 1:3 * nrow_per_beam], 5)
        assert np.allclose(weather_interval[3 * nrow_per_beam + 1:], 5)
        temperature = tb.getcol("TEMPERATURE")
        assert np.allclose(temperature[:16], 11 + 273.16)
        assert np.allclose(temperature[16:31], 11.1 + 273.16)
        assert np.allclose(temperature[31:47], 11 + 273.16)
        assert np.allclose(temperature[47:62], 11.1 + 273.16)
        assert np.allclose(temperature[62:78], 11 + 273.16)
        assert np.allclose(temperature[78:93], 11.1 + 273.16)
        assert np.allclose(temperature[93:109], 11 + 273.16)
        assert np.allclose(temperature[109:], 11.1 + 273.16)
        assert np.all(np.logical_not(tb.getcol("TEMPERATURE_FLAG")))
        pressure = tb.getcol("PRESSURE")
        assert np.allclose(pressure, 866)
        assert np.all(np.logical_not(tb.getcol("PRESSURE_FLAG")))
        assert np.all(tb.getcol("REL_HUMIDITY") == 0)
        assert np.all(np.logical_not(tb.getcol("REL_HUMIDITY_FLAG")))
        wind_speed = tb.getcol("WIND_SPEED")
        assert np.allclose(wind_speed[:16], 0)
        assert np.allclose(wind_speed[16:20], 0.5)
        assert np.allclose(wind_speed[20:24], 0.8)
        assert np.allclose(wind_speed[24:28], 1)
        assert np.allclose(wind_speed[28:31], 0.9)
        assert np.allclose(wind_speed[31:47], 0)
        assert np.allclose(wind_speed[47:51], 0.5)
        assert np.allclose(wind_speed[51:55], 0.8)
        assert np.allclose(wind_speed[55:59], 1)
        assert np.allclose(wind_speed[59:62], 0.9)
        assert np.allclose(wind_speed[62:78], 0)
        assert np.allclose(wind_speed[78:82], 0.5)
        assert np.allclose(wind_speed[82:86], 0.8)
        assert np.allclose(wind_speed[86:90], 1)
        assert np.allclose(wind_speed[90:93], 0.9)
        assert np.allclose(wind_speed[93:109], 0)
        assert np.allclose(wind_speed[109:113], 0.5)
        assert np.allclose(wind_speed[113:117], 0.8)
        assert np.allclose(wind_speed[117:121], 1)
        assert np.allclose(wind_speed[121:], 0.9)
        assert np.all(np.logical_not(tb.getcol("WIND_SPEED_FLAG")))
        wind_direction = tb.getcol("WIND_DIRECTION")
        assert np.allclose(wind_direction[:1], 6.21337214)
        assert np.allclose(wind_direction[1:4], 6.19591884)
        assert np.allclose(wind_direction[4:16], 6.21337214)
        assert np.allclose(wind_direction[16:20], 1.6231562)
        assert np.allclose(wind_direction[20:24], 1.74532925)
        assert np.allclose(wind_direction[24:28], 2.18166156)
        assert np.allclose(wind_direction[28:31], 2.25147474)
        assert np.allclose(wind_direction[31:32], 6.21337214)
        assert np.allclose(wind_direction[32:35], 6.19591884)
        assert np.allclose(wind_direction[35:47], 6.21337214)
        assert np.allclose(wind_direction[47:51], 1.6231562)
        assert np.allclose(wind_direction[51:55], 1.74532925)
        assert np.allclose(wind_direction[55:59], 2.18166156)
        assert np.allclose(wind_direction[59:62], 2.25147474)
        assert np.allclose(wind_direction[62:63], 6.21337214)
        assert np.allclose(wind_direction[63:66], 6.19591884)
        assert np.allclose(wind_direction[66:78], 6.21337214)
        assert np.allclose(wind_direction[78:82], 1.6231562)
        assert np.allclose(wind_direction[82:86], 1.74532925)
        assert np.allclose(wind_direction[86:90], 2.18166156)
        assert np.allclose(wind_direction[90:93], 2.25147474)
        assert np.allclose(wind_direction[93:94], 6.21337214)
        assert np.allclose(wind_direction[94:97], 6.19591884)
        assert np.allclose(wind_direction[97:109], 6.21337214)
        assert np.allclose(wind_direction[109:113], 1.6231562)
        assert np.allclose(wind_direction[113:117], 1.74532925)
        assert np.allclose(wind_direction[117:121], 2.18166156)
        assert np.allclose(wind_direction[121:], 2.25147474)
        assert np.all(np.logical_not(tb.getcol("WIND_DIRECTION_FLAG")))

    # test number of rows in MS MAIN
    with open_table(msfile) as tb:
        # number of MS2 rows = 298
        nrows = tb.nrows()
        assert nrows == num_records // num_pols

        # scans = 0~30
        scans = tb.getcol("SCAN_NUMBER")
        nrows_per_scan = num_arrays // num_pols
        num_scans_expected = 31
        scans_expected = np.concatenate([[i] * nrows_per_scan for i in range(num_scans_expected)])
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

        # start time of first integration: 2024/9/30 17:49:53, integration time 1sec
        start_expected = datetime.datetime(2024, 9, 30, 17, 49, 53, 500000, tzinfo=datetime.timezone.utc)
        start_time = mjd2datetime(tb.getcell("TIME", 0))
        # impose msec accuracy
        assert abs((start_time - start_expected).total_seconds()) < 1e-3

        # start time of last integration: 2024/9/30 17:57:27, integration time 5sec
        end_expected = datetime.datetime(2024, 9, 30, 17, 57, 29, 500000, tzinfo=datetime.timezone.utc)
        end_time = mjd2datetime(tb.getcell("TIME", nrows - 1))
        # impose msec accuracy
        assert abs((end_time - end_expected).total_seconds()) < 1e-3

        # data cell shape
        for irow in range(nrows):
            float_data = tb.getcell("FLOAT_DATA", irow)
            dd_id = tb.getcell("DATA_DESC_ID", irow)
            spw_id = dd_id
            nchan = nchan_map[spw_id]
            shape_expected = (num_pols, nchan)
            assert float_data.shape == shape_expected


@pytest.mark.skipif(_ms is None, reason="casatools is not available")
def test_forest_ms2_summary(msfile):
    ms = _ms()
    ms.open(msfile)
    try:
        summary = ms.summary()
    except Exception as e:
        pytest.fail(f"ms.summary was failed with the error: {e}")
    finally:
        ms.close()

    assert isinstance(summary, dict)
