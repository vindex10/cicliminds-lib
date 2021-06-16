from cicliminds_lib.bindings.cdo import cdo_fldpctl_from_data
from cicliminds_lib.bindings.cdo import cdo_fldmean_from_data
from cicliminds_lib.bindings.cdo import cdo_fldmin_from_data
from cicliminds_lib.bindings.cdo import cdo_fldmax_from_data
from cicliminds_lib.stats import sigma_to_quantile


def get_sigma_band(val, s):
    lower_q, upper_q = sigma_to_quantile(s)
    lower_p, upper_p = lower_q*100, upper_q*100
    lower_edge = cdo_fldpctl_from_data(val, lower_p)
    upper_edge = cdo_fldpctl_from_data(val, upper_p)
    return lower_edge, upper_edge


def get_mean(val):
    mean = cdo_fldmean_from_data(val)
    return mean


def get_spreads(val):
    min_edge = cdo_fldmin_from_data(val)
    max_edge = cdo_fldmax_from_data(val)
    return min_edge, max_edge
