"""Numerical edge cases, mocked MNE compatibility and failure boundaries."""
import numpy as np
import pandas as pd
import pytest
from nssl.io import NeuralTrajectoryDataset
from nssl.embedding import PCAEmbedding
from nssl.dynamics import RegularizedLinearDynamics, LinearContinuousDynamics
from nssl.nulls import permute_reference_trials, phase_randomized_surrogate, shift_reference
from nssl.statistics import bootstrap_mean_ci, permutation_pvalue
from nssl.simulation import system_matrix
from nssl.preprocessing import ChannelStandardizer
from nssl.perturb import EmpiricalNoisePerturbation
from nssl.metrics import time_to_recovery

def test_mock_mne_epochs_adapter():
    class MiniEpochs:
        def __init__(self):
            self.times = np.array([0.,.1,.2,.3])
            self.metadata = pd.DataFrame({'condition':['a','b'], 'subject':['S1','S1']})
        def get_data(self, **kwargs):
            assert kwargs['picks']=='data'
            return np.ones((2,3,4))
    ds=NeuralTrajectoryDataset.from_mne(MiniEpochs())
    assert ds.data.shape==(2,3,4)
    assert ds.metadata.trial_id.is_unique

def test_adapter_rejects_missing_condition():
    class BadEpochs:
        times = np.arange(4.)
        metadata = pd.DataFrame({'subject':['S1']})
        def get_data(self,**kw):return np.ones((1,2,4))
    with pytest.raises(ValueError):NeuralTrajectoryDataset.from_mne(BadEpochs())

def test_validation_cases():
    with pytest.raises(ValueError):LinearContinuousDynamics(np.ones((2,3)))
    with pytest.raises(ValueError):system_matrix('other')
    with pytest.raises(ValueError):RegularizedLinearDynamics(alpha=-1)
    with pytest.raises(RuntimeError):RegularizedLinearDynamics().rollout(np.ones((1,2)),5)
    z=np.ones((3,2,5))
    with pytest.raises(ValueError):RegularizedLinearDynamics().fit(z,[0,1,2,3,9])
    with pytest.raises(ValueError):PCAEmbedding(2).fit(np.arange(24.).reshape(3,2,4)).transform(np.ones((3,3,4)))
    with pytest.raises(ValueError):ChannelStandardizer().fit(z).transform(np.ones((3,3,5)))
    with pytest.raises(ValueError):EmpiricalNoisePerturbation(np.ones((3,2))).apply(z,times=np.arange(5),time=7)
    with pytest.raises(ValueError):time_to_recovery([1,2,3],[0,1,2],-1)

def test_null_and_statistical_failures():
    with pytest.raises(ValueError):shift_reference(np.ones((2,2)),min_shift=2)
    with pytest.raises(ValueError):permute_reference_trials(np.ones((3,2,4)),groups=[1])
    with pytest.raises(ValueError):phase_randomized_surrogate(np.ones((3,2)))
    with pytest.raises(ValueError):bootstrap_mean_ci([1,np.nan],n_boot=100)
    with pytest.raises(ValueError):bootstrap_mean_ci([1,2,3],groups=[1,1,1])
    with pytest.raises(ValueError):permutation_pvalue(1,[1,2],alternative='nonsense')

def test_phase_surrogate_preserves_cross_spectra():
    x=np.random.default_rng(0).normal(size=(3,64))
    y=phase_randomized_surrogate(x)
    before=np.fft.rfft(x,axis=1)
    after=np.fft.rfft(y,axis=1)
    assert np.allclose(before[0]*np.conj(before[1]),after[0]*np.conj(after[1]),atol=1e-9)
