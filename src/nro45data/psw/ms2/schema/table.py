from dataclasses import dataclass, fields


def _as_dict(obj):
    if obj is dict:
        return obj()
    if hasattr(obj, 'as_dict'):
        return obj.as_dict()
    else:
        return obj.__dict__


@dataclass
class Table:
    coldesc: dict
    dminfo: dict

    @classmethod
    def as_dict(cls):
        return dict(
            (f.name, _as_dict(f.type)) for f in fields(cls)
        )
