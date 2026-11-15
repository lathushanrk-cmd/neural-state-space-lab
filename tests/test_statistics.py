import numpy as np
import pytest
from nssl.statistics import bootstrap_mean_ci,permutation_pvalue

def test_bootstrap_determinism_and_grouping():
    x = np.array([1,2,3,4,5,6.])
    a = bootstrap_mean_ci(x,n_boot=200,random_state=3)
    assert a == bootstrap_mean_ci(x,n_boot=200,random_state=3)
    assert a['lower'] <= a['estimate'] <= a['upper']
    b = bootstrap_mean_ci(x,n_boot=200,groups=[1,1,2,2,3,3])
    assert b['sampling_unit'] == 'groups'

def test_pvalue_finite_resolution():
    assert np.isclose(permutation_pvalue(3,[0,1,2],alternative='greater'), .25)
    with pytest.raises(ValueError): permutation_pvalue(1,[],alternative='greater')
