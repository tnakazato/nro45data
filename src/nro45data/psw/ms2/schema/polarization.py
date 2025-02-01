from dataclasses import dataclass

from .column_description import ArrayColumn, ScalarColumn
from .table import Table


@dataclass
class MsPolarizationCorrTypeColumn(ArrayColumn):
    comment: str = "The polarization type for each correlation product, as a Stokes enum."
    ndim: int = 1
    valueType: str = "int"


@dataclass
class MsPolarizationCorrProductColumn(ArrayColumn):
    comment: str = "Indices describing receptors of feed going into correlation"
    ndim: int = 2
    valueType: str = "int"


@dataclass
class MsPolarizationFlagRowColumn(ScalarColumn):
    comment: str = "Row flag"
    valueType: str = "bool"


@dataclass
class MsPolarizationNumCorrColumn(ScalarColumn):
    comment: str = "Number of correlation products"
    valueType: str = "int"


@dataclass
class MsPolarizationTable(Table):
    CORR_TYPE: MsPolarizationCorrTypeColumn
    CORR_PRODUCT: MsPolarizationCorrProductColumn
    FLAG_ROW: MsPolarizationFlagRowColumn
    NUM_CORR: MsPolarizationNumCorrColumn
