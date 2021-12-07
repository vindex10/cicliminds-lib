import numpy as np


def xr_weighted_median(data, weights, dim):
    return xr_weighted_quantile(0.5, data, weights, dim)


def xr_weighted_quantile(q, data, weights, dim):
    assert q > 0 and q < 1
    dim_idx = data.dims.index(dim)
    sorted_data_idx = data.argsort(axis=dim_idx)
    sorted_data_raw = np.take_along_axis(data.values, sorted_data_idx, axis=dim_idx)
    if weights is None:
        weights_vals = np.ones_like(sorted_data_raw)
    else:
        weights_vals = weights.values
    corresponding_weights_raw = np.take_along_axis(weights_vals, sorted_data_idx, axis=dim_idx)
    weights_cumsum = corresponding_weights_raw.cumsum(axis=dim_idx)
    mid = np.take_along_axis(weights_cumsum, np.zeros([1 for _ in data.shape], dtype=np.int32)-1, axis=dim_idx)*q
    mid_idx = np.argmax((weights_cumsum - mid) > 0, axis=dim_idx)
    mid_idx_extended = np.expand_dims(mid_idx, axis=dim_idx)
    data_mids_raw = np.take_along_axis(sorted_data_raw, mid_idx_extended, axis=dim_idx)
    res = data.copy().isel({dim: [0]})
    res.data = data_mids_raw
    return res.isel({dim: 0})
