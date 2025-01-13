from dataclasses import dataclass

from .column_description import PositionColumn, ScalarColumn
from .table import Table


@dataclass
class MsAntennaOffsetColumn(PositionColumn):
    comment: str = "Axes offset of mount to FEED REFERENCE point"


@dataclass
class MsAntennaPositionColumn(PositionColumn):
    comment: str = "Antenna X,Y,Z phase reference position"


@dataclass
class MsAntennaTypeColumn(ScalarColumn):
    comment: str = "Antenna type (e.g. SPACE-BASED)"
    valueType: str = "string"


@dataclass
class MsAntennaDishDiameterColumn(ScalarColumn):
    comment: str = "Physical diameter of dish"
    valueType: str = "double"


@dataclass
class MsAntennaFlagRowColumn(ScalarColumn):
    comment: str = "Flag for this row"
    valueType: str = "bool"


@dataclass
class MsAntennaMountColumn(ScalarColumn):
    comment: str = "Mount type e.g. alt-az, equatorial, etc."
    valueType: str = "string"


@dataclass
class MsAntennaNameColumn(ScalarColumn):
    comment: str = "Antenna name, e.g. VLA22, CA03"
    valueType: str = "string"


@dataclass
class MsAntennaStationColumn(ScalarColumn):
    comment: str = "Station (antenna pad) name"
    valueType: str = "string"


@dataclass
class MsAntennaTable(Table):
    OFFSET: MsAntennaOffsetColumn
    POSITION: MsAntennaPositionColumn
    TYPE: MsAntennaTypeColumn
    DISH_DIAMETER: MsAntennaDishDiameterColumn
    FLAG_ROW: MsAntennaFlagRowColumn
    MOUNT: MsAntennaMountColumn
    NAME: MsAntennaNameColumn
    STATION: MsAntennaStationColumn
