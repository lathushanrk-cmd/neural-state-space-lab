import numpy as np
from nssl.dynamics import LinearContinuousDynamics, RegularizedLinearDynamics
from nssl.simulation import system_matrix,simulate_linear,simulate_two_conditions,regression_to_mean_trap
from nssl.validation import validate_known_systems

def test_linear_known_behavior():
    result = validate_known_systems()
    assert result['stable']['final_separation'] < .1
    assert result['unstable']['final_separation'] > .4

def test_analytic_stable():
    t = np.linspace(0,2,21)
    a = LinearContinuousDynamics(np.diag([-1.,-2.]))
    z = a.rollout(np.array([[1,1]]),t)
    assert np.allclose(z[0,:, -1],np.exp([-2,-4]))

def test_two_condition_rate_order():
    s = simulate_two_conditions(noise=0)
    assert np.mean(np.linalg.norm(s['truth'][0,:,:,-1],axis=1)) < np.mean(np.linalg.norm(s['truth'][1,:,:,-1],axis=1))

def test_noise_selection_artifact():
    trap = regression_to_mean_trap(n_trials=5000,random_state=42)
    assert trap['mean_apparent_recovery'] > .05

def test_learned_transition_vs_persistence():
    s = simulate_linear('stable',n_trials=70,noise=0)
    model = RegularizedLinearDynamics(alpha=.001).fit(s['data'][:50],s['times'])
    e = model.evaluate_one_step(s['data'][50:])
    assert e['model_mse'] < e['persistence_mse']
    out = model.compare(s['data'][50:52,:,0],s['data'][50:52,:,0]+.2,30)
    assert out.perturbed.shape == (2,2,31)

def test_simulation_repeatability():
    assert np.array_equal(simulate_linear()['data'],simulate_linear()['data'])
