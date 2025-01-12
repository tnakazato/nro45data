from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from .column_description import ArrayColumn, ChronoColumn, ColumnDescription, DurationColumn, ScalarColumn
from .table import Table


@dataclass
class MsWeatherAntennaIdColumn(ScalarColumn):
    comment: str = "Antenna number"
    valueType: str = "int"


@dataclass
class MsWeatherIntervalColumn(DurationColumn):
    comment: str = "Interval over which data is relevant"


@dataclass
class MsWeatherTimeColumn(ChronoColumn):
    comment: str = "An MEpoch specifying the midpoint of the time forwhich data is relevant"


@dataclass
class MsWeatherPressureColumn(ScalarColumn):
    comment: str = "Ambient atmospheric pressure"
    valueType: str = "float"
    keywords: dict = field(default_factory=lambda: {"QuantumUnits": np.array(["hPa"])})


@dataclass
class MsWeatherPressureFlagColumn(ScalarColumn):
    comment: str = "Flag for ambient atmospheric pressure"
    valueType: str = "bool"


@dataclass
class MsWeatherRelHumidityColumn(ScalarColumn):
    comment: str = "Ambient relative humidity"
    valueType: str = "float"
    keywords: dict = field(default_factory=lambda: {"QuantumUnits": np.array(["%"])})


@dataclass
class MsWeatherRelHumidityFlagColumn(ScalarColumn):
    comment: str = "Flag for ambient relative humidity"
    valueType: str = "bool"


@dataclass
class MsWeatherTemperatureColumn(ScalarColumn):
    comment: str = "Ambient Air Temperature for an antenna"
    valueType: str = "float"
    keywords: dict = field(default_factory=lambda: {"QuantumUnits": np.array(["K"])})


@dataclass
class MsWeatherTemperatureFlagColumn(ScalarColumn):
    comment: str = "Flag for ambient air temperature for an antenna"
    valueType: str = "bool"


@dataclass
class MsWeatherDewPointColumn(ScalarColumn):
    comment: str = "Dew point"
    valueType: str = "float"
    keywords: dict = field(default_factory=lambda: {"QuantumUnits": np.array(["K"])})


@dataclass
class MsWeatherDewPointFlagColumn(ScalarColumn):
    comment: str = "Flag for dew point"
    valueType: str = "bool"


@dataclass
class MsWeatherWindDirectionColumn(ScalarColumn):
    comment: str = "Average wind direction"
    valueType: str = "float"
    keywords: dict = field(default_factory=lambda: {"QuantumUnits": np.array(["rad"])})


@dataclass
class MsWeatherWindDirectionFlagColumn(ScalarColumn):
    comment: str = "Flag for wind direction"
    valueType: str = "bool"


@dataclass
class MsWeatherWindSpeedColumn(ScalarColumn):
    comment: str = "Average wind speed"
    valueType: str = "float"
    keywords: dict = field(default_factory=lambda: {"QuantumUnits": np.array(["m/s"])})


@dataclass
class MsWeatherWindSpeedFlagColumn(ScalarColumn):
    comment: str = "Flag for wind speed"
    valueType: str = "bool"


@dataclass
class MsWeatherStationIdColumn(ScalarColumn):
    comment: str = "An identifier to identify uniquely a weather station"
    valueType: str = "int"


@dataclass
class MsWeatherStationPositionColumn(ArrayColumn):
    comment: str = "The position of the station"
    ndim: int = 1
    shape: npt.NDArray = field(default_factory=lambda: np.array([3]))
    valueType: str = "double"


@dataclass
class MsWeatherTableColumnDescription(ColumnDescription):
    ANTENNA_ID: MsWeatherAntennaIdColumn
    INTERVAL: MsWeatherIntervalColumn
    TIME: MsWeatherTimeColumn
    PRESSURE: MsWeatherPressureColumn
    PRESSURE_FLAG: MsWeatherPressureFlagColumn
    REL_HUMIDITY: MsWeatherRelHumidityColumn
    REL_HUMIDITY_FLAG: MsWeatherRelHumidityFlagColumn
    TEMPERATURE: MsWeatherTemperatureColumn
    TEMPERATURE_FLAG: MsWeatherTemperatureFlagColumn
    DEW_POINT: MsWeatherDewPointColumn
    DEW_POINT_FLAG: MsWeatherDewPointFlagColumn
    WIND_DIRECTION: MsWeatherWindDirectionColumn
    WIND_DIRECTION_FLAG: MsWeatherWindDirectionFlagColumn
    WIND_SPEED: MsWeatherWindSpeedColumn
    WIND_SPEED_FLAG: MsWeatherWindSpeedFlagColumn
    NS_WX_STATION_ID: MsWeatherStationIdColumn
    NS_WX_STATION_POSITION: MsWeatherStationPositionColumn


@dataclass
class MsWeatherTable(Table):
    coldesc: MsWeatherTableColumnDescription
