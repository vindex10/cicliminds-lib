from collections import namedtuple

import numpy as np
from matplotlib import cm
import xhistogram.xarray as xh

from cicliminds_lib.utils import patch_config

from cicliminds_lib.bindings import cdo_fldmean_from_data

from cicliminds_lib.plotting.config import RecipeConfig
from cicliminds_lib.plotting.elements import get_mean
from cicliminds_lib.plotting._helpers import _standardize_data
from cicliminds_lib.plotting._helpers import _generate_timeslices
from cicliminds_lib.plotting._helpers import _get_histogram_params
from cicliminds_lib.plotting._helpers import _configure_axes
from cicliminds_lib.plotting._helpers import _get_year_label


def plot_means_of_hists(ax, val, query):
    default_cfg = get_means_of_hists_config(val.name)
    cfg = patch_config(default_cfg, query)
    val = _standardize_data(val, cfg)
    timeslices = _generate_timeslices(val, cfg)
    _, timeslice = next(timeslices)
    bins, x, widths = _get_histogram_params(val, cfg.binsize)
    hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time"], density=cfg.normalize_histograms)
    mean = get_mean(hist)
    ax.bar(x, mean.values.ravel(), widths, label=_get_year_label(cfg, timeslice))
    cmap = cm.get_cmap(cfg.colormap)
    for intensity, timeslice in timeslices:
        hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time"], density=cfg.normalize_histograms)
        means = cdo_fldmean_from_data(hist).values[0, 0]
        ax.stairs(means, bins, label=_get_year_label(cfg, timeslice), color=cmap(intensity))
    _configure_axes(ax, cfg)


def plot_means_of_hists_diff(ax, val, query):
    default_cfg = get_means_of_hists_config(val.name)
    cfg = patch_config(default_cfg, query)
    val = _standardize_data(val, cfg)
    timeslices = _generate_timeslices(val, cfg)
    _, timeslice = next(timeslices)
    bins, _, _ = _get_histogram_params(val.isel(time=timeslice), cfg.binsize)
    hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time"])
    ref_mean = get_mean(hist)
    cmap = cm.get_cmap(cfg.colormap)
    for intensity, timeslice in timeslices:
        hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time"])
        mean = cdo_fldmean_from_data(hist) - ref_mean
        ax.stairs(mean.values[0, 0], bins, label=_get_year_label(cfg, timeslice), color=cmap(intensity))
    _configure_axes(ax, cfg)
    ax.set_yscale("linear")


def get_means_of_hists_config(index_name):
    default_index_cfg = MEANS_OF_HISTS_VIZ_DEFAULTS[index_name]
    return RecipeConfig(**default_index_cfg._asdict())


_cfg_format = namedtuple("MEANS_OF_HISTS_VIZ_DEFAULTS_ROW", ("unit", "unit_factor", "binsize", "yscale"))
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
