from dataclasses import dataclass, fields

import numpy as np

from .column_description import ColumnDescription, PositionColumn, ScalarColumn
from .data_manager_info import DataManagerInfoItem
from .table import Table


@dataclass
class MsProcessorFlagRowColumn(ScalarColumn):
    comment: str = 'Row flag'
    valueType: str = 'bool'


@dataclass
class MsProcessorModeIdColumn(ScalarColumn):
    comment: str = 'Processor mode ID'
    valueType: str = 'int'


@dataclass
class MsProcessorTypeColumn(ScalarColumn):
    comment: str = 'Processor type'
    valueType: str = 'string'


@dataclass
class MsProcessorTypeIdColumn(ScalarColumn):
    comment: str = 'Processor type id'
    valueType: str = 'int'


@dataclass
class MsProcessorSubTypeColumn(ScalarColumn):
    comment: str = 'Processor sub type'
    valueType: str = 'string'


@dataclass
class MsProcessorTableColumnDescription(ColumnDescription):
    FLAG_ROW: MsProcessorFlagRowColumn
    MODE_ID: MsProcessorModeIdColumn
    TYPE: MsProcessorTypeColumn
    TYPE_ID: MsProcessorTypeIdColumn
    SUB_TYPE: MsProcessorSubTypeColumn


@dataclass
class MsProcessorTable(Table):
    coldesc: MsProcessorTableColumnDescription
