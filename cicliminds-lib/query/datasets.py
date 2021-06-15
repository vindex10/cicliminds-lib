import os
import pandas as pd


def get_datasets(path):
    res = []
    for f in os.listdir(path):
        if f.startswith("."):
            continue
        parts = f.replace(".nc", "").split("_")
        variable, period, model, scenario, init_params, timespan = parts
        timespan_from, timespan_to = timespan.split("-")
        full_path = os.path.join(path, f)
        entry = {"variable": variable,
                 "frequency": period,
                 "model": model,
                 "scenario": scenario,
                 "init_params": init_params,
                 "timespan_from": timespan_from[:4],
                 "timespan_to": timespan_to[:4],
                 "path": full_path}
        res.append(entry)
    return pd.DataFrame.from_records(res).set_index("path")
