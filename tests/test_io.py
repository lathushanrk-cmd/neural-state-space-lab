import numpy as np
import pandas as pd
import pytest
from nssl.io import NeuralTrajectoryDataset, chronological_index

def data():
    return NeuralTrajectoryDataset(np.zeros((4,3,6)), np.linspace(0,1,6),pd.DataFrame({"trial_id":range(4),"condition":["a","a","b","b"],"subject":[1,1,2,2]}))

def test_create_subset():
    ds = data()
    assert ds.subset([0,2]).data.shape == (2,3,6)
    assert chronological_index(ds.times,.4) == 2

@pytest.mark.parametrize("change", ["nan", "times", "metadata", "dupe"])
def test_bad_data(change):
    ds = data()
    x, t, m = ds.data.copy(), ds.times.copy(), ds.metadata.copy()
    if change == "nan": x[0,0,0] = np.nan
    if change == "times": t[2] = t[1]
    if change == "metadata": m = m.iloc[:2]
    if change == "dupe": m.loc[1,"trial_id"] = 0
    with pytest.raises(ValueError): NeuralTrajectoryDataset(x,t,m)

def test_time_failure():
    with pytest.raises(ValueError): chronological_index(np.arange(4), 10)
