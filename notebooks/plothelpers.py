import numpy as np
import pandas as pd


class Params:
    c = None
    lr = None
    N = None

    def __init__(self, c, lr, N):
        self.c = c
        self.lr = lr
        self.N = N
        
    def __str__(self):
        base = f"c:{self.c}, lr: {self.lr}, N: {self.N}"
        
        optional = ""
            
        return base + optional
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
        
    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))


def extract_params(filename):
    # Remove extension
    name = filename.split(".csv")[0]
    name = name.split("/")[-1]

    params = name.split("-")

    if len(params) == 5:
        # Old version of files has a redundant parameter now
        output_type, c, lr, n, _ = params
    else:
        output_type, c, lr, n = params

    return Params(float(c), float(lr), int(n))


def split_into_runs(results, params):
    """
    When we export runs, they are all in one big pandas dataframe. Here, we split these into n
    runs, and return an array of these runs
    """
    N = params.N
    runs = int(len(results) / N)
    return [results.iloc[N*run: N*(run+1)].copy() for run in range(runs)]


def _freedman_diaconis(data):
    # Freedman Diaconis rule for bin sizes
    h = 2 * (np.percentile(data, 75) - np.percentile(data, 25)) / np.cbrt(len(data))
    
    # Default
    if h == 0:
        return 10
    
    # Bin size based on rule
    return int(np.ceil((data.max() - data.min()) / h))


def entropy(column):
    bins = _freedman_diaconis(column)
    vc = pd.Series(column).value_counts(normalize=True, sort=False, bins=bins)
    
    # Entropy, with convention 0 * log(0)=0
    ent = lambda x: -(x * np.log2(x, where=(x!=0), out=np.zeros_like(x))).sum()
    
    uniform = np.asarray([1/len(vc)] * len(vc))
    
    # Normalised entropy
    return ent(vc) / ent(uniform)
