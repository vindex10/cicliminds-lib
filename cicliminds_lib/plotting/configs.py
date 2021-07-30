from collections import namedtuple
from dataclasses import dataclass
from typing import Optional

import numpy as np


DEFAULT_REFERENCE_WINDOW_SIZE = 50
DEFAULT_SLIDING_WINDOW_SIZE = 30
DEFAULT_SLIDE_STEP = 30
COLORMAP = "gist_rainbow"

_cfg_format = namedtuple("INDEX_PLOT_CONFIG", ("unit", "unit_factor", "binsize", "yscale"))

MEANS_OF_HISTS_VIZ_DEFAULTS = {
    "altcddETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "altcsdiETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "altcwdETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "altwsdiETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "cddETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 90, "log"),
    "csdiETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "cwdETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "fdETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "idETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "gslETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "r10mmETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "r1mmETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "r20mmETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "suETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "trETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "wsdiETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 7, "log"),
    "dtrETCCDI": _cfg_format("degrees_C", 1, 1, "linear"),
    "tnnETCCDI": _cfg_format("degrees_C", 1, 1, "linear"),
    "tnxETCCDI": _cfg_format("degrees_C", 1, 1, "linear"),
    "txnETCCDI": _cfg_format("degrees_C", 1, 1, "linear"),
    "txxETCCDI": _cfg_format("degrees_C", 1, 1, "linear"),
    "r95pETCCDI": _cfg_format("cm", 10, 5, "log"),
    "r99pETCCDI": _cfg_format("cm", 10, 5, "log"),
    "rx1dayETCCDI": _cfg_format("cm", 10, 5, "log"),
    "sdiiETCCDI": _cfg_format("mm", 1, 1, "linear"),
    "rx5dayETCCDI": _cfg_format("cm", 10, 5, "log"),
    "prcptotETCCDI": _cfg_format("cm", 10, 25, "log"),
    "tn10pETCCDI": _cfg_format("percents", 1, 1, "linear"),
    "tn90pETCCDI": _cfg_format("percents", 1, 1, "linear"),
    "tx10pETCCDI": _cfg_format("percents", 1, 1, "linear"),
    "tx90pETCCDI": _cfg_format("percents", 1, 1, "linear")
}

HISTS_OF_MEANS_VIZ_DEFAULTS = {
    "altcddETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 1, "linear"),
    "altcsdiETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 1, "linear"),
    "altcwdETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 0.2, "linear"),
    "altwsdiETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 0.5, "linear"),
    "cddETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 2, "linear"),
    "csdiETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 1, "linear"),
    "cwdETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 0.2, "linear"),
    "fdETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 0.5, "linear"),
    "idETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 0.5, "linear"),
    "gslETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 1, "linear"),
    "r10mmETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 0.1, "linear"),
    "r1mmETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 0.5, "linear"),
    "r20mmETCCDI": _cfg_format("hours", np.timedelta64(1, 'h'), 2, "linear"),
    "suETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 0.5, "linear"),
    "trETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 1, "linear"),
    "wsdiETCCDI": _cfg_format("days", np.timedelta64(1, 'D'), 0.5, "linear"),
    "dtrETCCDI": _cfg_format("degrees_C/10", 0.1, 0.2, "linear"),
    "tnnETCCDI": _cfg_format("degrees_C", 1, 0.2, "linear"),
    "tnxETCCDI": _cfg_format("degrees_C", 1, 0.1, "linear"),
    "txnETCCDI": _cfg_format("degrees_C", 1, 0.2, "linear"),
    "txxETCCDI": _cfg_format("degrees_C", 1, 0.1, "linear"),
    "r95pETCCDI": _cfg_format("cm", 10, 0.5, "linear"),
    "r99pETCCDI": _cfg_format("cm", 10, 0.1, "linear"),
    "rx1dayETCCDI": _cfg_format("mm", 1, 0.2, "linear"),
    "sdiiETCCDI": _cfg_format("mm/10", 0.1, 0.2, "linear"),
    "rx5dayETCCDI": _cfg_format("cm", 10, 0.05, "linear"),
    "prcptotETCCDI": _cfg_format("cm", 10, 0.5, "linear"),
    "tn10pETCCDI": _cfg_format("percents", 1, 1, "linear"),
    "tn90pETCCDI": _cfg_format("percents", 1, 0.5, "linear"),
    "tx10pETCCDI": _cfg_format("percents", 1, 0.5, "linear"),
    "tx90pETCCDI": _cfg_format("percents", 1, 0.5, "linear")
}


@dataclass
class RecipeConfig:
    unit: str
    unit_factor: float
    yscale: str
    binsize: Optional[float]
    bincount: Optional[float] = None
    reference_window_size: float = DEFAULT_REFERENCE_WINDOW_SIZE
    sliding_window_size: float = DEFAULT_SLIDING_WINDOW_SIZE
    slide_step: float = DEFAULT_SLIDE_STEP


def get_means_of_hists_config(index_name):
    default_index_cfg = MEANS_OF_HISTS_VIZ_DEFAULTS[index_name]
    return RecipeConfig(**default_index_cfg._asdict())

def get_hists_of_means_config(index_name):
    default_index_cfg = MEANS_OF_HISTS_VIZ_DEFAULTS[index_name]
    return RecipeConfig(**default_index_cfg._asdict())
