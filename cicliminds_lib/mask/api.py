import pandas as pd
import xarray as xr

from cicliminds_lib.mask import get_land_mask
from cicliminds_lib.mask import get_antarctica_mask
from cicliminds_lib.mask import iter_reference_region_masks


def get_dataset_mask_by_query(dataset, plot_query):
    mask = _get_regions_mask(dataset, plot_query["regions"])
    return mask


def _get_regions_mask(data, regions):
    mask = get_land_mask(data)

    if not regions:
        mask = mask & (~get_antarctica_mask(data))
        return data.where(mask)

    all_reg_masks = [reg_mask for _, reg_mask in iter_reference_region_masks(data, regions)]
    reg_dim = pd.Series(regions, name="regions")
    merged_reg_mask = xr.concat(all_reg_masks, dim=reg_dim).any(dim="regions")
    mask = mask & merged_reg_mask
    return mask
    return data.where(mask)
