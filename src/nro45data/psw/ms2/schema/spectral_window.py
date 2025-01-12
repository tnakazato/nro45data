from dataclasses import dataclass, field

import numpy as np

from .column_description import ArrayColumn, ColumnDescription, ScalarColumn
from .table import Table


@dataclass
class MsSpectralWindowMeasFreqRefColumn(ScalarColumn):
    comment: str = 'Frequency Measure reference'
    valueType: str = 'int'


@dataclass
class MsSpectralWindowChanFreqColumn(ArrayColumn):
    comment: str = 'Center frequencies for each channel in the data matrix'
    valueType: str = 'double'
    ndim: int = 1
    keywords: dict = field(default_factory=lambda: {
        'MEASINFO': {
            'TabRefCodes': np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 64]),
            'TabRefTypes': np.array([
                'REST', 'LSRK', 'LSRD', 'BARY', 'GEO', 'TOPO',
                'GALACTO', 'LGROUP', 'CMB', 'Undefined'
            ]),
            'VarRefCol': 'MEAS_FREQ_REF',
            'type': 'frequency'
        },
        'QuantumUnits': np.array(['Hz'])
    })


@dataclass
class MsSpectralWindowRefFrequencyColumn(ScalarColumn):
    comment: str = 'The reference frequency'
    valueType: str = 'double'
    keywords: dict = field(default_factory=lambda: {
        'MEASINFO': {
            'TabRefCodes': np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 64]),
            'TabRefTypes': np.array([
                'REST', 'LSRK', 'LSRD', 'BARY', 'GEO', 'TOPO',
                'GALACTO', 'LGROUP', 'CMB', 'Undefined'
            ]),
            'VarRefCol': 'MEAS_FREQ_REF',
            'type': 'frequency'
        },
        'QuantumUnits': np.array(['Hz'])
    })


@dataclass
class MsSpectralWindowChanWidthColumn(ArrayColumn):
    comment: str = 'Channel width for each channel'
    valueType: str = 'double'
    ndim: int = 1
    keywords: dict = field(default_factory=lambda: {
        'QuantumUnits': np.array(['Hz'])
    })


@dataclass
class MsSpectralWindowEffectiveBWColumn(ArrayColumn):
    comment: str = 'Effective noise bandwidth of each channel'
    valueType: str = 'double'
    ndim: int = 1
    keywords: dict = field(default_factory=lambda: {
        'QuantumUnits': np.array(['Hz'])
    })


@dataclass
class MsSpectralWindowResolutionColumn(ArrayColumn):
    comment: str = 'Effective resolution of each channel'
    valueType: str = 'double'
    ndim: int = 1
    keywords: dict = field(default_factory=lambda: {
        'QuantumUnits': np.array(['Hz'])
    })


@dataclass
class MsSpectralWindowFlagRowColumn(ScalarColumn):
    comment: str = 'Row flag'
    valueType: str = 'bool'


@dataclass
class MsSpectralWindowFreqGroupColumn(ScalarColumn):
    comment: str = 'Frequency group'
    valueType: str = 'int'


@dataclass
class MsSpectralWindowFreqGroupNameColumn(ScalarColumn):
    comment: str = 'Frequency group name'
    valueType: str = 'string'


@dataclass
class MsSpectralWindowIfConvChainColumn(ScalarColumn):
    comment: str = 'The IF conversion chain number'
    valueType: str = 'int'


@dataclass
class MsSpectralWindowNameColumn(ScalarColumn):
    comment: str = 'Spectral window name'
    valueType: str = 'string'


@dataclass
class MsSpectralWindowNetSidebandColumn(ScalarColumn):
    comment: str = 'Net sideband'
    valueType: str = 'int'


@dataclass
class MsSpectralWindowNumChanColumn(ScalarColumn):
    comment: str = 'Number of spectral channels'
    valueType: str = 'int'


@dataclass
class MsSpectralWindowTotalBandwidthColumn(ScalarColumn):
    comment: str = 'The total bandwidth for this window'
    valueType: str = 'double'
    keywords: dict = field(default_factory=lambda: {
        'QuantumUnits': np.array(['Hz'])
    })


@dataclass
class MsSpectralWindowBbcNoColumn(ScalarColumn):
    comment: str = 'Baseband converter number'
    valueType: str = 'int'


@dataclass
class MsSpectralWindowAssocSpwIdColumn(ArrayColumn):
    comment: str = 'Associated spectral window id'
    valueType: str = 'int'
    ndim: int = -1


@dataclass
class MsSpectralWindowAssocNatureColumn(ArrayColumn):
    comment: str = 'Nature of association with other spectral window'
    valueType: str = 'string'
    ndim: int = -1


@dataclass
class MsSpectralWindowTableColumnDescription(ColumnDescription):
    MEAS_FREQ_REF: MsSpectralWindowMeasFreqRefColumn
    CHAN_FREQ: MsSpectralWindowChanFreqColumn
    REF_FREQUENCY: MsSpectralWindowRefFrequencyColumn
    CHAN_WIDTH: MsSpectralWindowChanWidthColumn
    EFFECTIVE_BW: MsSpectralWindowEffectiveBWColumn
    RESOLUTION: MsSpectralWindowResolutionColumn
    FLAG_ROW: MsSpectralWindowFlagRowColumn
    FREQ_GROUP: MsSpectralWindowFreqGroupColumn
    FREQ_GROUP_NAME: MsSpectralWindowFreqGroupNameColumn
    IF_CONV_CHAIN: MsSpectralWindowIfConvChainColumn
    NAME: MsSpectralWindowNameColumn
    NET_SIDEBAND: MsSpectralWindowNetSidebandColumn
    NUM_CHAN: MsSpectralWindowNumChanColumn
    TOTAL_BANDWIDTH: MsSpectralWindowTotalBandwidthColumn
    BBC_NO: MsSpectralWindowBbcNoColumn
    ASSOC_SPW_ID: MsSpectralWindowAssocSpwIdColumn
    ASSOC_NATURE: MsSpectralWindowAssocNatureColumn


@dataclass
class MsSpectralWindowTable(Table):
    coldesc: MsSpectralWindowTableColumnDescription
