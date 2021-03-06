from collections import namedtuple

import numpy as np
from matplotlib import cm
import xhistogram.xarray as xh

from cicliminds_lib.utils import patch_config

from cicliminds_lib.bindings import cdo_fldmean_from_data

from cicliminds_lib.unify.model_weights.normalize import align_model_weights_with_dataarray
from cicliminds_lib.unify.model_weights.normalize import density_model_weights

from cicliminds_lib.plotting.config import RecipeConfig
from cicliminds_lib.plotting._helpers import _standardize_data
from cicliminds_lib.plotting._helpers import _generate_timeslices
from cicliminds_lib.plotting._helpers import _get_histogram_params
from cicliminds_lib.plotting._helpers import _configure_axes
from cicliminds_lib.plotting._helpers import _get_year_label
from cicliminds_lib.plotting._helpers import _get_variable_name
from cicliminds_lib.plotting._helpers import get_smooth_hist
from cicliminds_lib.plotting._helpers import get_smooth_hist_normalized


class MeansOfHistsRecipe:
    @classmethod
    def plot(cls, ax, query, inputs):
        dataset = inputs["datasets"]
        variable = _get_variable_name(dataset)
        val = dataset[variable]
        default_cfg = cls.get_default_config(variable)
        cfg = patch_config(default_cfg, query)
        val = _standardize_data(val, cfg)
        timeslices = _generate_timeslices(val, cfg)
        _, timeslice = next(timeslices)
        bins, x, widths = _get_histogram_params(val, binsize=cfg.binsize, bincount=cfg.bincount)
        model_weights = None
        if inputs["model_weights"] is not None:
            model_weights = align_model_weights_with_dataarray(inputs["model_weights"], val.isel(time=timeslice))
            model_weights = density_model_weights(model_weights)
        hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time", "model", "scenario"],
                            density=cfg.normalize_histograms, weights=model_weights)
        smoother = get_smooth_hist if not cfg.normalize_histograms else get_smooth_hist_normalized
        mean_hist = cdo_fldmean_from_data(hist)
        mean = np.float64((mean_hist*x).sum()/mean_hist.sum())
        std = np.float64(((x**2*mean_hist).sum()/mean_hist.sum() - mean**2))
        label = _get_year_label(cfg, timeslice) + f" [{mean:.2f}, {std:.2f}]"
        smooth_xs = np.linspace(bins[0], bins[-1], len(bins)*10)
        smooth_hist = smoother(mean_hist.values.ravel(), bins)
        ax.fill_between(smooth_xs, smooth_hist(smooth_xs),
                        label=label, color="gray", alpha=0.4)
        cmap = cm.get_cmap(cfg.colormap)
        for intensity, timeslice in timeslices:
            model_weights = None
            if inputs["model_weights"] is not None:
                model_weights = align_model_weights_with_dataarray(inputs["model_weights"], val.isel(time=timeslice))
                model_weights = density_model_weights(model_weights)
            hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time", "model", "scenario"],
                                density=cfg.normalize_histograms, weights=model_weights)
            mean_hists = cdo_fldmean_from_data(hist).values[0, 0]
            mean = (mean_hists*x).sum()/mean_hists.sum()
            std = (x**2*mean_hists).sum()/mean_hists.sum() - mean**2
            label = _get_year_label(cfg, timeslice) + f" [{mean:.2f}, {std:.2f}]"
            smooth_hist = smoother(mean_hists, bins)
            ax.plot(smooth_xs, smooth_hist(smooth_xs), label=label, color=cmap(intensity))
        _configure_axes(ax, cfg)

    @staticmethod
    def get_default_config(index_name):
        default_index_cfg = MEANS_OF_HISTS_VIZ_DEFAULTS[index_name]
        return RecipeConfig(**default_index_cfg._asdict())


class MeansOfHistsDiffRecipe:
    @classmethod
    def plot(cls, ax, query, inputs):
        dataset = inputs["datasets"]
        variable = _get_variable_name(dataset)
        val = dataset[variable]
        default_cfg = cls.get_default_config(variable)
        cfg = patch_config(default_cfg, query)
        val = _standardize_data(val, cfg)
        timeslices = _generate_timeslices(val, cfg)
        _, timeslice = next(timeslices)
        bins, _, _ = _get_histogram_params(val.isel(time=timeslice), binsize=cfg.binsize, bincount=cfg.bincount)
        model_weights = None
        if inputs["model_weights"] is not None:
            model_weights = align_model_weights_with_dataarray(inputs["model_weights"], val.isel(time=timeslice))
            model_weights = density_model_weights(model_weights)
        hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time", "model", "scenario"],
                            density=cfg.normalize_histograms, weights=model_weights)
        ref_mean = cdo_fldmean_from_data(hist)
        cmap = cm.get_cmap(cfg.colormap)
        smoother = get_smooth_hist if not cfg.normalize_histograms else get_smooth_hist_normalized
        smooth_xs = np.linspace(bins[0], bins[-1], len(bins)*10)
        for intensity, timeslice in timeslices:
            model_weights = None
            if inputs["model_weights"] is not None:
                model_weights = align_model_weights_with_dataarray(inputs["model_weights"], val.isel(time=timeslice))
                model_weights = density_model_weights(model_weights)
            hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time", "model", "scenario"],
                                density=cfg.normalize_histograms, weights=model_weights)
            mean = cdo_fldmean_from_data(hist) - ref_mean
            smooth_hist = smoother(mean.values[0, 0], bins)
            ax.plot(smooth_xs, smooth_hist(smooth_xs), label=_get_year_label(cfg, timeslice), color=cmap(intensity))
        _configure_axes(ax, cfg)
        ax.set_yscale("linear")

    @staticmethod
    def get_default_config(index_name):
        default_index_cfg = MEANS_OF_HISTS_VIZ_DEFAULTS[index_name]
        res = RecipeConfig(**default_index_cfg._asdict())
        res.yscale = "linear"
        return res


_cfg_format = namedtuple("MEANS_OF_HISTS_VIZ_DEFAULTS_ROW", ("unit", "unit_factor", "binsize", "yscale"))
MEANS_OF_HISTS_VIZ_DEFAULTS = {
    "altcddETCCDI": _cfg_format("days", 1, 7, "log"),
    "altcsdiETCCDI": _cfg_format("days", 1, 7, "log"),
    "altcwdETCCDI": _cfg_format("days", 1, 7, "log"),
    "altwsdiETCCDI": _cfg_format("days", 1, 7, "log"),
    "cddETCCDI": _cfg_format("days", 1, 90, "log"),
    "csdiETCCDI": _cfg_format("days", 1, 7, "log"),
    "cwdETCCDI": _cfg_format("days", 1, 7, "log"),
    "fdETCCDI": _cfg_format("days", 1, 7, "log"),
    "idETCCDI": _cfg_format("days", 1, 7, "log"),
    "gslETCCDI": _cfg_format("days", 1, 7, "log"),
    "r10mmETCCDI": _cfg_format("days", 1, 7, "log"),
    "r1mmETCCDI": _cfg_format("days", 1, 7, "log"),
    "r20mmETCCDI": _cfg_format("days", 1, 7, "log"),
    "suETCCDI": _cfg_format("days", 1, 7, "log"),
    "trETCCDI": _cfg_format("days", 1, 7, "log"),
    "wsdiETCCDI": _cfg_format("days", 1, 7, "log"),
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
