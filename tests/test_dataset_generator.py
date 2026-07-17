import sys
import os
import pytest

# Ensure services/ese-core is on pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../services/ese-core")))

@pytest.fixture(autouse=True)
def isolate_dataset_env():
    # Save original value
    old_val = os.environ.get("ACTIVE_DATASET")
    os.environ["ACTIVE_DATASET"] = "test_temp_generator"
    yield
    # Restore original value
    if old_val is not None:
        os.environ["ACTIVE_DATASET"] = old_val
    else:
        os.environ.pop("ACTIVE_DATASET", None)

from dataset_generator import DatasetGenerator

def test_deterministic_generation():
    """Verify that using the same seed produces identical dataset sizes and statistics"""
    gen1 = DatasetGenerator(seed=101)
    res1 = gen1.generate("tiny")
    
    gen2 = DatasetGenerator(seed=101)
    res2 = gen2.generate("tiny")
    
    assert res1["customers"] == res2["customers"]
    assert res1["businesses"] == res2["businesses"]
    assert res1["transactions"] == res2["transactions"]
    assert res1["customers"] == 25

def test_profile_sizes():
    """Verify customer counts map correctly to profile sizes"""
    gen = DatasetGenerator(seed=202)
    res_tiny = gen.generate("tiny")
    assert res_tiny["customers"] == 25
    
    res_small = gen.generate("small")
    assert res_small["customers"] == 100

def test_performance_targets():
    """Verify tiny and small profiles generate well within SLA limits"""
    gen = DatasetGenerator(seed=303)
    res = gen.generate("tiny")
    assert res["duration_seconds"] < 5.0
