"""OPTIONAL ONLINE REAL-DATA EXAMPLE. Downloads PhysioNet EEGBCI via MNE.
No raw EEG files are bundled. A reproduced subject-1 observational figure and\nmetadata are archived under results/eegbci_subject1/.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nssl import NeuralTrajectoryDataset, PCAEmbedding, ConditionReference
from nssl.preprocessing import ChannelStandardizer
from nssl.metrics import reference_distance
from nssl.plotting import neon_style, finish_axis, CYAN, PINK, BG

def extract_motor_imagery_events(raw):
    """Extract exactly T1/hands and T2/feet with stable explicit integer IDs."""
    import mne
    if not {"T1", "T2"}.issubset(set(raw.annotations.description)):
        raise ValueError("expected hand/foot cue annotations were not found")
    raw.annotations.rename(dict(T1="hands", T2="feet"))
    events, mapping = mne.events_from_annotations(
        raw, event_id={"hands": 2, "feet": 3}, verbose=False
    )
    if set(mapping) != {"hands", "feet"} or not len(events):
        raise ValueError("expected hand/foot cue annotations were not found")
    return events, mapping

def main():
    import mne
    from mne.datasets import eegbci
    from mne.io import read_raw_edf
    files = eegbci.load_data(1, [6,10,14], update_path=True)
    raws = [read_raw_edf(f, preload=True, verbose=False) for f in files]
    raw = mne.concatenate_raws(raws)
    events, event_id = extract_motor_imagery_events(raw)
    raw.filter(l_freq=7, h_freq=30, verbose=False)
    epochs = mne.Epochs(raw, events=events, event_id=event_id, tmin=0.5, tmax=3.0,
                        baseline=None, preload=True, picks="eeg", verbose=False)
    if not len(epochs):
        raise ValueError("no usable EEG epochs after preprocessing")
    labels = np.array(["hands" if k == 2 else "feet" for k in epochs.events[:,2]])
    epochs.metadata = pd.DataFrame({"trial_id":np.arange(len(labels)), "condition":labels,
                                     "subject":np.repeat("S001",len(labels))})
    ds = NeuralTrajectoryDataset.from_mne(epochs)
    rng = np.random.default_rng(42)
    train, test = [], []
    for c in np.unique(labels):
        ids = rng.permutation(np.flatnonzero(labels == c))
        split = int(len(ids)*.7)
        if split < 2 or split == len(ids):
            raise ValueError("not enough trials per condition")
        train.extend(ids[:split]); test.extend(ids[split:])
    train, test = np.asarray(train), np.asarray(test)
    scale = ChannelStandardizer().fit(ds.data[train])
    xtrain, xtest = scale.transform(ds.data[train]), scale.transform(ds.data[test])
    emb = PCAEmbedding(n_components=3).fit(xtrain)
    ztrain, ztest = emb.transform(xtrain), emb.transform(xtest)
    refs = ConditionReference().fit(ztrain,labels[train]).transform(labels[test])
    distances = reference_distance(ztest,refs)
    output = Path("outputs/eegbci"); output.mkdir(parents=True, exist_ok=True)
    with neon_style():
        fig,ax=plt.subplots(figsize=(11,5),layout="constrained")
        for label,color in (("hands",CYAN),("feet",PINK)):
            subset=distances[labels[test]==label]
            ax.plot(ds.times,subset.mean(axis=0),label=f"{label} (n={len(subset)})",color=color,lw=2)
        finish_axis(ax,"Held-out distance to training-condition PCA trajectory", "Time after cue (s)", "Distance (standardized PCA coordinates)")
        ax.legend()
        fig.savefig(output/"eeg_observational.png",dpi=175,facecolor=BG,bbox_inches="tight")
        plt.close(fig)
    summary={"event_mapping": event_id, "dataset":"PhysioNet EEGBCI motor imagery", "participant":"subject 1", "runs":[6,10,14],
             "train_trials":len(train), "test_trials":len(test),"seed":42,
             "scope":"descriptive observational held-out trial analysis, no inferential p-values",
             "limitation":"single participant; no independent-subject generalization; not a perturbation experiment"}
    (output/"eeg_observational_metadata.json").write_text(json.dumps(summary,indent=2))
    print(summary)

if __name__=="__main__":
    main()
