import numpy as np
from nssl.trajectories import velocity,trajectory_centroid

def test_velocity_and_centroid():
    t=np.linspace(0,1,11)
    z=np.stack([2*t,3*t])[None,:,:]
    v=velocity(z,t)
    assert np.allclose(v[:,0],2)
    assert np.allclose(v[:,1],3)
    assert trajectory_centroid(z).shape==(2,11)
