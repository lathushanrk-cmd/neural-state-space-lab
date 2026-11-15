"""Ensure published neon assets are derived reproducibly from actual simulations."""
import json
from nssl.demo import generate

def test_generate_all_figures(tmp_path):
    paths=generate(tmp_path)
    assert len(paths)==9
    assert all(path.exists() and path.stat().st_size>100 for path in paths)
    result=json.loads((tmp_path/'simulation_results.json').read_text())
    assert result['source']=='exact known-system ODE and seeded synthetic processes'
    assert result['stable_final_separation']<result['stable_initial_separation']
    assert result['unstable_final_separation']>result['unstable_initial_separation']
