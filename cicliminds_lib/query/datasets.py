import numpy as np
import pandas as pd

DATASET_FIELDS = ["model", "scenario", "init_params", "frequency", "variable"]


def get_datasets_for_block(datasets_reg, query):
    mask = get_shallow_filters_mask(datasets_reg, query)
    mask = mask & apply_scenario_filter(datasets_reg, mask, [query["scenario"]])
    return datasets_reg[mask].copy()


def get_shallow_filters_mask(datasets_reg, query):
    mask = pd.Series(np.full(datasets_reg.shape[0], True), index=datasets_reg.index)
    for field in DATASET_FIELDS:
        values = query[field]
        if not values:
            continue
        mask = mask & datasets_reg[field].isin(values)
    return mask


def apply_scenario_filter(datasets, mask, scenarios):
    new_mask = mask.copy()
    scenarios_set = set(scenarios)
    columns_without_scenario = [i for i in datasets.columns if i not in ["scenario", "timespan"]]
    for _, group in datasets[mask].groupby(columns_without_scenario):
        group_scenarios = set(group["scenario"].values)
        if not scenarios_set - group_scenarios:
            continue
        new_mask[group.index] = False
    return new_mask
