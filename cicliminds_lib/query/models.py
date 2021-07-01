import logging

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


def list_model_configurations(datasets):
    all_indices_count = datasets.variable.unique().shape[0]
    res = []
    for params, data in datasets.reset_index()\
                                .assign(init_params_trunc=lambda x: [i[:-1] for i in x["init_params"]]) \
                                .groupby(["model", "scenario", "frequency", "init_params_trunc"]):
        model, scenario, frequency, _ = params
        all_indices = _has_all_indices(data, all_indices_count)
        init_params, init_params_non_uniform = _get_init_params(data)
        timespan, timespan_non_uniform = _get_timespan(data)
        res.append({"model": model,
                    "scenario": scenario,
                    "all_indices": all_indices,
                    "init_params": init_params,
                    "init_params_non_uniform": init_params_non_uniform,
                    "frequency": frequency,
                    "timespan": timespan,
                    "timespan_non_uniform": timespan_non_uniform})
    res = pd.DataFrame.from_records(res)
    _check_insanity_and_clean(res, "init_params_non_uniform")
    _check_insanity_and_clean(res, "timespan_non_uniform")
    return res


def _has_all_indices(data, all_indices_count):
    var_num = data["variable"].unique().shape[0]
    all_indices = var_num == all_indices_count
    return all_indices


def _get_init_params(data):
    init_params_non_uniform = data["init_params"].unique().shape[0] > 1
    init_params = data["init_params"].values[0] \
        if not init_params_non_uniform \
        else data["init_params_trunc"].values[0]
    return init_params, init_params_non_uniform


def _get_timespan(data):
    timespans = data["timespan"].unique()
    timespan_non_uniform = timespans.shape[0] > 1
    timespan = timespans[0]
    return timespan, timespan_non_uniform


def _check_insanity_and_clean(data, col):
    is_insane = np.any(data[col])
    if not is_insane:
        logger.info("%s: %s", col, is_insane)
        del data[col]
