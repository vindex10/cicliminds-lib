import os
import pandas as pd


def get_datasets(path):
    res = []
    for f in os.listdir(path):
        if not f.endswith(".nc"):
            continue
        entry = parse_dataset_name(f)
        entry["path"] = os.path.join(path, f)
        res.append(entry)
    return pd.DataFrame.from_records(res).set_index("path")


def parse_dataset_name(f):
    parts = f.replace(".nc", "").split("_")
    variable, period, model, scenario, init_params, timespan = parts
    timespan_from, timespan_to = timespan.split("-")
    entry = {"variable": variable,
             "frequency": period,
             "model": model,
             "scenario": scenario,
             "init_params": init_params,
             "timespan_from": timespan_from[:4],
             "timespan_to": timespan_to[:4]}
    return entry
