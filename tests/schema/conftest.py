import os
import tempfile

import pytest

import nro45data.psw.ms2.builder as builder


@pytest.fixture(scope="session")
def msfile():
    with tempfile.TemporaryDirectory() as workdir:
        name = os.path.join(workdir, "test.ms")
        builder.build_ms2(name)
        yield name
