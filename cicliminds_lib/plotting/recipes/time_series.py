from itertools import chain

import numpy as np
from matplotlib import cm

from cicliminds_lib.utils import patch_config
from cicliminds_lib.bindings import FLOAT_MISSING_VALUE
from cicliminds_lib.bindings import nco_fldmean_from_data
from cicliminds_lib.plotting.recipes.means_of_hists import MeansOfHistsRecipe
from cicliminds_lib.plotting.recipes.means_of_hists import MeansOfHistsDiffRecipe
from cicliminds_lib.plotting._helpers import _standardize_data
from cicliminds_lib.plotting._helpers import _configure_axes
from cicliminds_lib.plotting._helpers import _get_year_label
from cicliminds_lib.plotting._helpers import _get_variable_name


class TimeSeriesRecipe:
    @classmethod
    def plot(cls, ax, dataset, query):
        variable = _get_variable_name(dataset)
        val = dataset[variable]
        default_cfg = cls.get_default_config(variable)
        cfg = patch_config(default_cfg, query)
        val = _standardize_data(val, cfg)
        val = val.fillna(FLOAT_MISSING_VALUE)
        val.attrs["_FillValue"] = FLOAT_MISSING_VALUE
        fldmeaned = nco_fldmean_from_data(val, ["lon", "lat"])
        smoothed = fldmeaned.rolling(dim={"time": 20}, center=True).mean()
        model_median = smoothed.median(dim=["model"])
        model_lower = smoothed.quantile(0.25, dim=["model"])
        model_upper = smoothed.quantile(0.75, dim=["model"])
        cmap = cm.get_cmap(cfg.colormap)
        for i, scenario in enumerate(model_median["scenario"].data):
            intensity = (i+1)/model_median["scenario"].shape[0]
            dataset_lower = model_lower.sel(scenario=scenario)
            dataset_upper = model_upper.sel(scenario=scenario)
            ax.fill_between(dataset["time"].data, dataset_lower.data, dataset_upper.data, color=cmap(intensity), alpha=0.4, zorder=2*i)
            dataset = model_median.sel(scenario=scenario)
            ax.plot(dataset["time"].data, dataset.data, color=cmap(intensity), label=f"{scenario}", zorder=2*i+1)
        ax.legend()
        ax.set_xlabel("year")
        ax.set_ylabel(f"{cfg.unit}")
        xticks = ax.get_xticks()
        years = [str(int(xtick)//360 + 1800) for xtick in xticks]
        ax.set_xticklabels(years)

    @staticmethod
    def get_default_config(index_name):
        return MeansOfHistsRecipe.get_default_config(index_name)


class TimeSeriesDiffRecipe:
    @classmethod
    def plot(cls, ax, dataset, query):
        variable = _get_variable_name(dataset)
        val = dataset[variable]
        default_cfg = cls.get_default_config(variable)
        cfg = patch_config(default_cfg, query)
        val = _standardize_data(val, cfg)
        ref_mean = val.isel(time=slice(0, cfg.reference_window_size)).mean(dim=["time"])
        val = val - ref_mean
        val = val.fillna(FLOAT_MISSING_VALUE)
        val.attrs["_FillValue"] = FLOAT_MISSING_VALUE
        fldmeaned = nco_fldmean_from_data(val, ["lon", "lat"])
        smoothed = fldmeaned.rolling(dim={"time": 20}, center=True).mean()
        model_median = smoothed.median(dim=["model"])
        model_lower = smoothed.quantile(0.25, dim=["model"])
        model_upper = smoothed.quantile(0.75, dim=["model"])
        cmap = cm.get_cmap(cfg.colormap)
        for i, scenario in enumerate(model_median["scenario"].data):
            intensity = (i+1)/model_median["scenario"].shape[0]
            dataset_lower = model_lower.sel(scenario=scenario)
            dataset_upper = model_upper.sel(scenario=scenario)
            ax.fill_between(dataset["time"].data, dataset_lower.data, dataset_upper.data, color=cmap(intensity), alpha=0.4, zorder=2*i)
            dataset = model_median.sel(scenario=scenario)
            ax.plot(dataset["time"].data, dataset.data, color=cmap(intensity), label=f"{scenario}", zorder=2*i+1)
        ax.legend()
        ax.set_xlabel("year")
        ax.set_ylabel(f"{cfg.unit}")
        xticks = ax.get_xticks()
        years = [str(int(xtick)//360 + 1800) for xtick in xticks]
        ax.set_xticklabels(years)

    @staticmethod
    def get_default_config(index_name):
        return MeansOfHistsDiffRecipe.get_default_config(index_name)
