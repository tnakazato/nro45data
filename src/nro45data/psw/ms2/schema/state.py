from dataclasses import dataclass, field

import numpy as np

from .column_description import ColumnDescription, ScalarColumn
from .data_manager_info import DataManagerInfoItem
from .table import Table


@dataclass
class MsStateCalColumn(ScalarColumn):
    comment: str = 'Noise calibration temperature'
    valueType: str = 'double'
    keywords: dict = field(default_factory=lambda: {
        'QuantumUnits': np.array(['K'])
    })


@dataclass
class MsStateFlagRowColumn(ScalarColumn):
    comment: str = 'Row flag'
    valueType: str = 'bool'


@dataclass
class MsStateLoadColumn(ScalarColumn):
    comment: str = 'Load temperature'
    valueType: str = 'double'
    keywords: dict = field(default_factory=lambda: {
        'QuantumUnits': np.array(['K'])
    })


@dataclass
class MsStateObsModeColumn(ScalarColumn):
    comment: str = 'Observing mode, e.g., OFF_SPECTRUM'
    valueType: str = 'string'


@dataclass
class MsStateRefColumn(ScalarColumn):
    comment: str = 'True for a reference observation'
    valueType: str = 'bool'


@dataclass
class MsStateSigColumn(ScalarColumn):
    comment: str = 'True for a source observation'
    valueType: str = 'bool'


@dataclass
class MsStateSubScanColumn(ScalarColumn):
    comment: str = 'Sub scan number, relative to scan number'
    valueType: str = 'int'


@dataclass
class MsStateTableColumnDescription(ColumnDescription):
    CAL: MsStateCalColumn
    FLAG_ROW: MsStateFlagRowColumn
    LOAD: MsStateLoadColumn
    OBS_MODE: MsStateObsModeColumn
    REF: MsStateRefColumn
    SIG: MsStateSigColumn
    SUB_SCAN: MsStateSubScanColumn


@dataclass
class MsStateTable(Table):
    coldesc: MsStateTableColumnDescription
