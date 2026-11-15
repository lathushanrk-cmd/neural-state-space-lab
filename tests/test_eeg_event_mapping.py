"""Offline test of explicit EEGBCI annotation codes; not a real dataset validation."""
import importlib.util
from pathlib import Path
import numpy as np
import pytest

def test_explicit_motor_events_with_rest_annotation():
    mne = pytest.importorskip("mne")
    module_path = Path(__file__).resolve().parents[1] / "reproduce" / "eegbci_demo.py"
    spec = importlib.util.spec_from_file_location("eegbci_demo", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    info = mne.create_info(["C3", "C4"], sfreq=100, ch_types=["eeg", "eeg"])
    raw = mne.io.RawArray(np.zeros((2, 1100)), info, verbose=False)
    raw.set_annotations(mne.Annotations(onset=[1., 3., 5., 7.], duration=[0]*4,
                                         description=["T0", "T1", "T2", "T1"]))
    events, mapping = mod.extract_motor_imagery_events(raw)
    assert mapping == {"hands": 2, "feet": 3}
    assert events[:, 2].tolist() == [2, 3, 2]
    ep = mne.Epochs(raw, events=events, event_id=mapping, tmin=0, tmax=.5,
                    preload=True, baseline=None, verbose=False)
    assert len(ep) == 3
    assert ep["hands"].events[:, 2].tolist() == [2, 2]
    assert ep["feet"].events[:, 2].tolist() == [3]

def test_no_expected_cues_rejected():
    mne = pytest.importorskip("mne")
    module_path = Path(__file__).resolve().parents[1] / "reproduce" / "eegbci_demo.py"
    spec = importlib.util.spec_from_file_location("eegbci_demo", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    raw = mne.io.RawArray(np.zeros((1, 500)), mne.create_info(["C3"], 100, ch_types="eeg"), verbose=False)
    raw.set_annotations(mne.Annotations(onset=[1.], duration=[0.], description=["T0"]))
    with pytest.raises(ValueError, match="hand/foot"):
        mod.extract_motor_imagery_events(raw)
