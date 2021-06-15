import numpy as np
import pandas as pd
from cicliminds_lib.ui import display


def list_model_configurations(datasets):
    all_indices_count = datasets.variable.unique().shape[0]
    res = []
    for params, data in datasets.reset_index()\
                                .assign(init_params_trunc=lambda x: [i[:-1] for i in x["init_params"]]) \
                                .groupby(["model", "scenario", "frequency", "init_params_trunc"]):
        model, scenario, frequency, init_params_trunc = params
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
    timespan_froms = data["timespan_from"].unique().astype(np.int64)
    timespan_tos = data["timespan_to"].unique().astype(np.int64)
    timespan_from = np.max(timespan_froms)
    timespan_to = np.min(timespan_tos)
    timespan_non_uniform = np.any([(timespan_froms.shape[0] > 1), (timespan_tos.shape[0] > 1)])
    timespan = f"{timespan_from}-{timespan_to}"
    return timespan, timespan_non_uniform


def _check_insanity_and_clean(data, col):
    is_insane = np.any(data[col])
    if not is_insane:
        display(f"{col}: {is_insane}")
        del data[col]
