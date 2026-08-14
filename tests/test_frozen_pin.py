"""frozen_v1.yaml refactor pin: the schema-expressed frozen definition must
reproduce the campaign's standing overrides exactly."""
from backtest.campaign import BASE_OVERRIDES, _FROZEN


def test_frozen_definition_is_pure_refactor():
    assert BASE_OVERRIDES == {
        "features.baseline_mode": "session_time",
        "features.baseline_sessions": 8,
        "features.min_baseline_obs": 5}
    assert _FROZEN["mode"] == "engine"
    assert _FROZEN["exit_scheme"] == {"name": "r_multiple", "r": 2.0,
                                      "stop": {"name": "beyond_signature_n"}}
