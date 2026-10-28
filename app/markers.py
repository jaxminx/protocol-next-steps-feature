"""The markers this service knows about: names, display units and unit conversions.

These are fixed facts. Anything a clinician or the business might tune lives in config/.
"""
import re
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from typing import Callable

Converter = Callable[[Decimal], Decimal]


def normalise_name(name: str) -> str:
    """'LDL-C', 'ldl c' and 'LDL C' all become 'ldlc'."""
    return re.sub(r"[\s\-()]", "", name).lower()


def normalise_unit(unit: str) -> str:
    """'µg/L', 'μg/L' (a different character) and 'ug/l' all become 'ug/l'."""
    return re.sub(r"\s", "", unit).lower().replace("µ", "u").replace("μ", "u")


@dataclass(frozen=True)
class Marker:
    key: str
    name: str
    display_unit: str
    decimals: int
    aliases: tuple[str, ...]
    # Accepted input units. None means the unit is already the display unit.
    conversions: dict[str, Converter | None] = field(default_factory=dict)

    def accepts(self, unit: str) -> bool:
        return normalise_unit(unit) in self._conversions_by_unit()

    def to_display_unit(self, value: Decimal, unit: str) -> Decimal:
        convert = self._conversions_by_unit()[normalise_unit(unit)]
        return convert(value) if convert else value

    def round(self, value: Decimal) -> Decimal:
        """Round half up for display. Python's round() would turn 2.65 into 2.6."""
        return value.quantize(Decimal(1).scaleb(-self.decimals), rounding=ROUND_HALF_UP)

    def _conversions_by_unit(self) -> dict[str, Converter | None]:
        return {normalise_unit(unit): convert for unit, convert in self.conversions.items()}


# Conversion formulas come from the brief.
_MARKER_LIST = [
    Marker("ldl", "LDL Cholesterol", "mmol/L", 1, ("LDL Cholesterol", "LDL-C"),
           {"mmol/L": None, "mg/dL": lambda v: v / Decimal("38.67")}),
    Marker("apob", "ApoB", "g/L", 2, ("ApoB",), {"g/L": None}),
    Marker("hba1c", "HbA1c", "mmol/mol", 1, ("HbA1c",),
           {"mmol/mol": None, "%": lambda v: (v - Decimal("2.15")) * Decimal("10.929")}),
    Marker("hscrp", "hs-CRP", "mg/L", 1, ("hs-CRP",), {"mg/L": None}),
    Marker("vitd", "Vitamin D (25-OH)", "nmol/L", 1, ("Vitamin D (25-OH)", "25 OH Vitamin D"),
           {"nmol/L": None, "ng/mL": lambda v: v * Decimal("2.496")}),
    Marker("ferritin", "Ferritin", "µg/L", 0, ("Ferritin",), {"µg/L": None}),
    Marker("glucose", "Glucose", "mmol/L", 1, ("Glucose",), {"mmol/L": None}),
]

# Flags with the same status are listed in this order.
MARKERS: dict[str, Marker] = {m.key: m for m in _MARKER_LIST}

_BY_ALIAS = {normalise_name(alias): m for m in _MARKER_LIST for alias in m.aliases}


def match_marker(name: str) -> Marker | None:
    return _BY_ALIAS.get(normalise_name(name))
