from dataclasses import asdict, dataclass, field, fields

import numpy as np
import numpy.typing as npt


@dataclass
class StandardColumn:
    comment: str = ''
    dataManagerGroup: str = 'StandardStMan'
    dataManagerType: str = 'StandardStMan'
    keywords: dict = field(default_factory=dict)
    maxlen: int = 0
    option: int = 0


@dataclass
class ScalarColumn(StandardColumn):
    valueType: str = ''


@dataclass
class ArrayColumn(StandardColumn):
    valueType: str = ''
    ndim: int = 0
    option: int = 0


@dataclass
class DurationColumn(ScalarColumn):
    valueType: str = 'double'
    keywords: dict = field(default_factory=lambda: {
        'QuantumUnits': np.array(['s'])
    })


@dataclass
class ChronoColumn(ScalarColumn):
    valueType: str = 'double'
    keywords: dict = field(default_factory=lambda: {
        'MEASINFO': {'Ref': 'UTC', 'type': 'epoch'},
        'QuantumUnits': np.array(['s'])
    })


@dataclass
class PositionColumn(ArrayColumn):
    valueType: str = 'double'
    ndim: int = 1
    shape: npt.NDArray = field(default_factory=lambda: np.array([3]))
    keywords: dict = field(default_factory=lambda: {
        'MEASINFO': {'Ref': 'ITRF', 'type': 'position'},
        'QuantumUnits': np.array(['m', 'm', 'm'])
    })


@dataclass
class DirectionColumn(ArrayColumn):
    valueType: str = 'double'
    ndim: int = -1
    keywords: dict = field(default_factory=lambda: {
        'MEASINFO': {'Ref': 'J2000', 'type': 'direction'},
        'QuantumUnits': np.array(['rad', 'rad'])
    })


@dataclass
class FixedDirectionColumn(ArrayColumn):
    valueType: str = 'double'
    ndim: int = 1
    shape: npt.NDArray = field(default_factory=lambda: np.array([2]))
    keywords: dict = field(default_factory=lambda: {
        'MEASINFO': {'Ref': 'J2000', 'type': 'direction'},
        'QuantumUnits': np.array(['rad', 'rad'])
    })


@dataclass
class ColumnDescription:
    @classmethod
    def as_dict(cls):
        return dict(
            (f.name, asdict(f.type())) for f in fields(cls)
        )
