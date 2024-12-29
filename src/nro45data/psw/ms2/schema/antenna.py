from dataclasses import asdict, dataclass, fields

import numpy as np

from .column_description import PositionColumn, ScalarColumn
from .data_manager_info import DataManagerInfoItem
from .table import Table


@dataclass
class AntennaOffsetColumn(PositionColumn):
    comment: str = 'Axes offset of mount to FEED REFERENCE point'


@dataclass
class AntennaPositionColumn(PositionColumn):
    comment: str = 'Antenna X,Y,Z phase reference position'


@dataclass
class AntennaTypeColumn(ScalarColumn):
    comment: str = 'Antenna type (e.g. SPACE-BASED)'
    valueType: str = 'string'


@dataclass
class AntennaDishDiameterColumn(ScalarColumn):
    comment: str = 'Physical diameter of dish'
    valueType: str = 'double'


@dataclass
class AntennaFlagRowColumn(ScalarColumn):
    comment: str = 'Flag for this row'
    valueType: str = 'bool'


@dataclass
class AntennaMountColumn(ScalarColumn):
    comment: str = 'Mount type e.g. alt-az, equatorial, etc.'
    valueType: str = 'string'


@dataclass
class AntennaNameColumn(ScalarColumn):
    comment: str = 'Antenna name, e.g. VLA22, CA03'
    valueType: str = 'string'


@dataclass
class AntennaStationColumn(ScalarColumn):
    comment: str = 'Station (antenna pad) name'
    valueType: str = 'string'


@dataclass
class AntennaTableColumnDescription:
    OFFSET: AntennaOffsetColumn
    POSITION: AntennaPositionColumn
    TYPE: AntennaTypeColumn
    DISH_DIAMETER: AntennaDishDiameterColumn
    FLAG_ROW: AntennaFlagRowColumn
    MOUNT: AntennaMountColumn
    NAME: AntennaNameColumn
    STATION: AntennaStationColumn

    @classmethod
    def as_dict(cls):
        return asdict(cls(
            OFFSET=AntennaOffsetColumn(),
            POSITION=AntennaPositionColumn(),
            TYPE=AntennaTypeColumn(),
            DISH_DIAMETER=AntennaDishDiameterColumn(),
            FLAG_ROW=AntennaFlagRowColumn(),
            MOUNT=AntennaMountColumn(),
            NAME=AntennaNameColumn(),
            STATION=AntennaStationColumn()
        ))


class AntennaTableDataManagerInfo:
    @classmethod
    def as_dict(cls):
        columns = np.array([f.name for f in fields(AntennaTableColumnDescription)])
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
class AntennaTable(Table):
    @classmethod
    def as_dict(cls):
        return asdict(cls(
            coldesc=AntennaTableColumnDescription.as_dict(),
            dminfo=AntennaTableDataManagerInfo.as_dict()
        ))
