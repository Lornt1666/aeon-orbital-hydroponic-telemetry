"""Closed-loop hydroponic telemetry helpers. Habitat sketch, not a flight system."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NutrientReading:
    reservoir_id: str
    ec_ms_cm: float
    ph: float
    temp_c: float
    light_ppfd: float


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def nutrient_setpoints() -> dict[str, tuple[float, float]]:
    return {
        "ec_ms_cm": (1.2, 2.4),
        "ph": (5.5, 6.5),
        "temp_c": (18.0, 24.0),
        "light_ppfd": (200.0, 600.0),
    }


def classify(reading: NutrientReading) -> dict[str, str]:
    bounds = nutrient_setpoints()
    out = {}
    mapping = {
        "ec_ms_cm": reading.ec_ms_cm,
        "ph": reading.ph,
        "temp_c": reading.temp_c,
        "light_ppfd": reading.light_ppfd,
    }
    for key, value in mapping.items():
        lo, hi = bounds[key]
        if value < lo:
            out[key] = "low"
        elif value > hi:
            out[key] = "high"
        else:
            out[key] = "ok"
    return out


def lighting_duty_cycle(ppfd: float, target: float = 400.0) -> float:
    if target <= 0:
        raise ValueError("target must be positive")
    return clamp(ppfd / target, 0.0, 1.0)
