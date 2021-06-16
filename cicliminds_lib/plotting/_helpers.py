import numpy as np

from cicliminds_lib.plotting.configs import TIME_WINDOW_STEP
from cicliminds_lib.plotting.configs import TIME_WINDOW_SIZE


def _infer_hist_bins(vals, binsize):
    # min_val = np.min(vals)
    # max_val = np.max(vals)
    min_val = np.nanquantile(vals, 0.00001)
    max_val = np.nanquantile(vals, 0.99999)

    left_edge = np.floor(min_val)
    right_edge = ((max_val - left_edge)//binsize)*binsize + left_edge

    return np.arange(left_edge, right_edge, binsize)


def _generate_timeslices(val):
    size = len(val.time)
    for start in range(0, size-TIME_WINDOW_SIZE, TIME_WINDOW_STEP):
        intensity = start/size
        yield intensity, slice(start, start+TIME_WINDOW_SIZE)


def _configure_axes(ax, cfg, title):
    ax.set_title(title)
    ax.set_xlabel(f"{cfg.unit}, binsize={cfg.binsize}")
    ax.set_ylabel("N")
    ax.set_yscale(cfg.yscale)
    ax.legend()


def _standardize_data(val, cfg):
    scale = cfg.unit_factor
    val = val/scale
    return val


def _get_histogram_params(val, binsize):
    bins = _infer_hist_bins(val, binsize)
    x = (bins[1:] + bins[:-1])/2
    widths = bins[1:] - bins[:-1]
    return bins, x, widths
