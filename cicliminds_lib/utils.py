import tempfile
import subprocess

from dataclasses import asdict
from dataclasses import replace

import numpy as np
import xarray as xr


def filter_pdarray(pdarray, query):
    mask = np.array(True)
    for key, val in query.items():
        mask = mask & (pdarray[key] == val)
    return pdarray[mask]


def run_fs_cmd(fout_path, cmd, fin_path):
    if not isinstance(fin_path, str):
        fin_path = " ".join(map(str, fin_path))
    subprocess.run(f"{cmd} {fin_path} {fout_path}", shell=True)


def data_to_data(func, newvar=None):
    def _func(data, *args):
        with tempfile.NamedTemporaryFile("r") as fout, \
             tempfile.NamedTemporaryFile("r") as fin:
            data.to_netcdf(fin.name)
            func(fout.name, fin.name, *args)
            res = xr.load_dataset(fout.name, engine="netcdf4")
        if not isinstance(data, xr.DataArray):
            return res
        newvar_name = newvar if newvar is not None else data.name
        return res[newvar_name]
    return _func


def _get_dataclass_patch_from_dict(cfg, update):
    patch_fields = set(asdict(cfg)).intersection(set(list(update)))
    patch = {k: update[k] for k in patch_fields}
    return patch


def _get_dataclass_patch_from_ntuple(cfg, update):
    patch_fields = set(fields(cfg)).intersection(set(update._fields))
    patch = {k: v for k in fields(cfg) if k in update}
    return patch


def patch_config(cfg, update):
    if isinstance(update, dict):
        patch = _get_dataclass_patch_from_dict(cfg, update)
    elif hasattr(update, "_fields"):
        patch = _get_dataclass_patch_from_ntuple(cfg, update)
    elif isinstance(update, list):
        if not update:
            return cfg
        patch = patch_config(cfg, update[0])
        patch = patch_config(patch, update[1:])
        patch = asdict(patch)
    else:
        raise ValueError("unsupported type of the patch")
    return replace(cfg, **patch)
