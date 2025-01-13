from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from .column_description import ArrayColumn, ChronoColumn, ColumnDescription, ScalarColumn
from .table import Table


@dataclass
class MsObservationTimeRangeColumn(ArrayColumn):
    comment: str = "Start and end of observation"
    valueType: str = "double"
    ndim: int = 1
    shape: npt.NDArray = field(default_factory=lambda: np.array([2]))
    keywords: dict = field(
        default_factory=lambda: {"MEASINFO": {"Ref": "UTC", "type": "epoch"}, "QuantumUnits": np.array(["s"])}
    )


@dataclass
class MsObservationLogColumn(ArrayColumn):
    comment: str = "Observation log"
    valueType: str = "string"


@dataclass
class MsObservationScheduleColumn(ArrayColumn):
    comment: str = "Observing schedule"
    valueType: str = "string"


@dataclass
class MsObservationFlagRowColumn(ScalarColumn):
    comment: str = "Row flag"
    valueType: str = "bool"


@dataclass
class MsObservationObserverColumn(ScalarColumn):
    comment: str = "Name of observer(s)"
    valueType: str = "string"


@dataclass
class MsObservationProjectColumn(ScalarColumn):
    comment: str = "Project identification string"
    valueType: str = "string"


@dataclass
class MsObservationReleaseDateColumn(ChronoColumn):
    comment: str = "Release date when data becomes public"


@dataclass
class MsObservationScheduleTypeColumn(ScalarColumn):
    comment: str = "Observing schedule type"
    valueType: str = "string"


@dataclass
class MsObservationTelescopeNameColumn(ScalarColumn):
    comment: str = "Telescope Name (e.g. WSRT, VLBA)"
    valueType: str = "string"


@dataclass
class MsObservationTableColumnDescription(ColumnDescription):
    TIME_RANGE: MsObservationTimeRangeColumn
    LOG: MsObservationLogColumn
    SCHEDULE: MsObservationScheduleColumn
    FLAG_ROW: MsObservationFlagRowColumn
    OBSERVER: MsObservationObserverColumn
    PROJECT: MsObservationProjectColumn
    RELEASE_DATE: MsObservationReleaseDateColumn
    SCHEDULE_TYPE: MsObservationScheduleTypeColumn
    TELESCOPE_NAME: MsObservationTelescopeNameColumn


@dataclass
class MsObservationTable(Table):
    coldesc: MsObservationTableColumnDescription
