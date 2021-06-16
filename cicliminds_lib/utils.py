import numpy as np


def filter_pdarray(pdarray, query):
    mask = np.array(True)
    for key, val in query:
        mask = mask & (pdarray[key] == val)
    return pdarray[mask]
