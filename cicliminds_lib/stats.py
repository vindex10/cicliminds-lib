import scipy as sp
from scipy import stats  # pylint: disable=unused-import # noqa: F401


def sigma_to_quantile(s):
    tail = 1 - sp.stats.distributions.norm().cdf(s)
    return tail, 1 - tail
