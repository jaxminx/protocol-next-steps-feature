"""The member file as it arrives, validated on load.

Only the fields this feature needs are declared. InBody, wearables, protocols, longevity
scores, age, sex and full name are in the file but never read.
"""
import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from pydantic import BaseModel


class Report(BaseModel):
    id: str
    date: date
    type: str                  # core, retest or upload
    review: str | None = None  # uploads only: pending, verified or rejected
    lab: str | None = None

    @property
    def is_verified(self) -> bool:
        """Our own tests are trusted. Another clinic's upload is trusted once our team has checked it."""
        return self.type in ("core", "retest") or self.review == "verified"

    @property
    def counts_as_retest(self) -> bool:
        return self.type in ("core", "retest")


class ResultRow(BaseModel):
    report: str
    marker: str
    value: Decimal
    unit: str


class Membership(BaseModel):
    retest_due: date


class MemberFile(BaseModel):
    today: date
    membership: Membership
    reports: list[Report]
    results: list[ResultRow]


def load_member_file(path: Path) -> MemberFile:
    """Parse every number as an exact Decimal, then validate. A malformed file raises here."""
    with open(path, encoding="utf-8") as f:
        raw = json.load(f, parse_float=Decimal, parse_int=Decimal)
    return MemberFile.model_validate(raw)
