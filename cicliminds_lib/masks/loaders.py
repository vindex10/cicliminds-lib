import os

import geopandas as gp
import regionmask
from regionmask.core.regions import Regions
from shapely.geometry import Polygon


def load_reference_regions():
    fname = "referenceRegions/referenceRegions.shp"
    path_to_regions = os.path.join(os.path.dirname(__file__), fname)
    gp_regions = gp.read_file(path_to_regions)
    rmask_regions = regionmask.from_geopandas(gp_regions, name="regions",
                                              names="NAME", abbrevs="LAB")
    return _rmask_with_fixed_negative_degrees(rmask_regions)


def load_reference_regions_meta():
    fname = "referenceRegions/referenceRegions.shp"
    path_to_regions = os.path.join(os.path.dirname(__file__), fname)
    gp_regions = gp.read_file(path_to_regions)
    return gp_regions[["NAME", "LAB", "USAGE"]]


def _rmask_with_fixed_negative_degrees(rmask_regions):
    new_outlines = []
    for region in rmask_regions:
        outline = region._polygon  # pylint: disable=protected-access
        if not isinstance(outline, Polygon):
            raise NotImplementedError("Outline is not a Polygon")
        new_coords = []
        for coord_x, coord_y in outline.exterior.coords[:-1]:
            if coord_x < 180.000001:
                new_coords.append((coord_x, coord_y))
                continue
            new_coords.append((coord_x-360, coord_y))
        new_coords = new_coords[::-1]
        new_outline = Polygon(new_coords)
        new_outlines.append(new_outline)
    return Regions(new_outlines,
                   numbers=rmask_regions.numbers,
                   names=rmask_regions.names,
                   abbrevs=rmask_regions.abbrevs,
                   name=rmask_regions.name,
                   source=rmask_regions.source)
