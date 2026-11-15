import numpy as np
import pytest
from nssl.metrics import reference_distance,recovery_fraction,time_to_recovery,divergence_integral,directional_restoration,local_trajectory_separation

def test_metrics_known_answers():
    z = np.array([[[3.,2.,1.],[4.,0.,0.]]])
    ref = np.zeros_like(z)
    d = reference_distance(z,ref)
    assert np.allclose(d[0],[5,2,1])
    assert np.isclose(recovery_fraction(d)[0],.8)
    assert np.isclose(time_to_recovery(d[0],[0,1,2],1),2)
    assert np.isnan(time_to_recovery(d[0],[0,1,2],.5))
    assert np.isclose(divergence_integral(d[0],[0,1,2]),5)
    assert np.array_equal(local_trajectory_separation(z,ref),d)

def test_directional_restoration():
    z = np.array([[3.,2.,1.],[0.,0.,0.]])
    r = np.zeros_like(z)
    q = directional_restoration(z,r,[0,1,2])
    assert np.allclose(q,1)

def test_zero_direction_undefined():
    z = np.ones((2,5))
    assert np.isnan(directional_restoration(z,z,np.arange(5))).all()

def test_metric_failures():
    with pytest.raises(ValueError): reference_distance(np.zeros((2,3)),np.zeros((2,4)))
    with pytest.raises(ValueError): recovery_fraction([-1,0])
    with pytest.raises(ValueError): time_to_recovery([1,0],[0,0],1)
