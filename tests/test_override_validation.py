import pytest
from engine.config import load
from engine.strategy import validate_overrides


def test_bogus_override_path_refused():
    cfg = load()
    validate_overrides(cfg, {"gating.strict_mode": True})   # valid
    with pytest.raises(ValueError, match="gating.strict_modes"):
        validate_overrides(cfg, {"gating.strict_modes": True})
    with pytest.raises(ValueError, match="trial log"):
        validate_overrides(cfg, {"nonexistent.key": 1})
