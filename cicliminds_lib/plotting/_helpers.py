import numpy as np


COMMON_DATA_VARS = ["lon_bnds", "lat_bnds", "time_bnds"]


def _get_variable_name(dataset):
    variable = [i for i in dataset.data_vars.keys() if i not in COMMON_DATA_VARS]
    if len(variable) > 1:
        raise Exception("More than 1 variable in the dataset")
    return variable[0]


def _infer_hist_bins(vals, binsize, bincount):
    # min_val = np.min(vals)
    # max_val = np.max(vals)
    min_val = np.nanquantile(vals, 0.00001)
    max_val = np.nanquantile(vals, 0.99999)

    left_edge = np.floor(min_val)
    if bincount is not None:
        return np.linspace(left_edge, max_val, bincount)

    right_edge = ((max_val - left_edge)//binsize)*binsize + left_edge

    return np.arange(left_edge, right_edge, binsize)


def _generate_timeslices(val, cfg):
    size = len(val.time)
    yield 0, slice(0, cfg.reference_window_size)
    for start in range(cfg.reference_window_size, size-cfg.sliding_window_size, cfg.slide_step):
        intensity = start/size
        yield intensity, slice(start, start+cfg.sliding_window_size)


def _configure_axes(ax, cfg):
    ax.set_xlabel(f"{cfg.unit}, binsize={cfg.binsize}")
    ax.set_ylabel("N")
    ax.set_yscale(cfg.yscale)
    ax.legend()


def _standardize_data(val, cfg):
    scale = cfg.unit_factor
    val = val/scale
    return val


def _get_histogram_params(val, binsize=None, bincount=None):
    bins = _infer_hist_bins(val, binsize=binsize, bincount=bincount)
    x = (bins[1:] + bins[:-1])/2
    widths = bins[1:] - bins[:-1]
    return bins, x, widths


def _get_year_label(cfg, timeslice):
    start = cfg.init_year + timeslice.start
    stop = cfg.init_year + timeslice.stop
    return f"{start}-{stop}"
