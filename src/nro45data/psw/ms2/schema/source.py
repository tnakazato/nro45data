from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from .column_description import (
    ArrayColumn,
    ChronoColumn,
    DurationColumn,
    FixedDirectionColumn,
    PositionColumn,
    ScalarColumn,
)
from .table import Table


@dataclass
class MsSourceDirectionColumn(FixedDirectionColumn):
    comment: str = "Direction (e.g. RA, DEC)."


@dataclass
class MsSourceProperMotionColumn(ArrayColumn):
    comment: str = "Proper motion"
    valueType: str = "double"
    ndim: int = 1
    shape: npt.NDArray = field(default_factory=lambda: np.array([2]))
    keywords: dict = field(default_factory=lambda: {"QuantumUnits": np.array(["rad/s"])})


@dataclass
class MsSourceCalibrationGroupColumn(ScalarColumn):
    comment: str = "Number of grouping for calibration purpose."
    valueType: str = "int"


@dataclass
class MsSourceCodeColumn(ScalarColumn):
    comment: str = "Special characteristics of source, e.g. Bandpass calibrator"
    valueType: str = "string"


@dataclass
class MsSourceIntervalColumn(DurationColumn):
    comment: str = "Interval of time for which this set of parameters is accurate"


@dataclass
class MsSourceNameColumn(ScalarColumn):
    comment: str = "Name of source as given during observations"
    valueType: str = "string"


@dataclass
class MsSourceNumLinesColumns(ScalarColumn):
    comment: str = "Number of spectral lines"
    valueType: str = "int"


@dataclass
class MsSourceSourceIdColumn(ScalarColumn):
    comment: str = "Source id"
    valueType: str = "int"


@dataclass
class MsSourceSpectralWindowIdColumn(ScalarColumn):
    comment: str = "ID for this spectral window setup"
    valueType: str = "int"


@dataclass
class MsSourceTimeColumn(ChronoColumn):
    comment: str = "Midpoint of time for which this set of parameters is accurate."


@dataclass
class MsSourcePositionColumn(PositionColumn):
    comment: str = "Position (e.g. for solar system objects)"


@dataclass
class MsSourceTransitionColumn(ArrayColumn):
    comment: str = "Line Transition name"
    valueType: str = "string"
    ndim: int = 1


@dataclass
class MsSourceRestFrequencyColumn(ArrayColumn):
    comment: str = "Line rest frequency"
    valueType: str = "double"
    ndim: int = 1
    keywords: dict = field(
        default_factory=lambda: {"MEASINFO": {"Ref": "LSRK", "type": "frequency"}, "QuantumUnits": np.array(["Hz"])}
    )


@dataclass
class MsSourceSysvelColumn(ArrayColumn):
    comment: str = "Systemic velocity at reference"
    valueType: str = "double"
    ndim: int = 1
    keywords: dict = field(
        default_factory=lambda: {
            "MEASINFO": {"Ref": "LSRK", "type": "radialvelocity"},
            "QuantumUnits": np.array(["m/s"]),
        }
    )


@dataclass
class MsSourceTable(Table):
    DIRECTION: MsSourceDirectionColumn
    PROPER_MOTION: MsSourceProperMotionColumn
    CALIBRATION_GROUP: MsSourceCalibrationGroupColumn
    CODE: MsSourceCodeColumn
    INTERVAL: MsSourceIntervalColumn
    NAME: MsSourceNameColumn
    NUM_LINES: MsSourceNumLinesColumns
    SOURCE_ID: MsSourceSourceIdColumn
    SPECTRAL_WINDOW_ID: MsSourceSpectralWindowIdColumn
    TIME: MsSourceTimeColumn
    POSITION: MsSourcePositionColumn
    TRANSITION: MsSourceTransitionColumn
    REST_FREQUENCY: MsSourceRestFrequencyColumn
    SYSVEL: MsSourceSysvelColumn
