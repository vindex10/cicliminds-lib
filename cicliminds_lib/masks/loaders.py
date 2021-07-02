import geopandas as gp
import regionmask
from regionmask.core.regions import Regions
from shapely.geometry import Polygon

try:
    from importlib_resources import path
except ImportError:
    from importlib.resources import path


def load_reference_regions():
    with path("cicliminds_lib.masks", "referenceRegions.zip") as path_to_regions:
        gp_regions = gp.read_file(f"zip://{path_to_regions}")
    rmask_regions = regionmask.from_geopandas(gp_regions, name="regions",
                                              names="NAME", abbrevs="LAB")
    return _rmask_with_fixed_negative_degrees(rmask_regions)


def load_reference_regions_meta():
    with path("cicliminds_lib.masks", "referenceRegions.zip") as path_to_regions:
        gp_regions = gp.read_file(f"zip://{path_to_regions}")
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
