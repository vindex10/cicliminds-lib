import numpy as np
import regionmask


REFERENCE_REGIONS = regionmask.defined_regions.ar6.land


def get_land_mask(data):
    mask = regionmask.defined_regions.natural_earth.land_110.mask(data)
    return mask == 0


def get_antarctica_mask(data):
    return ~get_reference_region_mask(data, "ANT*")


def get_nan_mask(data):
    return data == data  # pylint: disable=comparison-with-itself


def get_reference_region_mask(data, abbrev):
    return _get_bool_mask_by_abbrev(data, abbrev)


def iter_reference_region_masks(data, abbrevs=None):
    if abbrevs is None:
        abbrevs = REFERENCE_REGIONS.abbrevs
    for abbrev in abbrevs:
        bool_mask = _get_bool_mask_by_abbrev(data, abbrev)
        yield abbrev, bool_mask


def _get_bool_mask_by_abbrev(data, abbrev):
    reg = REFERENCE_REGIONS[[abbrev]]
    mask = reg.mask(data.lon, data.lat)
    bool_mask = ~np.isnan(mask)
    return bool_mask
