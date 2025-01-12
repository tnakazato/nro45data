from dataclasses import dataclass, field

import numpy as np

from .column_description import (
    ArrayColumn,
    ChronoColumn,
    ColumnDescription,
    DirectionColumn,
    DurationColumn,
    PositionColumn,
    ScalarColumn,
)
from .table import Table


@dataclass
class MsFeedPositionColumn(PositionColumn):
    comment: str = "Position of feed relative to feed reference position"


@dataclass
class MsFeedBeamOffsetColumn(DirectionColumn):
    comment: str = "Beam position offset (on sky but in antennareference frame)"
    ndim: int = 2


@dataclass
class MsFeedPolarizationTypeColumn(ScalarColumn):
    comment: str = "Type of polarization to which a given RECEPTOR responds"
    valueType: str = "string"


@dataclass
class MsFeedPolResponseColumn(ArrayColumn):
    comment: str = "D-matrix i.e. leakage between two receptors"
    valueType: str = "complex"
    ndim: int = 2


@dataclass
class MsFeedReceptorAngleColumn(ArrayColumn):
    comment: str = "The reference angle for polarization"
    valueType: str = "double"
    ndim: int = 1
    keywords: dict = field(default_factory=lambda: {"QuantumUnits": np.array(["rad"])})


@dataclass
class MsFeedAntennaIdColumn(ScalarColumn):
    comment: str = "ID of antenna in this array"
    valueType: str = "int"


@dataclass
class MsFeedBeamIdColumn(ScalarColumn):
    comment: str = "Id for BEAM model"
    valueType: str = "int"


@dataclass
class MsFeedFeedIdColumn(ScalarColumn):
    comment: str = "Feed id"
    valueType: str = "int"


@dataclass
class MsFeedIntervalColumn(DurationColumn):
    comment: str = "Interval for which this set of parameters is accurate"


@dataclass
class MsFeedNumReceptorsColumn(ScalarColumn):
    comment: str = "Number of receptors on this feed (probably 1 or 2)"
    valueType: str = "int"


@dataclass
class MsFeedSpectralWindowIdColumn(ScalarColumn):
    comment: str = "ID for this spectral window setup"
    valueType: str = "int"


@dataclass
class MsFeedTimeColumn(ChronoColumn):
    comment: str = "Midpoint of time for which this set of parameters is accurate"


@dataclass
class MsFeedFocusLengthColumn(ScalarColumn):
    comment: str = "Focus length"
    valueType: str = "double"
    keywords: dict = field(default_factory=lambda: {"QuantumUnits": np.array(["m"])})


@dataclass
class MsFeedTableColumnDescription(ColumnDescription):
    ANTENNA_ID: MsFeedAntennaIdColumn
    BEAM_ID: MsFeedBeamIdColumn
    BEAM_OFFSET: MsFeedBeamOffsetColumn
    FEED_ID: MsFeedFeedIdColumn
    FOCUS_LENGTH: MsFeedFocusLengthColumn
    INTERVAL: MsFeedIntervalColumn
    NUM_RECEPTORS: MsFeedNumReceptorsColumn
    POL_RESPONSE: MsFeedPolResponseColumn
    POLARIZATION_TYPE: MsFeedPolarizationTypeColumn
    POSITION: MsFeedPositionColumn
    RECEPTOR_ANGLE: MsFeedReceptorAngleColumn
    SPECTRAL_WINDOW_ID: MsFeedSpectralWindowIdColumn
    TIME: MsFeedTimeColumn


@dataclass
class MsFeedTable(Table):
    coldesc: MsFeedTableColumnDescription
