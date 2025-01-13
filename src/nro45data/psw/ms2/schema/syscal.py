from dataclasses import dataclass, field

import numpy as np

from .column_description import ArrayColumn, ChronoColumn, ColumnDescription, DurationColumn, ScalarColumn
from .table import Table


@dataclass
class TemperatureArrayColumn(ArrayColumn):
    valueType: str = "float"
    ndim: int = 2
    keywords: dict = field(default_factory=lambda: {"QuantumUnits": np.array(["K"])})


@dataclass
class MsSyscalAntennaIdColumn(ScalarColumn):
    comment: str = "ID of antenna in this array"
    valueType: str = "int"


@dataclass
class MsSyscalFeedIdColumn(ScalarColumn):
    comment: str = "Feed id"
    valueType: str = "int"


@dataclass
class MsSyscalIntervalColumn(DurationColumn):
    comment: str = "Interval for which this set of parameters is accurate"


@dataclass
class MsSyscalSpectralWindowIdColumn(ScalarColumn):
    comment: str = "ID for this spectral window setup"
    valueType: str = "int"


@dataclass
class MsSyscalTimeColumn(ChronoColumn):
    comment: str = "Midpoint of time for which this set of parameters is accurate"


@dataclass
class MsSyscalTcalSpectrumColumn(TemperatureArrayColumn):
    comment: str = "Calibration temperature for each channel and receptor"


@dataclass
class MsSyscalTrxSpectrumColumn(TemperatureArrayColumn):
    comment: str = "Receiver temperature for each channel and receptor"


@dataclass
class MsSyscalTskySpectrumColumn(TemperatureArrayColumn):
    comment: str = "Sky temperature for each channel and receptor"


@dataclass
class MsSyscalTsysSpectrumColumn(TemperatureArrayColumn):
    comment: str = "System temperature for each channel and receptor"


@dataclass
class MsSyscalTantSpectrumColumn(TemperatureArrayColumn):
    comment: str = "Antenna temperature for each channel and receptor"


@dataclass
class MsSyscalTantTsysSpectrumColumn(ArrayColumn):
    comment: str = "Ratio of antenna to system temperature for each channel and receptor"
    valueType: str = "float"
    ndim: int = 2


@dataclass
class MsSyscalTcalFlagColumn(ScalarColumn):
    comment: str = "Flag for TCAL"
    valueType: str = "bool"


@dataclass
class MsSyscalTrxFlagColumn(ScalarColumn):
    comment: str = "Flag for TRX"
    valueType: str = "bool"


@dataclass
class MsSyscalTskyFlagColumn(ScalarColumn):
    comment: str = "Flag for TSKY"
    valueType: str = "bool"


@dataclass
class MsSyscalTsysFlagColumn(ScalarColumn):
    comment: str = "Flag for TSYS"
    valueType: str = "bool"


@dataclass
class MsSyscalTantFlagColumn(ScalarColumn):
    comment: str = "Flag for TANT"
    valueType: str = "bool"


@dataclass
class MsSyscalTantTsysFlagColumn(ScalarColumn):
    comment: str = "Flag for TANT_TSYS"
    valueType: str = "bool"


@dataclass
class MsSyscalTableColumnDescription(ColumnDescription):
    ANTENNA_ID: MsSyscalAntennaIdColumn
    FEED_ID: MsSyscalFeedIdColumn
    INTERVAL: MsSyscalIntervalColumn
    SPECTRAL_WINDOW_ID: MsSyscalSpectralWindowIdColumn
    TIME: MsSyscalTimeColumn
    TCAL_SPECTRUM: MsSyscalTcalSpectrumColumn
    TRX_SPECTRUM: MsSyscalTrxSpectrumColumn
    TSKY_SPECTRUM: MsSyscalTskySpectrumColumn
    TSYS_SPECTRUM: MsSyscalTsysSpectrumColumn
    TANT_SPECTRUM: MsSyscalTantSpectrumColumn
    TANT_TSYS_SPECTRUM: MsSyscalTantTsysSpectrumColumn
    TCAL_FLAG: MsSyscalTcalFlagColumn
    TRX_FLAG: MsSyscalTrxFlagColumn
    TSKY_FLAG: MsSyscalTskyFlagColumn
    TSYS_FLAG: MsSyscalTsysFlagColumn
    TANT_FLAG: MsSyscalTantFlagColumn
    TANT_TSYS_FLAG: MsSyscalTantTsysFlagColumn


@dataclass
class MsSyscalTable(Table):
    coldesc: MsSyscalTableColumnDescription
