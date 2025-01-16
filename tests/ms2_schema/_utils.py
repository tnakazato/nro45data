from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nro45data.psw.ms2._casa import _table


class ColumnDescriptionChecker:
    def __init__(self, tb: "_table", name: str):
        self.name: str = name
        self.desc: dict = tb.getcoldesc(name)
        self.kw: dict = self.desc.get("keywords", {})

    def is_array(self):
        return "ndim" in self.desc

    def is_var_array(self):
        return self.is_array() and self.get_ndim() == -1

    def is_scalar(self):
        return not self.is_array()

    def get_type(self):
        return self.desc["valueType"]

    def get_ndim(self):
        if self.is_array():
            return self.desc["ndim"]
        else:
            return None

    def get_shape(self):
        return self.desc.get("shape", None)

    def get_unit(self):
        return self.desc.get("QuantumUnit", None)

    def is_meas(self):
        return "MEASINFO" in self.kw

    def get_meas_type(self):
        return self.kw["MEASINFO"]["type"] if self.is_meas() is True else None

    def get_meas_ref(self):
        return self.kw["MEASINFO"]["Ref"] if self.is_meas() else None

    def get_meas_unit(self):
        return self.kw.get("QuantumUnits", None)

    def is_epoch_meas(self):
        return self.is_meas() and (self.get_meas_type() == "epoch")

    def is_direction_meas(self):
        return self.is_meas() and self.get_meas_type() == "direction"

    def is_position_meas(self):
        return self.is_meas() and self.get_meas_type() == "position"

    def is_uvw_meas(self):
        return self.is_meas() and self.get_meas_type() == "uvw"

    def is_frequency_meas(self):
        return self.is_meas() and self.get_meas_type() == "frequency"

    def is_velocity_meas(self):
        return self.is_meas() and self.get_meas_type() == "radialvelocity"



def get_checker(tb: "_table", name: str) -> ColumnDescriptionChecker:
    return ColumnDescriptionChecker(tb, name)
