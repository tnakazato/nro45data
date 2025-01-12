from dataclasses import dataclass, field


@dataclass
class DataManagerInfoItem:
    SEQNR: int
    COLUMNS: list[str] = field(default_factory=list)
    NAME: str = 'StandardStMan'
    SPEC: dict = field(default_factory=dict)
    TYPE: str = 'StandardStMan'
