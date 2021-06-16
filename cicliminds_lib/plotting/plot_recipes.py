from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy.crs as ccrs
import xhistogram.xarray as xh

from cicliminds_lib.bindings.cdo import cdo_gridweights_from_data
from cicliminds_lib.bindings.cdo import cdo_fldmean_from_data

from cicliminds_lib.plotting.configs import MEANS_OF_HISTS_VIZ_CFG
from cicliminds_lib.plotting.configs import HISTS_OF_MEANS_VIZ_CFG
from cicliminds_lib.plotting.configs import COLORMAP
from cicliminds_lib.plotting.elements import get_mean
from cicliminds_lib.plotting.elements import get_spreads
from cicliminds_lib.plotting._helpers import _standardize_data
from cicliminds_lib.plotting._helpers import _generate_timeslices
from cicliminds_lib.plotting._helpers import _get_histogram_params
from cicliminds_lib.plotting._helpers import _configure_axes


def plot_median_idx(ax, dat, idx, scale=1):
    val = dat[idx].median(dim=["lon", "lat"])/scale
    is_yr = dat.frequency == "yr"
    time_scale = 60*60*24*1E9 * (365 if is_yr else 1)
    time_origin = np.datetime64(datetime.strptime(dat.time.time_origin, "%Y-%m-%d %H:%M:%S"))
    origin_year = (time_origin.astype('object').year if is_yr else 0)  # pylint: disable=no-member
    time_range = (dat.time.values - time_origin)/time_scale
    time = origin_year + time_range
    ax.plot(time, val)
    print(dat[idx].long_name)
    ax.set_title(idx)


def plot_spatial_idx_at_t(ax, dat, idx, t, scale=1):
    val = dat[idx].sel(time=t)/scale
    # mesh_lon, mesh_lat = np.meshgrid(val.lon, val.lat)
    # ax.contourf(mesh_lon, mesh_lat, val, transform=ccrs.PlateCarree())
    val.plot(ax=ax, transform=ccrs.PlateCarree(), cbar_kwargs={"shrink": 0.5})
    print(dat[idx].long_name)
    ax.set_title(f"time: {t}")


def plot_idx_value(dat, idx):
    ax = plt.axes(projection=ccrs.Robinson())
    ax.coastlines()
    ax.stock_img()
    ax.set_global()
    plot_spatial_idx_at_t(ax, dat, idx, t=dat.time.values[0], scale=np.timedelta64(1, 'D'))
    plt.show()
    plt.close()


def plot_mean(ax, mean, x, widths, timeslice):
    ax.bar(x, mean.values.ravel(), widths, label=f"{timeslice.start}-{timeslice.stop}")


def plot_spreads(ax, spreads, x, widths):
    lower_edge, upper_edge = spreads[0].values.ravel(), spreads[1].values.ravel()
    ax.fill_between(x - widths/2, lower_edge, upper_edge, color="#eee", label="min-max", step="post")


def plot_means_of_hists(ax, val):
    cfg = MEANS_OF_HISTS_VIZ_CFG[val.name]
    val = _standardize_data(val, cfg)
    timeslices = _generate_timeslices(val)
    _, timeslice = next(timeslices)
    bins, x, widths = _get_histogram_params(val.isel(time=timeslice), cfg.binsize)
    hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time"])
    mean = get_mean(hist)
    plot_mean(ax, mean, x, widths, timeslice)
    if cfg.yscale == "log":
        spreads = get_spreads(hist)
        plot_spreads(ax, spreads, x, widths)
    cmap = cm.get_cmap(COLORMAP)
    for intensity, timeslice in timeslices:
        hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time"])
        means = cdo_fldmean_from_data(hist).values[0, 0]
        ax.stairs(means, bins, label=f"{timeslice.start}-{timeslice.stop}", color=cmap(intensity))
    _configure_axes(ax, cfg, "fldmean last")


def plot_means_of_hists_diff(ax, val):
    cfg = MEANS_OF_HISTS_VIZ_CFG[val.name]
    val = _standardize_data(val, cfg)
    timeslices = _generate_timeslices(val)
    _, timeslice = next(timeslices)
    bins, _, _ = _get_histogram_params(val.isel(time=timeslice), cfg.binsize)
    hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time"])
    ref_mean = get_mean(hist)
    cmap = cm.get_cmap(COLORMAP)
    for intensity, timeslice in timeslices:
        hist = xh.histogram(val.isel(time=timeslice), bins=[bins], dim=["time"])
        mean = cdo_fldmean_from_data(hist) - ref_mean
        ax.stairs(mean.values[0, 0], bins, label=f"{timeslice.start}-{timeslice.stop}", color=cmap(intensity))
    _configure_axes(ax, cfg, "fldmean last, refdiff")
    ax.set_yscale("linear")


