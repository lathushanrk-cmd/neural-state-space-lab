# Tutorial 1 — Ground-truth stable dynamics

```python
import numpy as np
from nssl.dynamics import LinearContinuousDynamics
from nssl.simulation import system_matrix
from nssl.metrics import local_trajectory_separation, recovery_fraction

times = np.linspace(0, 5, 201)
model = LinearContinuousDynamics(system_matrix("stable"))
initial = np.array([[1.0, 0.5]])
displaced = initial + np.array([[0.4, 0.]])
result = model.compare(initial, displaced, times)
distance = local_trajectory_separation(result.perturbed, result.baseline)
print(distance[0, 0], distance[0, -1], recovery_fraction(distance)[0])
```

Both states evolve in a known linear field; separation decays in this simulated stable system. This does not establish the dynamics of a real brain.
