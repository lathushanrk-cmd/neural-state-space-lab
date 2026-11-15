import numpy as np
import pytest
from nssl.embedding import PCAEmbedding, FactorAnalysisEmbedding
from nssl.preprocessing import ChannelStandardizer
from nssl.references import ConditionReference, leave_one_out_reference

def data():
    return np.random.default_rng(1).normal(size=(10,5,20))

@pytest.mark.parametrize("model", [PCAEmbedding,FactorAnalysisEmbedding])
def test_embedding_and_inverse(model):
    x = data()
    obj = model(3).fit(x)
    assert obj.transform(x[:3]).shape == (3,3,20)
    assert obj.inverse_transform(obj.transform(x[:3])).shape == (3,5,20)

def test_embedding_unfitted_and_invalid():
    with pytest.raises(RuntimeError): PCAEmbedding().transform(data())
    with pytest.raises(ValueError): PCAEmbedding(100).fit(data())

def test_preprocessing_train_only():
    x = data()
    norm = ChannelStandardizer().fit(x[:7])
    y = norm.transform(x[:7]); z = norm.transform(x[7:])
    assert np.allclose(y.mean(axis=(0,2)),0)
    assert z.shape == (3,5,20)
    with pytest.raises(RuntimeError): ChannelStandardizer().transform(x)

def test_reference():
    z = data()
    ref = ConditionReference().fit(z[:8], np.array(["a"]*4+["b"]*4))
    assert np.allclose(ref.transform(["a"])[0],z[:4].mean(axis=0))
    loo = leave_one_out_reference(z[:4],["a"]*4)
    assert np.allclose(loo[0],z[1:4].mean(axis=0))
    with pytest.raises(ValueError): leave_one_out_reference(z[:1],["a"])