def plot_hists_of_means(ax, val):
    cfg = HISTS_OF_MEANS_VIZ_CFG[val.name]
    val = _standardize_data(val, cfg)
    mean = get_mean(val)
    timeslices = _generate_timeslices(mean)
    _, timeslice = next(timeslices)
    bins, x, widths = _get_histogram_params(mean.isel(time=timeslice), cfg.binsize)
    hist = xh.histogram(mean.isel(time=timeslice), bins=[bins], dim=None)  # dim=None to flatten the variable
    plot_mean(ax, hist, x, widths, timeslice)
    cmap = cm.get_cmap(COLORMAP)
    for intensity, timeslice in timeslices:
        hist = xh.histogram(mean.isel(time=timeslice), bins=[bins], dim=None)  # dim=None to flatten the variable
        ax.stairs(hist, bins, label=f"{timeslice.start}-{timeslice.stop}", color=cmap(intensity))
    _configure_axes(ax, cfg, "fldmean first")


def plot_hists_of_means_diff(ax, val):
    cfg = HISTS_OF_MEANS_VIZ_CFG[val.name]
    val = _standardize_data(val, cfg)
    mean = get_mean(val)
    timeslices = _generate_timeslices(mean)
    _, timeslice = next(timeslices)
    bins, _, _ = _get_histogram_params(mean.isel(time=timeslice), cfg.binsize)
    ref_hist = xh.histogram(mean.isel(time=timeslice), bins=[bins], dim=None)  # dim=None to flatten the variable
    cmap = cm.get_cmap(COLORMAP)
    for intensity, timeslice in timeslices:
        hist = xh.histogram(mean.isel(time=timeslice), bins=[bins], dim=None)  # dim=None to flatten the variable
        ax.stairs(hist-ref_hist, bins, label=f"{timeslice.start}-{timeslice.stop}", color=cmap(intensity))
    _configure_axes(ax, cfg, "fldmean first, refdiff")
    ax.set_yscale("linear")


def plot_hist_of_timeavgs(ax, val):
    cfg = MEANS_OF_HISTS_VIZ_CFG[val.name]
    val = _standardize_data(val, cfg)
    weights = cdo_gridweights_from_data(val)
    timeslices = _generate_timeslices(val)
    _, timeslice = next(timeslices)
    mean = val.isel(time=timeslice).mean(dim=["time"])
    bins, x, widths = _get_histogram_params(mean, cfg.binsize)
    hist = xh.histogram(mean, bins=[bins], dim=["lat", "lon"], weights=weights)
    plot_mean(ax, hist, x, widths, timeslice)
    cmap = cm.get_cmap(COLORMAP)
    for intensity, timeslice in timeslices:
        mean = val.isel(time=timeslice).mean(dim=["time"])
        hist = xh.histogram(mean, bins=[bins], dim=["lat", "lon"], weights=weights)
        ax.stairs(hist, bins, label=f"{timeslice.start}-{timeslice.stop}", color=cmap(intensity))
    _configure_axes(ax, cfg, "fld hist, timeavg")


def plot_hist_of_timeavgs_diff(ax, val):
    cfg = MEANS_OF_HISTS_VIZ_CFG[val.name]
    val = _standardize_data(val, cfg)
    weights = cdo_gridweights_from_data(val)
    timeslices = _generate_timeslices(val)
    _, timeslice = next(timeslices)
    mean = val.isel(time=timeslice).mean(dim=["time"])
    bins, _, _ = _get_histogram_params(mean, cfg.binsize)
    ref_hist = xh.histogram(mean, bins=[bins], dim=["lat", "lon"], weights=weights)
    cmap = cm.get_cmap(COLORMAP)
    for intensity, timeslice in timeslices:
        mean = val.isel(time=timeslice).mean(dim=["time"])
        hist = xh.histogram(mean, bins=[bins], dim=["lat", "lon"], weights=weights)
        ax.stairs(hist - ref_hist, bins, label=f"{timeslice.start}-{timeslice.stop}", color=cmap(intensity))
    _configure_axes(ax, cfg, "fld hist, timeavg, refdiff")
    ax.set_yscale("linear")
