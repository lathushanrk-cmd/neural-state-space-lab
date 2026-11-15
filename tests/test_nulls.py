import numpy as np
import pytest
from nssl.nulls import permute_trial_labels,shift_reference,random_times,phase_randomized_surrogate,permute_reference_trials

def test_permutations():
    c = np.array([0,0,1,1,2,2])
    assert sorted(permute_trial_labels(c)) == sorted(c)
    assert np.array_equal(permute_trial_labels(c, groups=[1,1,1,2,2,2])[:3],np.array([0,0,1])) or set(permute_trial_labels(c, groups=[1,1,1,2,2,2])[:3])=={0,1}
    ref = np.arange(30.).reshape(2,15)
    assert not np.array_equal(shift_reference(ref),ref)
    assert len(random_times(10,5)) == 5
    assert permute_reference_trials(np.ones((4,2,10))).shape == (4,2,10)

def test_phase_preserves_periodogram():
    x = np.random.default_rng(8).normal(size=(3,300))
    y = phase_randomized_surrogate(x)
    assert np.allclose(np.abs(np.fft.rfft(x,axis=-1)),np.abs(np.fft.rfft(y,axis=-1)),atol=1e-9)
    assert not np.allclose(x,y)

def test_invalid_null():
    with pytest.raises(ValueError): phase_randomized_surrogate(np.array([1,2,3]))
