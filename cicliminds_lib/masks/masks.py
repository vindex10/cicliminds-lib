import numpy as np
import regionmask
from cicliminds_lib.masks.loaders import load_reference_regions


def get_oceans_mask(data):
    mask = regionmask.defined_regions.natural_earth.land_110.mask(data)
    return mask == 0


def get_antarctica_mask(data):
    mask = regionmask.defined_regions.natural_earth.countries_110.mask(data)
    ant = regionmask.defined_regions.natural_earth.countries_110.map_keys("Antarctica")
    return mask != ant


def get_nan_mask(data):
    return data == data  # pylint: disable=comparison-with-itself


def get_reference_region_mask(data, abbrev):
    regions = load_reference_regions()
    return _get_bool_mask_by_abbrev(regions, data, abbrev)


def iter_reference_region_masks(data):
    regions = load_reference_regions()
    for abbrev in regions.abbrevs:
        bool_mask = _get_bool_mask_by_abbrev(regions, data, abbrev)
        yield abbrev, bool_mask


def _get_bool_mask_by_abbrev(regions, data, abbrev):
    reg = regions[[abbrev]]
    mask = reg.mask(data.lon, data.lat)
    bool_mask = ~np.isnan(mask)
    return bool_mask
