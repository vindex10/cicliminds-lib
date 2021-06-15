import os
import unittest

import numpy as np
import xarray as xr

from cicliminds_lib.query.datasets import parse_dataset_name
from cicliminds_lib.bindings.cdo import cdo_fldmean_from_data
from cicliminds_lib.bindings.cdo import cdo_gridweights_from_data


class TestWeights(unittest.TestCase):
    def setUp(self):
        dataset_path, variable = self._get_dataset()
        self.dataset_path = dataset_path
        self.variable = variable

    def test_weights(self):
        dat = self._prepare_dataset(self.dataset_path, self.variable)

        mean_cdo = cdo_fldmean_from_data(dat)
        mean_manual = self._calc_mean_manually(dat[self.variable])

        dev = np.sum((mean_cdo[self.variable].values.ravel() - mean_manual.values.ravel())**2)
        rel_dev = dev/np.mean(mean_manual.values.ravel())
        self.assertLess(rel_dev, 1E-5)

    @staticmethod
    def _prepare_dataset(path, var):
        dat = xr.load_dataset(path)
        dat[var] = dat[var]/np.timedelta64(1, 'ns')
        return dat

    @staticmethod
    def _calc_mean_manually(dat_var):
        weights = cdo_gridweights_from_data(dat_var)
        manual_mean = (dat_var).weighted(weights).mean(dim=["lon", "lat"])
        return manual_mean

    @staticmethod
    def _get_dataset():
        data_dir = os.environ["DATA_DIR"]
        f = None
        for f in os.listdir(data_dir):
            if f.endswith(".nc"):
                break
        if f is None:
            raise FileNotFoundError("No netcdf4 input files in the DATA_DIR")
        parsed = parse_dataset_name(f)
        path = os.path.join(data_dir, f)
        return path, parsed["variable"]
