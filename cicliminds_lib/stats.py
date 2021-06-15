import scipy as sp
from scipy import stats  # pylint: disable=unused-import # noqa: F401

from cicliminds_lib.bindings.cdo import cdo_fldpctl_from_data


def sigma_to_quantile(s):
    tail = 1 - sp.stats.distributions.norm().cdf(s)
    return tail, 1 - tail


def get_sigma_band(val, s):
    lower_q, upper_q = sigma_to_quantile(s)
    lower_p, upper_p = lower_q*100, upper_q*100
    lower_edge = cdo_fldpctl_from_data(val, lower_p)
    upper_edge = cdo_fldpctl_from_data(val, upper_p)
    return lower_edge, upper_edge
