from dataclasses import dataclass

from .column_description import ChronoColumn, DirectionColumn, ScalarColumn
from .table import Table


@dataclass
class MsFieldCodeColumn(ScalarColumn):
    comment: str = "Special characteristics of field, e.g. Bandpass calibrator"
    valueType: str = "string"


@dataclass
class MsFieldFlagRowColumn(ScalarColumn):
    comment: str = "Row Flag"
    valueType: str = "bool"


@dataclass
class MsFieldNameColumn(ScalarColumn):
    comment: str = "Name of this field"
    valueType: str = "string"


@dataclass
class MsFieldNumPolyColumn(ScalarColumn):
    comment: str = "Polynomial order of _DIR columns"
    valueType: str = "int"


@dataclass
class MsFieldSourceIdColumn(ScalarColumn):
    comment: str = "Source id"
    valueType: str = "int"


@dataclass
class MsFieldTimeColumn(ChronoColumn):
    comment: str = "Time origin for direction and rate"


@dataclass
class MsFieldPhaseDirColumn(DirectionColumn):
    comment: str = "Phase direction"
    ndim: int = 2


@dataclass
class MsFieldDelayDirColumn(DirectionColumn):
    comment: str = "Delay direction"
    ndim: int = 2


@dataclass
class MsFieldReferenceDirColumn(DirectionColumn):
    comment: str = "Reference direction"
    ndim: int = 2


@dataclass
class MsFieldTable(Table):
    CODE: MsFieldCodeColumn
    FLAG_ROW: MsFieldFlagRowColumn
    NAME: MsFieldNameColumn
    NUM_POLY: MsFieldNumPolyColumn
    SOURCE_ID: MsFieldSourceIdColumn
    TIME: MsFieldTimeColumn
    PHASE_DIR: MsFieldPhaseDirColumn
    DELAY_DIR: MsFieldDelayDirColumn
    REFERENCE_DIR: MsFieldReferenceDirColumn
