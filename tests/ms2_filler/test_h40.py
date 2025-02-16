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
def test_h40_ms2_structure(msfile):
    print(f"msfile = {msfile}")
    assert os.path.exists(msfile)

    num_records = 76
    num_arrays = 4
    num_spws = 4
    num_pols = 1
    num_beams = 1

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
        # start time: 2024/09/25 15:58:54
        # end time: 2024/09/25 16:03:50
        # ---> mid-time 2024/09/25 16:01:22
        #      interval 4min 56sec = 296sec
        time_expected = datetime.datetime(2024, 9, 25, 16, 1, 22, tzinfo=datetime.timezone.utc)
        interval_expected = 296.0  # sec
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
            assert pol_type[0] == "R"
            assert pol_type[1] == "L"
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
        # start time: 2024/09/25 15:58:54
        field_time = mjd2datetime(tb.getcell("TIME", 0))
        time_expected = datetime.datetime(2024, 9, 25, 15, 58, 54, tzinfo=datetime.timezone.utc)
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
            assert abs((direction[0, 0] - ra_expected) / ra_expected) < 1e-6
            assert abs((direction[0, 1] - dec_expected) / dec_expected) < 1e-6
        assert tb.getcell("SOURCE_ID", 0) == 0
        assert tb.getcell("FLAG_ROW", 0) is False

    with open_table(os.path.join(msfile, "SOURCE")) as tb:
        # start time: 2024/09/25 15:58:54
        # end time: 2024/09/25 16:03:50
        # ---> mid-time 2024/09/25 16:01:22
        #      interval 4min 56sec = 296sec
        time_expected = datetime.datetime(2024, 9, 25, 16, 1, 22, tzinfo=datetime.timezone.utc)
        interval_expected = 296.0  # sec
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
        # start time: 2024/09/25 15:58:54
        # end time: 2024/09/25 16:03:50
        start_expected = datetime.datetime(2024, 9, 25, 15, 58, 54, tzinfo=datetime.timezone.utc)
        start_time = mjd2datetime(time_range[0])
        # impose msec accuracy
        assert abs((start_time - start_expected).total_seconds()) < 1e-3

        end_expected = datetime.datetime(2024, 9, 25, 16, 3, 50, tzinfo=datetime.timezone.utc)
        end_time = mjd2datetime(time_range[1])
        # impose msec accuracy
        assert abs((end_time - end_expected).total_seconds()) < 1e-3
        assert tb.getcell("TELESCOPE_NAME", 0) == "NRO45M"
        assert tb.getcell("OBSERVER", 0) == "csv24"
        log = tb.getcell("LOG", 0)
        assert len(log) == 1
        assert log[0] == ""
        assert tb.getcell("SCHEDULE_TYPE", 0) == "NRO45M nmlh40"
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
        fcal0 = (43137620000.0, 43106380000.0)  # Hz
        fcal1 = (42836620000.0, 42805380000.0)  # Hz
        cf0 = tb.getcell("CHAN_FREQ", 0)
        assert np.allclose(cf0[0], fcal0[0])
        assert np.allclose(cf0[-1], fcal0[1])
        cf1 = tb.getcell("CHAN_FREQ", 1)
        assert np.allclose(cf1[0], fcal0[0])
        assert np.allclose(cf1[-1], fcal0[1])
        cf2 = tb.getcell("CHAN_FREQ", 2)
        assert np.allclose(cf2[0], fcal1[0])
        assert np.allclose(cf2[-1], fcal1[1])
        cf3 = tb.getcell("CHAN_FREQ", 3)
        assert np.allclose(cf3[0], fcal1[0])
        assert np.allclose(cf3[-1], fcal1[1])
        # channel width, effective_bw, resolution are all the same
        assert np.allclose(tb.getcol("CHAN_WIDTH"), -7628.815628815629)
        assert np.allclose(tb.getcol("EFFECTIVE_BW"), -7628.815628815629)
        assert np.allclose(tb.getcol("RESOLUTION"), -7628.815628815629)
        # spw name should contain array name
        assert tb.getcell("NAME", 0) == "A5"
        assert tb.getcell("NAME", 1) == "A6"
        assert tb.getcell("NAME", 2) == "A13"
        assert tb.getcell("NAME", 3) == "A14"
        # ref_frequency taken from F0CAL
        ref_freq0 = 43122000000
        ref_freq1 = 42821000000
        assert tb.getcell("REF_FREQUENCY", 0) == ref_freq0
        assert tb.getcell("REF_FREQUENCY", 1) == ref_freq0
        assert tb.getcell("REF_FREQUENCY", 2) == ref_freq1
        assert tb.getcell("REF_FREQUENCY", 3) == ref_freq1
        # frequency frame is LSRK
        assert np.all(tb.getcol("MEAS_FREQ_REF") == 1)
        assert np.all(tb.getcol("NET_SIDEBAND") == -1)
        assert np.all(tb.getcol("IF_CONV_CHAIN") == 0)
        # all rows have the same number of channels
        assert np.all(tb.getcol("NUM_CHAN") == 4096)
        # total_bandwidth = chan_width * num_chan
        assert np.allclose(tb.getcol("TOTAL_BANDWIDTH"), 7628.815628815629 * 4096)
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
        assert corr_type[0] == 8  # RR
        corr_product = tb.getcell("CORR_PRODUCT", 0)
        assert corr_product.shape == (2, num_pols)
        assert np.all(corr_product == 0)
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
        assert np.all(tb.getcol("ANTENNA_ID") == 0)
        weather_time = tb.getcol("TIME")
        weather_time_expected = [
            datetime.datetime(2024, 9, 25, 15, 59, 19, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 15, 59, 52, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 0, 2, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 0, 12, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 0, 36, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 0, 45, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 0, 54, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 1, 18, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 1, 28, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 1, 38, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 2, 3, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 2, 12, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 2, 21, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 2, 45, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 2, 55, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 3, 5, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 3, 29, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 3, 38, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 3, 47, 500000, tzinfo=datetime.timezone.utc)
        ]
        assert tb.nrows() == len(weather_time_expected)
        for wt, dt_ex in zip(weather_time, weather_time_expected):
            dt = mjd2datetime(wt)
            assert abs((dt - dt_ex).total_seconds()) < 1e-3
        weather_interval = tb.getcol("INTERVAL")
        assert np.allclose(weather_interval[:1], 1)
        assert np.allclose(weather_interval[1:], 5)
        temperature = tb.getcol("TEMPERATURE")
        assert np.allclose(temperature[:7], 13 + 273.16)
        assert np.allclose(temperature[7:], 12.9 + 273.16)
        assert np.all(np.logical_not(tb.getcol("TEMPERATURE_FLAG")))
        pressure = tb.getcol("PRESSURE")
        assert np.allclose(pressure, 868)
        assert np.all(np.logical_not(tb.getcol("PRESSURE_FLAG")))
        assert np.all(tb.getcol("REL_HUMIDITY") == 0)
        assert np.all(np.logical_not(tb.getcol("REL_HUMIDITY_FLAG")))
        wind_speed = tb.getcol("WIND_SPEED")
        assert np.allclose(wind_speed[:2], 1.3)
        assert np.allclose(wind_speed[2:7], 1.6)
        assert np.allclose(wind_speed[7:10], 0.4)
        assert np.allclose(wind_speed[10:], 1.3)
        assert np.all(np.logical_not(tb.getcol("WIND_SPEED_FLAG")))
        wind_direction = tb.getcol("WIND_DIRECTION")
        assert np.allclose(wind_direction[:2], 5.93411946)
        assert np.allclose(wind_direction[2:7], 6.19591884)
        assert np.allclose(wind_direction[7:10], 6.10865238)
        assert np.allclose(wind_direction[10:15], 0.10471976)
        assert np.allclose(wind_direction[15:], 0.05235988)
        assert np.all(np.logical_not(tb.getcol("WIND_DIRECTION_FLAG")))

    with open_table(os.path.join(msfile, "POINTING")) as tb:
        assert tb.nrows() == num_records // num_pols // num_spws
        assert np.all(tb.getcol("ANTENNA_ID") == 0)
        assert np.all(tb.getcol("NUM_POLY") == 0)
        assert np.all(np.array(tb.getcol("NAME")) == "")
        assert np.all(np.array(tb.getcol("TRACKING")))
        pointing_time = np.array(tb.getcol("TIME"))
        pointing_time_origin = np.array(tb.getcol("TIME_ORIGIN"))
        assert np.all(pointing_time_origin == pointing_time)
        pointing_time_expected = [
            datetime.datetime(2024, 9, 25, 15, 59, 19, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 15, 59, 52, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 0, 2, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 0, 12, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 0, 36, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 0, 45, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 0, 54, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 1, 18, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 1, 28, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 1, 38, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 2, 3, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 2, 12, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 2, 21, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 2, 45, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 2, 55, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 3, 5, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 3, 29, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 3, 38, 500000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2024, 9, 25, 16, 3, 47, 500000, tzinfo=datetime.timezone.utc)
        ]
        assert tb.nrows() == len(pointing_time_expected)
        for wt, dt_ex in zip(pointing_time, pointing_time_expected):
            dt = mjd2datetime(wt)
            assert abs((dt - dt_ex).total_seconds()) < 1e-3
        pointing_interval = tb.getcol("INTERVAL")
        assert np.allclose(pointing_interval[:1], 1)
        assert np.allclose(pointing_interval[1:], 5)
        assert np.allclose(tb.getcol("SOURCE_OFFSET"), 0)
        assert tb.getcolkeyword("DIRECTION", "MEASINFO")["Ref"] == "J2000"
        assert tb.getcolkeyword("TARGET", "MEASINFO")["Ref"] == "J2000"
        assert tb.getcolkeyword("SOURCE_OFFSET", "MEASINFO")["Ref"] == "J2000"
        assert tb.getcolkeyword("ENCODER", "MEASINFO")["Ref"] == "AZELGEO"
        ra_expected = 1.01875305
        dec_expected = 0.19907613
        az_expected = [
            2.06807743, 2.06954179, 2.07015452, 2.0707679 , 2.07275534,
            2.07344539, 2.07413612, 2.07613253, 2.0767516 , 2.07737131,
            2.0794541 , 2.0801507 , 2.08084798, 2.08286274, 2.08348832,
            2.08411455, 2.08613848, 2.08684166, 2.08754553
        ]
        el_expected = [
            0.86827902, 0.87009498, 0.87061334, 0.87113149, 0.87247113,
            0.87283984, 0.87320837, 0.8745458 , 0.87506229, 0.87557856,
            0.87696523, 0.87733221, 0.87769901, 0.87903182, 0.87954637,
            0.8800607 , 0.88139113, 0.88175637, 0.88212142
        ]
        for irow in range(tb.nrows()):
            radec = tb.getcell("DIRECTION", irow).squeeze()
            np.allclose(radec[0], ra_expected)
            np.allclose(radec[1], dec_expected)
            target = tb.getcell("TARGET", irow).squeeze()
            np.allclose(target[0], ra_expected)
            np.allclose(target[1], dec_expected)
            azel = tb.getcell("ENCODER", irow).squeeze()
            np.allclose(azel[0], az_expected[irow])
            np.allclose(azel[1], el_expected[irow])

    # test number of rows in MS MAIN
    with open_table(msfile) as tb:
        # number of MS2 rows = 76
        nrows = tb.nrows()
        assert nrows == num_records // num_pols

        # scans = 0~18
        scans = tb.getcol("SCAN_NUMBER")
        nrows_per_scan = num_arrays // num_pols
        num_scans_expected = 19
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

        # start time of first integration: 2024/9/25 15:59:19, integration time 1sec
        start_expected = datetime.datetime(2024, 9, 25, 15, 59, 19, 500000, tzinfo=datetime.timezone.utc)
        start_time = mjd2datetime(tb.getcell("TIME", 0))
        # impose msec accuracy
        assert abs((start_time - start_expected).total_seconds()) < 1e-3

        # start time of last integration: 2024/9/25 16:3:50, integration time 5sec
        end_expected = datetime.datetime(2024, 9, 25, 16, 3, 47, 500000, tzinfo=datetime.timezone.utc)
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
def test_h40_ms2_summary(msfile):
    ms = _ms()
    ms.open(msfile)
    try:
        summary = ms.summary()
    except Exception as e:
        pytest.fail(f"ms.summary was failed with the error: {e}")
    finally:
        ms.close()

    assert isinstance(summary, dict)
