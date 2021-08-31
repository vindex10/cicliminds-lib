import os
from dataclasses import dataclass
from dataclasses import fields


@dataclass
class Config:
    cdo_executable: str = "cdo"


CFG = Config()


def update_from_env():
    for field in fields(CFG):
        var_name = f"CICLIMINDS_LIB_{field.name.upper()}"
        try:
            value = os.environ[var_name]
            setattr(CFG, field.name, value)
        except KeyError:
            pass


update_from_env()
