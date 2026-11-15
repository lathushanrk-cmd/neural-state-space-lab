"""Run local resource/runtime benchmark. Never publish hardware-independent numbers."""
import json
import platform
from pathlib import Path
from time import perf_counter
import tracemalloc
import numpy as np
from nssl.embedding import PCAEmbedding
from nssl.perturb import IsotropicPerturbation

def bench():
    records = []
    for n_trials, n_features in ((10,10),(30,20),(60,40),(120,40)):
        x = np.random.default_rng(9).normal(size=(n_trials,n_features,100))
        tracemalloc.start()
        start = perf_counter()
        embedded = PCAEmbedding(min(6,n_features)).fit_transform(x)
        fit_seconds = perf_counter()-start
        start = perf_counter()
        IsotropicPerturbation(1.,42).apply(embedded,times=np.linspace(0,1,100),time=.5)
        perturb_seconds = perf_counter()-start
        _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
        records.append({"trials":n_trials,"features":n_features,"fit_seconds":fit_seconds,
                        "perturb_seconds":perturb_seconds,"peak_traced_bytes":peak})
    output=Path("benchmarks/results.json")
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps({"machine":platform.platform(), "python":platform.python_version(),
                                 "records":records,"note":"measured locally; tracemalloc does not capture all native allocations"},indent=2))
    print(output)

if __name__=="__main__":bench()
