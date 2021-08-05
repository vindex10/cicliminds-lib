from collections import namedtuple

import numpy as np
from matplotlib import cm
import xhistogram.xarray as xh

from cicliminds_lib.utils import patch_config

from cicliminds_lib.plotting.config import RecipeConfig
from cicliminds_lib.plotting.elements import get_mean
from cicliminds_lib.plotting._helpers import _standardize_data
from cicliminds_lib.plotting._helpers import _generate_timeslices
from cicliminds_lib.plotting._helpers import _get_histogram_params
from cicliminds_lib.plotting._helpers import _configure_axes
from cicliminds_lib.plotting._helpers import _get_year_label


class HistsOfMeansRecipe:
    @classmethod
    def plot(cls, ax, val, query):
        default_cfg = cls.get_default_config(val.name)
        cfg = patch_config(default_cfg, query)
        val = _standardize_data(val, cfg)
        mean = get_mean(val)
        timeslices = _generate_timeslices(mean, cfg)
        _, timeslice = next(timeslices)
        bins, x, widths = _get_histogram_params(mean.isel(time=timeslice), cfg.binsize)
        hist = xh.histogram(mean.isel(time=timeslice), bins=[bins], dim=None)  # dim=None to flatten the variable
        ax.bar(x, hist.values.ravel(), widths, label=_get_year_label(cfg, timeslice))
        cmap = cm.get_cmap(cfg.colormap)
        for intensity, timeslice in timeslices:
            hist = xh.histogram(mean.isel(time=timeslice), bins=[bins], dim=None)  # dim=None to flatten the variable
            ax.stairs(hist, bins, label=_get_year_label(cfg, timeslice), color=cmap(intensity))
        _configure_axes(ax, cfg)

    @staticmethod
    def get_default_config(index_name):
        default_index_cfg = HISTS_OF_MEANS_VIZ_DEFAULTS[index_name]
        return RecipeConfig(**default_index_cfg._asdict())


class HistsOfMeansDiffRecipe:
    @classmethod
    def plot(cls, ax, val, query):
        default_cfg = cls.get_default_config(val.name)
        cfg = patch_config(default_cfg, query)
        val = _standardize_data(val, cfg)
        mean = get_mean(val)
        timeslices = _generate_timeslices(mean, cfg)
        _, timeslice = next(timeslices)
        bins, _, _ = _get_histogram_params(mean.isel(time=timeslice), cfg.binsize)
        ref_hist = xh.histogram(mean.isel(time=timeslice), bins=[bins], dim=None)  # dim=None to flatten the variable
        cmap = cm.get_cmap(cfg.colormap)
        for intensity, timeslice in timeslices:
            hist = xh.histogram(mean.isel(time=timeslice), bins=[bins], dim=None)  # dim=None to flatten the variable
            ax.stairs(hist-ref_hist, bins, label=_get_year_label(cfg, timeslice), color=cmap(intensity))
        _configure_axes(ax, cfg)
        ax.set_yscale("linear")

    @staticmethod
    def get_default_config(index_name):
        default_index_cfg = HISTS_OF_MEANS_VIZ_DEFAULTS[index_name]
        res = RecipeConfig(**default_index_cfg._asdict())
        res.yscale = "linear"
        return res


_cfg_format = namedtuple("HISTS_OF_MEANS_VIZ_DEFAULTS_ROW", ("unit", "unit_factor", "binsize", "yscale"))
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
