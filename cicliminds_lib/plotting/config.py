from dataclasses import dataclass
from numbers import Number
from typing import Optional


DEFAULT_RECIPE_CONFIG = {
    "yscale": "linear",
    "binsize": None,
    "bincount": None,
    "reference_window_size": 50,
    "sliding_window_size": 30,
    "slide_step": 30,
    "normalize_histograms": True,
    "colormap": "gist_rainbow",
    "init_year": 0
}


@dataclass
class RecipeConfig:
    unit: str
    unit_factor: Number
    yscale: str = DEFAULT_RECIPE_CONFIG["yscale"]
    binsize: Optional[Number] = DEFAULT_RECIPE_CONFIG["binsize"]
    bincount: Optional[Number] = DEFAULT_RECIPE_CONFIG["bincount"]
    reference_window_size: Number = DEFAULT_RECIPE_CONFIG["reference_window_size"]
    sliding_window_size: Number = DEFAULT_RECIPE_CONFIG["sliding_window_size"]
    slide_step: Number = DEFAULT_RECIPE_CONFIG["slide_step"]
    normalize_histograms: bool = DEFAULT_RECIPE_CONFIG["normalize_histograms"]
    colormap: str = DEFAULT_RECIPE_CONFIG["colormap"]
    init_year: Number = DEFAULT_RECIPE_CONFIG["init_year"]
