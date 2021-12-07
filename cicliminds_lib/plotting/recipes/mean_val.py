from itertools import chain

import numpy as np
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes

from cicliminds_lib.utils import patch_config
from cicliminds_lib.math import xr_weighted_median
from cicliminds_lib.unify.model_weights.normalize import align_model_weights_with_dataarray
from cicliminds_lib.unify.model_weights.normalize import density_model_weights
from cicliminds_lib.plotting.recipes.means_of_hists import MeansOfHistsRecipe
from cicliminds_lib.plotting.recipes.means_of_hists import MeansOfHistsDiffRecipe
from cicliminds_lib.plotting._helpers import _standardize_data
from cicliminds_lib.plotting._helpers import _get_variable_name


MAP_PROJECTION = ccrs.Mollweide()


class MeanValRecipe:
    @classmethod
    def plot(cls, ax, query, inputs):
        dataset = inputs["datasets"]
        variable = _get_variable_name(dataset)
        val = dataset[variable]
        default_cfg = cls.get_default_config(variable)
        cfg = patch_config(default_cfg, query)
        val = _standardize_data(val, cfg)
        val_mean = val.isel(time=slice(-cfg.sliding_window_size, None)).mean(dim=["time"])
        scenario_median = val_mean.median(dim=["scenario"])
        model_weights = None
        if inputs["model_weights"] is not None:
            model_weights = align_model_weights_with_dataarray(inputs["model_weights"], scenario_median)
            model_weights = density_model_weights(model_weights)
        model_median = xr_weighted_median(scenario_median, model_weights, "model")
        cmap = cm.get_cmap(cfg.colormap)
        ccrs_ax = inset_axes(ax, width="100%", height="100%",
                             axes_class=GeoAxes,
                             axes_kwargs={"map_projection": MAP_PROJECTION},
                             borderpad=0)
        ccrs_ax.stock_img()
        ccrs_ax.coastlines()
        lon_grid, lat_grid = np.meshgrid(model_median.lon, model_median.lat)
        heatmap = ccrs_ax.pcolormesh(lon_grid, lat_grid, model_median.data, transform=ccrs.PlateCarree(), cmap=cmap)
        ccrs_ax.set_xticks([])
        ccrs_ax.set_yticks([])
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in chain(ax.spines.values(), ccrs_ax.spines.values()):
            spine.set_visible(False)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.05)
        ccrs_ax.figure.colorbar(heatmap, cax=cax, label=f"{cfg.unit}")

    @staticmethod
    def get_default_config(index_name):
        res = MeansOfHistsRecipe.get_default_config(index_name)
        if res.unit == "degrees_C":
            res.colormap = "afmhot"
        return res


class MeanValDiffRecipe:
    @classmethod
    def plot(cls, ax, query, inputs):
        dataset = inputs["datasets"]
        variable = _get_variable_name(dataset)
        val = dataset[variable]
        default_cfg = cls.get_default_config(variable)
        cfg = patch_config(default_cfg, query)
        val = _standardize_data(val, cfg)
        val_mean = val.isel(time=slice(-cfg.sliding_window_size, None)).mean(dim=["time"])
        ref_mean = val.isel(time=slice(None, cfg.reference_window_size)).mean(dim=["time"])
        mean_diff = val_mean - ref_mean
        scenario_median = mean_diff.median(dim=["scenario"])
        model_weights = None
        if inputs["model_weights"] is not None:
            model_weights = align_model_weights_with_dataarray(inputs["model_weights"], scenario_median)
            model_weights = density_model_weights(model_weights)
        model_median = xr_weighted_median(scenario_median, model_weights, "model")
        cmap = cm.get_cmap(cfg.colormap)
        ccrs_ax = inset_axes(ax, width="100%", height="100%",
                             axes_class=GeoAxes,
                             axes_kwargs={"map_projection": MAP_PROJECTION},
                             borderpad=0)
        ccrs_ax.stock_img()
        ccrs_ax.coastlines()
        lon_grid, lat_grid = np.meshgrid(model_median.lon, model_median.lat)
        heatmap = ccrs_ax.pcolormesh(lon_grid, lat_grid, model_median.data, transform=ccrs.PlateCarree(), cmap=cmap)
        ccrs_ax.set_xticks([])
        ccrs_ax.set_yticks([])
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in chain(ax.spines.values(), ccrs_ax.spines.values()):
            spine.set_visible(False)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.05)
        ccrs_ax.figure.colorbar(heatmap, cax=cax, label=f"{cfg.unit}")

    @staticmethod
    def get_default_config(index_name):
        res = MeansOfHistsDiffRecipe.get_default_config(index_name)
        if res.unit == "degrees_C":
            res.colormap = "afmhot"
        return res
