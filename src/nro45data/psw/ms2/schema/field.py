from dataclasses import dataclass

from .column_description import ChronoColumn, ColumnDescription, DirectionColumn, ScalarColumn
from .data_manager_info import DataManagerInfoItem
from .table import Table


@dataclass
class MsFieldCodeColumn(ScalarColumn):
    comment: str = 'Special characteristics of field, e.g. Bandpass calibrator'
    valueType: str = 'string'


@dataclass
class MsFieldFlagRowColumn(ScalarColumn):
    comment: str = 'Row Flag'
    valueType: str = 'bool'


@dataclass
class MsFieldNameColumn(ScalarColumn):
    comment: str = 'Name of this field'
    valueType: str = 'string'


@dataclass
class MsFieldNumPolyColumn(ScalarColumn):
    comment: str = 'Polynomial order of _DIR columns'
    valueType: str = 'int'


@dataclass
class MsFieldSourceIdColumn(ScalarColumn):
    comment: str = 'Source id'
    valueType: str = 'int'


@dataclass
class MsFieldTimeColumn(ChronoColumn):
    comment: str = 'Time origin for direction and rate'


@dataclass
class MsFieldPhaseDirColumn(DirectionColumn):
    comment: str = 'Phase direction'


@dataclass
class MsFieldDelayDirColumn(DirectionColumn):
    comment: str = 'Delay direction'


@dataclass
class MsFieldReferenceDirColumn(DirectionColumn):
    comment: str = 'Reference direction'


@dataclass
class MsFieldTableColumnDescription(ColumnDescription):
    CODE: MsFieldCodeColumn
    FLAG_ROW: MsFieldFlagRowColumn
    NAME: MsFieldNameColumn
    NUM_POLY: MsFieldNumPolyColumn
    SOURCE_ID: MsFieldSourceIdColumn
    TIME: MsFieldTimeColumn
    PHASE_DIR: MsFieldPhaseDirColumn
    DELAY_DIR: MsFieldDelayDirColumn
    REFERENCE_DIR: MsFieldReferenceDirColumn


@dataclass
class MsFieldTable(Table):
    coldesc: MsFieldTableColumnDescription
