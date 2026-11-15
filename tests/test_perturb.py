import numpy as np
import pytest
from nssl.perturb import (IsotropicPerturbation, AxisPerturbation, EmpiricalNoisePerturbation, StateSwapPerturbation)
Z = np.random.default_rng(7).normal(size=(8,3,20))
times = np.linspace(0,1,20)

def test_isotropic_fixed_norm_and_determinism():
    p = IsotropicPerturbation(.6, 4)
    a = p.apply(Z,times=times,time=.5)
    b = p.apply(Z,times=times,time=.5)
    assert np.allclose(np.linalg.norm(a.delta, axis=1), .6)
    assert np.array_equal(a.delta,b.delta)
    assert np.array_equal(Z, Z.copy())

def test_axis_and_direction():
    a = AxisPerturbation(2,axis=1).apply(Z,times=times,time=.5)
    assert np.allclose(a.delta[:,1],2)
    assert np.allclose(a.delta[:,[0,2]],0)
    b = AxisPerturbation(2,direction=[3,4,0]).apply(Z,times=times,time=.5)
    assert np.allclose(np.linalg.norm(b.delta,axis=1),2)

def test_empirical_and_swap():
    a = EmpiricalNoisePerturbation(np.ones((4,3)),magnitude=2).apply(Z,times=times,time=.5)
    assert np.allclose(a.delta,0)
    indices = np.roll(np.arange(8),1)
    b = StateSwapPerturbation(indices).apply(Z,times=times,time=.5)
    assert np.allclose(b.displaced, Z[indices,:,b.index])

def test_failures():
    with pytest.raises(ValueError): IsotropicPerturbation(-1)
    with pytest.raises(ValueError): AxisPerturbation(1,axis=20).apply(Z,times=times,time=.2)
    with pytest.raises(ValueError): StateSwapPerturbation([1,2]).apply(Z,times=times,time=.2)
