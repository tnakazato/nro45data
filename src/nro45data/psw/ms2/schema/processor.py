from dataclasses import dataclass

from .column_description import ScalarColumn
from .table import Table


@dataclass
class MsProcessorFlagRowColumn(ScalarColumn):
    comment: str = "Row flag"
    valueType: str = "bool"


@dataclass
class MsProcessorModeIdColumn(ScalarColumn):
    comment: str = "Processor mode ID"
    valueType: str = "int"


@dataclass
class MsProcessorTypeColumn(ScalarColumn):
    comment: str = "Processor type"
    valueType: str = "string"


@dataclass
class MsProcessorTypeIdColumn(ScalarColumn):
    comment: str = "Processor type id"
    valueType: str = "int"


@dataclass
class MsProcessorSubTypeColumn(ScalarColumn):
    comment: str = "Processor sub type"
    valueType: str = "string"


@dataclass
class MsProcessorTable(Table):
    FLAG_ROW: MsProcessorFlagRowColumn
    MODE_ID: MsProcessorModeIdColumn
    TYPE: MsProcessorTypeColumn
    TYPE_ID: MsProcessorTypeIdColumn
    SUB_TYPE: MsProcessorSubTypeColumn
