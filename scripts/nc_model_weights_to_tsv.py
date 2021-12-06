import sys
from contextlib import contextmanager
import xarray as xr


def main(path_to_dataset):
    with safe_open_dataset(path_to_dataset) as data:
        weights = data.weight.data
        keys = data.model_ensemble.data
    header, rows = parse(keys, weights)
    res = to_tsv(rows, header=header)
    print(res)


def parse(keys, weights):
    header = ["model", "init_param", "scenario", "weight"]
    rows = []
    for key, weight in zip(keys, weights):
        model, init_param, scenario = key.split("_")
        rows.append((model, init_param, scenario, weight))
    return header, rows


def to_tsv(rows, header=None):
    res = ("\t".join(header) + "\n") if header else ""
    res += "\n".join(("\t".join(map(str, row)) for row in rows))
    res += "\n"
    return res


@contextmanager
def safe_open_dataset(*args, **kwargs):
    try:
        dataset = xr.open_dataset(*args, **kwargs)
        yield dataset
    finally:
        dataset.close()


if __name__ == "__main__":
    path_to_dataset = sys.argv[1]
    main(path_to_dataset)
