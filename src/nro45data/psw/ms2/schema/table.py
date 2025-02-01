from dataclasses import asdict, fields


class Table:
    @classmethod
    def as_dict(cls):
        return dict((f.name, asdict(f.type())) for f in fields(cls))
