from dataclasses import asdict, dataclass, field

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
    maxlen: int = 0
    option: int = 5
    shape: npt.NDArray = field(default_factory=list)


@dataclass
class PositionColumn(ArrayColumn):
    valueType: str = 'double'
    ndim: int = 1
    maxlen: int = 3
    shape: npt.NDArray = field(default_factory=lambda: np.array([3]))
    keywords: dict = field(default_factory=lambda: {
        'MEASINFO': {'Ref': 'ITRF', 'type': 'position'},
        'QuantumUnits': np.array(['m', 'm', 'm'])
    })
