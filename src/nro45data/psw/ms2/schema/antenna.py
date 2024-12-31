from dataclasses import dataclass, fields

import numpy as np

from .column_description import ColumnDescription, PositionColumn, ScalarColumn
from .data_manager_info import DataManagerInfoItem
from .table import Table


@dataclass
class MsAntennaOffsetColumn(PositionColumn):
    comment: str = 'Axes offset of mount to FEED REFERENCE point'


@dataclass
class MsAntennaPositionColumn(PositionColumn):
    comment: str = 'Antenna X,Y,Z phase reference position'


@dataclass
class MsAntennaTypeColumn(ScalarColumn):
    comment: str = 'Antenna type (e.g. SPACE-BASED)'
    valueType: str = 'string'


@dataclass
class MsAntennaDishDiameterColumn(ScalarColumn):
    comment: str = 'Physical diameter of dish'
    valueType: str = 'double'


@dataclass
class MsAntennaFlagRowColumn(ScalarColumn):
    comment: str = 'Flag for this row'
    valueType: str = 'bool'


@dataclass
class MsAntennaMountColumn(ScalarColumn):
    comment: str = 'Mount type e.g. alt-az, equatorial, etc.'
    valueType: str = 'string'


@dataclass
class MsAntennaNameColumn(ScalarColumn):
    comment: str = 'Antenna name, e.g. VLA22, CA03'
    valueType: str = 'string'


@dataclass
class MsAntennaStationColumn(ScalarColumn):
    comment: str = 'Station (antenna pad) name'
    valueType: str = 'string'


@dataclass
class MsAntennaTableColumnDescription(ColumnDescription):
    OFFSET: MsAntennaOffsetColumn
    POSITION: MsAntennaPositionColumn
    TYPE: MsAntennaTypeColumn
    DISH_DIAMETER: MsAntennaDishDiameterColumn
    FLAG_ROW: MsAntennaFlagRowColumn
    MOUNT: MsAntennaMountColumn
    NAME: MsAntennaNameColumn
    STATION: MsAntennaStationColumn


class MsAntennaTableDataManagerInfo:
    @classmethod
    def as_dict(cls):
        columns = np.array([f.name for f in fields(MsAntennaTableColumnDescription)])
        info_items = [
            DataManagerInfoItem(
                COLUMNS=columns,
                SEQNR=0,
                SPEC={
                    'BUCKETSIZE': 3332,
                    'IndexLength': 126,
                    'MaxCacheSize': 2,
                    'PERSCACHESIZE': 2
                }
            )
        ]
        return dict((f'*{i.SEQNR + 1}', i) for i in info_items)


@dataclass
class MsAntennaTable(Table):
    coldesc: MsAntennaTableColumnDescription
    dminfo: MsAntennaTableDataManagerInfo
