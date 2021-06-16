import regionmask


def get_oceans_mask(data):
    mask = regionmask.defined_regions.natural_earth.land_110.mask(data)
    return mask == 0


def get_antarctica_mask(data):
    mask = regionmask.defined_regions.natural_earth.countries_110.mask(data)
    ant = regionmask.defined_regions.natural_earth.countries_110.map_keys("Antarctica")
    return mask != ant


def get_nan_mask(data):
    return data == data  # pylint: disable=comparison-with-itself
