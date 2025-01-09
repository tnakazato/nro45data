from dataclasses import dataclass, field

import numpy as np

from .column_description import ChronoColumn, ColumnDescription, DirectionColumn, DurationColumn, ScalarColumn
from .data_manager_info import DataManagerInfoItem
from .table import Table


@dataclass
class MsPointingDirectionColumn(DirectionColumn):
    comment: str = 'Antenna pointing direction as polynomial in time'
    keywords: dict = field(default_factory=lambda: {
        'MEASINFO': {'Ref': 'AZELGEO', 'type': 'direction'},
        'QuantumUnits': np.array(['rad', 'rad'])
    })


@dataclass
class MsPointingAntennaIdColumn(ScalarColumn):
    comment: str = 'Antenna Id'
    valueType: str = 'int'


@dataclass
class MsPointingIntervalColumn(DurationColumn):
    comment: str = 'Time interval'


@dataclass
class MsPointingNameColumn(ScalarColumn):
    comment: str = 'Pointing position name'
    valueType: str = 'string'


@dataclass
class MsPointingNumPolyColumn(ScalarColumn):
    comment: str = 'Series order'
    valueType: str = 'int'


@dataclass
class MsPointingTargetColumn(DirectionColumn):
    comment: str = 'target direction as polynomial in time'
    keywords: dict = field(default_factory=lambda: {
        'MEASINFO': {'Ref': 'AZELGEO', 'type': 'direction'},
        'QuantumUnits': np.array(['rad', 'rad'])
    })
    ndim: int = -1


@dataclass
class MsPointingTimeColumn(ChronoColumn):
    comment: str = 'Time interval midpoint'


@dataclass
class MsPointingTimeOriginColumn(ChronoColumn):
    comment: str = 'Time origin for direction'


@dataclass
class MsPointingTrackingColumn(ScalarColumn):
    comment: str = 'Tracking flag - True if on position'
    valueType: str = 'bool'


@dataclass
class MsPointingSourceOffsetColumn(DirectionColumn):
    comment: str = 'Offset from source position'
    ndim: int = -1


@dataclass
class MsPointingEncoderColumn(DirectionColumn):
    comment: str = 'Encoder values'
    keywords: dict = field(default_factory=lambda: {
        'MEASINFO': {'Ref': 'AZELGEO', 'type': 'direction'},
        'QuantumUnits': np.array(['rad', 'rad'])
    })
    ndim: int = -1


@dataclass
class MsPointingOnSourceColumn(ScalarColumn):
    comment: str = 'On source flag'
    valueType: str = 'bool'


@dataclass
class MsPointingTableColumnDescription(ColumnDescription):
    ANTENNA_ID: MsPointingAntennaIdColumn
    DIRECTION: MsPointingDirectionColumn
    INTERVAL: MsPointingIntervalColumn
    NAME: MsPointingNameColumn
    NUM_POLY: MsPointingNumPolyColumn
    TARGET: MsPointingTargetColumn
    TIME: MsPointingTimeColumn
    TIME_ORIGIN: MsPointingTimeOriginColumn
    TRACKING: MsPointingTrackingColumn
    SOURCE_OFFSET: MsPointingSourceOffsetColumn
    ENCODER: MsPointingEncoderColumn
    ON_SOURCE: MsPointingOnSourceColumn


@dataclass
class MsPointingTable(Table):
    coldesc: MsPointingTableColumnDescription
