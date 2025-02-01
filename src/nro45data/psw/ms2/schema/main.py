from dataclasses import dataclass, field

import numpy as np

from .column_description import (
    ArrayColumn,
    ChronoColumn,
    DurationColumn,
    PositionColumn,
    ScalarColumn,
)
from .table import Table


@dataclass
class MsMainUvwColumn(PositionColumn):
    comment: str = "Vector with uvw coordinates (in meters)"
    keywords: dict = field(
        default_factory=lambda: {"MEASINFO": {"Ref": "ITRF", "type": "uvw"}, "QuantumUnits": np.array(["m", "m", "m"])}
    )


@dataclass
class MsMainFlagColumn(ArrayColumn):
    comment: str = "The data flags, array of bools with same shape as data"
    valueType: str = "bool"
    ndim: int = 2


@dataclass
class MsMainFlagCategoryColumn(ScalarColumn):
    comment: str = "The flag category, NUM_CAT flags for each datum"
    valueType: str = "bool"
    ndim: int = 3
    keywords: dict = field(
        default_factory=lambda: {"CATEGORY": np.array([], dtype=str)}
    )


@dataclass
class MsMainWeightColumn(ArrayColumn):
    comment: str = "Weight for each polarization spectrum"
    valueType: str = "float"
    ndim: int = 1


@dataclass
class MsMainSigmaColumn(ArrayColumn):
    comment: str = "Estimated rms noise for channel with unity bandpass response"
    valueType: str = "float"
    ndim: int = 1


@dataclass
class MsMainAntenna1Column(ScalarColumn):
    comment: str = "ID of first antenna in interferometer"
    valueType: str = "int"


@dataclass
class MsMainAntenna2Column(ScalarColumn):
    comment: str = "ID of second antenna in interferometer"
    valueType: str = "int"


@dataclass
class MsMainArrayIdColumn(ScalarColumn):
    comment: str = "ID of array or subarray"
    valueType: str = "int"


@dataclass
class MsMainDataDescIdColumn(ScalarColumn):
    comment: str = "The data description table index"
    valueType: str = "int"


@dataclass
class MsMainExposureColumn(DurationColumn):
    comment: str = "The effective integration time"


@dataclass
class MsMainFeed1Column(ScalarColumn):
    comment: str = "The feed index for ANTENNA1"
    valueType: str = "int"


@dataclass
class MsMainFeed2Column(ScalarColumn):
    comment: str = "The feed index for ANTENNA2"
    valueType: str = "int"


@dataclass
class MsMainFieldIdColumn(ScalarColumn):
    comment: str = "Unique id for this pointing"
    valueType: str = "int"


@dataclass
class MsMainFlagRowColumn(ScalarColumn):
    comment: str = "Row flag - flag all data in this row if True"
    valueType: str = "bool"


@dataclass
class MsMainIntervalColumn(DurationColumn):
    comment: str = "The sampling interval"


@dataclass
class MsMainObservationIdColumn(ScalarColumn):
    comment: str = "ID for this observation, index in OBSERVATION table"
    valueType: str = "int"


@dataclass
class MsMainProcessorIdColumn(ScalarColumn):
    comment: str = "Id for backend processor, index in PROCESSOR table"
    valueType: str = "int"


@dataclass
class MsMainScanNumberColumn(ScalarColumn):
    comment: str = "Sequential scan number from on-line system"
    valueType: str = "int"


@dataclass
class MsMainStateIdColumn(ScalarColumn):
    comment: str = "ID for this observing state"
    valueType: str = "int"


@dataclass
class MsMainTimeColumn(ChronoColumn):
    comment: str = "Modified Julian Day"


@dataclass
class MsMainTimeCentroidColumn(ChronoColumn):
    comment: str = "Modified Julian Day"


@dataclass
class MsMainFloatDataColumn(ArrayColumn):
    comment: str = "Floating point data - for single dish"
    valueType: str = "float"
    ndim: int = 2


@dataclass
class MsMainTable(Table):
    ARRAY_ID: MsMainArrayIdColumn
    ANTENNA1: MsMainAntenna1Column
    ANTENNA2: MsMainAntenna2Column
    DATA_DESC_ID: MsMainDataDescIdColumn
    EXPOSURE: MsMainExposureColumn
    FEED1: MsMainFeed1Column
    FEED2: MsMainFeed2Column
    FIELD_ID: MsMainFieldIdColumn
    FLAG: MsMainFlagColumn
    FLAG_CATEGORY: MsMainFlagCategoryColumn
    FLAG_ROW: MsMainFlagRowColumn
    INTERVAL: MsMainIntervalColumn
    OBSERVATION_ID: MsMainObservationIdColumn
    PROCESSOR_ID: MsMainProcessorIdColumn
    SCAN_NUMBER: MsMainScanNumberColumn
    STATE_ID: MsMainStateIdColumn
    TIME: MsMainTimeColumn
    TIME_CENTROID: MsMainTimeCentroidColumn
    UVW: MsMainUvwColumn
    WEIGHT: MsMainWeightColumn
    SIGMA: MsMainSigmaColumn
    FLOAT_DATA: MsMainFloatDataColumn
