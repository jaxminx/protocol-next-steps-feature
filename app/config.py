"""Loads the adjustable settings in config/: bands, tests, retest timing and demo tokens."""
from decimal import Decimal
from pathlib import Path

import yaml
from pydantic import BaseModel

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


class Test(BaseModel):
    key: str
    name: str
    price_sgd: int
    covers: list[str]


class RetestPolicy(BaseModel):
    test: str
    due_soon_days: int
    early_retest_days: int


class DemoUser(BaseModel):
    member_id: str
    preferred_name: str


# A band is a set of limits, e.g. {"ge": 30, "le": 200} for 30–200.
Band = dict[str, Decimal]


def _read(filename: str) -> dict:
    with open(CONFIG_DIR / filename, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _as_decimals(limits: dict) -> Band:
    # str() first, so YAML's 2.6 becomes exactly 2.6 rather than 2.600000000000000088…
    return {op: Decimal(str(limit)) for op, limit in limits.items()}


BANDS: dict[str, dict[str, Band]] = {
    marker: {band: _as_decimals(limits) for band, limits in bands.items()}
    for marker, bands in _read("bands.yaml").items()
}
TESTS: dict[str, Test] = {key: Test(key=key, **spec) for key, spec in _read("tests.yaml").items()}
RETEST = RetestPolicy(**_read("retest.yaml"))
DEMO_TOKENS: dict[str, DemoUser] = {token: DemoUser(**user) for token, user in _read("tokens.yaml").items()}
