from dataclasses import dataclass

from .column_description import ScalarColumn, ColumnDescription
from .table import Table


@dataclass
class MsDataDescriptionFlagRowColumn(ScalarColumn):
    comment: str = 'Flag this row'
    valueType: str = 'bool'


@dataclass
class MsDataDescriptionPolarizationIdColumn(ScalarColumn):
    comment: str = 'Pointer to polarization table'
    valueType: str = 'int'


@dataclass
class MsDataDescriptionSpectralWindowIdColumn(ScalarColumn):
    comment: str = 'Pointer to spectralwindow table'
    valueType: str = 'int'


@dataclass
class MsDataDescriptionTableColumnDescription(ColumnDescription):
    FLAG_ROW: MsDataDescriptionFlagRowColumn
    POLARIZATION_ID: MsDataDescriptionPolarizationIdColumn
    SPECTRAL_WINDOW_ID: MsDataDescriptionSpectralWindowIdColumn


@dataclass
class MsDataDescriptionTable(Table):
    coldesc: MsDataDescriptionTableColumnDescription