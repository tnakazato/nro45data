from dataclasses import dataclass

from .column_description import ArrayColumn, ChronoColumn, ColumnDescription, ScalarColumn
from .table import Table


@dataclass
class MsHistoryAppParamsColumn(ArrayColumn):
    comment: str = "Application parameters"
    ndim: int = 1
    valueType: str = "string"


@dataclass
class MsHistoryCliCommandColumn(ArrayColumn):
    comment: str = "CLI command sequence"
    ndim: int = 1
    valueType: str = "string"


@dataclass
class MsHistoryApplicationColumn(ScalarColumn):
    comment: str = "Application name"
    valueType: str = "string"


@dataclass
class MsHistoryMessageColumn(ScalarColumn):
    comment: str = "Log message"
    valueType: str = "string"


@dataclass
class MsHitoryObjectIdColumn(ScalarColumn):
    comment: str = "Originating ObjectID"
    valueType: str = "int"


@dataclass
class MsHistoryObservationIdColumn(ScalarColumn):
    comment: str = "Observation id (index in OBSERVATION table)"
    valueType: str = "int"


@dataclass
class MsHistoryOriginColumn(ScalarColumn):
    comment: str = "(Source code) origin from which message originated"
    valueType: str = "string"


@dataclass
class MsHistoryPriorityColumn(ScalarColumn):
    comment: str = "Message priority"
    valueType: str = "string"


@dataclass
class MsHistoryTimeColumn(ChronoColumn):
    comment: str = "Timestamp of message"


@dataclass
class MsHistoryTableColumnDescription(ColumnDescription):
    APP_PARAMS: MsHistoryAppParamsColumn
    CLI_COMMAND: MsHistoryCliCommandColumn
    APPLICATION: MsHistoryApplicationColumn
    MESSAGE: MsHistoryMessageColumn
    OBJECT_ID: MsHitoryObjectIdColumn
    OBSERVATION_ID: MsHistoryObservationIdColumn
    ORIGIN: MsHistoryOriginColumn
    PRIORITY: MsHistoryPriorityColumn
    TIME: MsHistoryTimeColumn


@dataclass
class MsHistoryTable(Table):
    coldesc: MsHistoryTableColumnDescription
