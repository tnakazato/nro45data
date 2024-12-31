from dataclasses import dataclass

import numpy as np

from .column_description import ChronoColumn, ColumnDescription, DurationColumn, ScalarColumn
from .data_manager_info import DataManagerInfoItem
from .table import Table


@dataclass
class MsFlagCmdAppliedColumn(ScalarColumn):
    comment: str = 'True if flag has been applied to main table'
    valueType: str = 'bool'


@dataclass
class MsFlagCmdCommandColumn(ScalarColumn):
    comment: str = 'Flagging command'
    valueType: str = 'string'


@dataclass
class MsFlagCmdIntervalColumn(DurationColumn):
    comment: str = 'Time interval for which this flag is valid'


@dataclass
class MsFlagCmdLevelColumn(ScalarColumn):
    comment: str = 'Flag level - revision level '
    valueType: str = 'int'


@dataclass
class MsFlagCmdReasonColumn(ScalarColumn):
    comment: str = 'Flag reason'
    valueType: str = 'string'


@dataclass
class MsFlagCmdSeverityColumn(ScalarColumn):
    comment: str = 'Severity code (0-10) '
    valueType: str = 'int'


@dataclass
class MsFlagCmdTimeColumn(ChronoColumn):
    comment: str = 'Midpoint of interval for which this flag is valid'


@dataclass
class MsFlagCmdTypeColumn(ScalarColumn):
    comment: str = 'Type of flag (FLAG or UNFLAG)'
    valueType: str = 'string'


@dataclass
class MsFlagCmdTableColumnDescription(ColumnDescription):
    APPLIED: MsFlagCmdAppliedColumn
    COMMAND: MsFlagCmdCommandColumn
    INTERVAL: MsFlagCmdIntervalColumn
    LEVEL: MsFlagCmdLevelColumn
    REASON: MsFlagCmdReasonColumn
    SEVERITY: MsFlagCmdSeverityColumn
    TIME: MsFlagCmdTimeColumn
    TYPE: MsFlagCmdTypeColumn


@dataclass
class MsFlagCmdTable(Table):
    coldesc: MsFlagCmdTableColumnDescription
