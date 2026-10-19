"""Fully synthetic product, supplier and operational reference data."""
from __future__ import annotations

from dataclasses import dataclass

PRODUCTS = {
    "SOLAR": {"name": "Solar charging modules", "base_daily": 34, "inventory": 165, "unit_value": 74},
    "COLD": {"name": "Cold-chain temperature sensors", "base_daily": 23, "inventory": 108, "unit_value": 122},
    "FILTER": {"name": "Industrial water filters", "base_daily": 39, "inventory": 230, "unit_value": 48},
    "BATTERY": {"name": "Backup battery cells", "base_daily": 31, "inventory": 185, "unit_value": 87},
    "TRACKER": {"name": "Shipment GPS trackers", "base_daily": 25, "inventory": 122, "unit_value": 102},
    "MEDKIT": {"name": "Emergency medical kits", "base_daily": 27, "inventory": 142, "unit_value": 79},
}

@dataclass(frozen=True)
class Supplier:
    code: str
    name: str
    cost_factor: float
    capacity: int  # total units available during a 21-day planning horizon
    lead_days: int
    delay_probability: float
    kg_co2_per_unit: float

SUPPLIERS = (
    Supplier("ATLAS", "Atlas Freight", 0.91, 1150, 15, 0.28, 6.5),
    Supplier("NOVA", "Nova Distribution", 1.03, 1400, 6, 0.08, 3.8),
    Supplier("CEDAR", "Cedar Low-Carbon", 1.12, 1100, 9, 0.06, 1.4),
    Supplier("RAPID", "RapidBridge", 1.21, 900, 3, 0.04, 7.8),
)

# Not every supplier is approved for every SKU.
ELIGIBILITY = {
    "SOLAR": ("ATLAS", "NOVA", "CEDAR"),
    "COLD": ("NOVA", "CEDAR", "RAPID"),
    "FILTER": ("ATLAS", "NOVA", "RAPID"),
    "BATTERY": ("ATLAS", "CEDAR", "RAPID"),
    "TRACKER": ("ATLAS", "NOVA", "CEDAR", "RAPID"),
    "MEDKIT": ("NOVA", "CEDAR", "RAPID"),
}

INVENTORY = {code: spec["inventory"] for code, spec in PRODUCTS.items()}
