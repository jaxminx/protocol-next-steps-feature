import copy
import json
from decimal import Decimal
from pathlib import Path

import pytest

from app.cleaning import clean
from app.next_steps import build_next_steps
from app.records import MemberFile

with open(Path(__file__).parent.parent / "data" / "alex_lim.json", encoding="utf-8") as f:
    ALEX = json.load(f, parse_float=Decimal, parse_int=Decimal)


@pytest.fixture
def run():
    """Clean a member file and build the response. Returns (clean record, response body)."""
    def _run(member_file=None):
        record = clean(MemberFile.model_validate(member_file or copy.deepcopy(ALEX)))
        return record, build_next_steps(record, "Alex")
    return _run
