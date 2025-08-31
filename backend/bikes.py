"""Bike catalog and search helpers.

This module defines a small in-memory catalog of bikes available on the market
and provides helper functions to query and score them based on user needs.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


@dataclass
class Bike:
    id: str
    name: str
    brand: str
    category: str  # e.g., "road", "mountain", "hybrid", "e-bike", "gravel", "city"
    frame: str  # e.g., "aluminum", "carbon", "steel"
    groupset: str  # e.g., "Shimano 105", "SRAM GX", "MicroSHIFT"
    wheel_size: str  # e.g., "700c", "29", "27.5"
    motor: Optional[str]  # e.g., "Bosch", None
    battery_wh: Optional[int]
    weight_kg: float
    price_usd: int
    suspension: str  # e.g., "rigid", "front", "full"
    brakes: str  # e.g., "disc", "rim"
    terrain: List[str]  # e.g., ["paved", "gravel", "trail", "urban"]


def _catalog() -> List[Bike]:
    """Returns a static catalog. In real apps, you'd load from a DB/API."""
    return [
        Bike(
            id="r1",
            name="Alpine Road 105",
            brand="Alpine",
            category="road",
            frame="carbon",
            groupset="Shimano 105",
            wheel_size="700c",
            motor=None,
            battery_wh=None,
            weight_kg=8.4,
            price_usd=2499,
            suspension="rigid",
            brakes="disc",
            terrain=["paved", "urban"],
        ),
        Bike(
            id="m1",
            name="Peak Trail GX",
            brand="Peak",
            category="mountain",
            frame="aluminum",
            groupset="SRAM GX",
            wheel_size="29",
            motor=None,
            battery_wh=None,
            weight_kg=13.2,
            price_usd=1999,
            suspension="full",
            brakes="disc",
            terrain=["trail", "gravel"],
        ),
        Bike(
            id="h1",
            name="Metro Hybrid 2",
            brand="Metro",
            category="hybrid",
            frame="aluminum",
            groupset="Shimano Altus",
            wheel_size="700c",
            motor=None,
            battery_wh=None,
            weight_kg=12.1,
            price_usd=799,
            suspension="front",
            brakes="disc",
            terrain=["urban", "paved", "gravel"],
        ),
        Bike(
            id="e1",
            name="Volt City E-Step",
            brand="Volt",
            category="e-bike",
            frame="aluminum",
            groupset="Shimano Deore",
            wheel_size="700c",
            motor="Bosch",
            battery_wh=500,
            weight_kg=21.0,
            price_usd=2899,
            suspension="front",
            brakes="disc",
            terrain=["urban", "paved"],
        ),
        Bike(
            id="g1",
            name="Terra Gravel Rival",
            brand="Terra",
            category="gravel",
            frame="carbon",
            groupset="SRAM Rival",
            wheel_size="700c",
            motor=None,
            battery_wh=None,
            weight_kg=9.2,
            price_usd=2899,
            suspension="rigid",
            brakes="disc",
            terrain=["gravel", "paved"],
        ),
        Bike(
            id="c1",
            name="City Commuter 8",
            brand="Metro",
            category="city",
            frame="steel",
            groupset="MicroSHIFT Advent",
            wheel_size="700c",
            motor=None,
            battery_wh=None,
            weight_kg=13.8,
            price_usd=599,
            suspension="rigid",
            brakes="rim",
            terrain=["urban", "paved"],
        ),
        Bike(
            id="m2",
            name="Peak Trail Deore",
            brand="Peak",
            category="mountain",
            frame="aluminum",
            groupset="Shimano Deore",
            wheel_size="27.5",
            motor=None,
            battery_wh=None,
            weight_kg=13.9,
            price_usd=1299,
            suspension="front",
            brakes="disc",
            terrain=["trail", "gravel"],
        ),
    ]


def list_bikes() -> List[Dict[str, Any]]:
    return [asdict(b) for b in _catalog()]


def filter_bikes(
    max_price: Optional[int] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    terrain: Optional[str] = None,
    motorized: Optional[bool] = None,
) -> List[Bike]:
    bikes = _catalog()
    results: List[Bike] = []
    for bike in bikes:
        if max_price is not None and bike.price_usd > max_price:
            continue
        if category is not None and bike.category.lower() != category.lower():
            continue
        if brand is not None and bike.brand.lower() != brand.lower():
            continue
        if terrain is not None and terrain.lower() not in [t.lower() for t in bike.terrain]:
            continue
        if motorized is not None:
            if motorized and bike.motor is None:
                continue
            if not motorized and bike.motor is not None:
                continue
        results.append(bike)
    return results


def score_bike(bike: Bike, prefs: Dict[str, Any]) -> float:
    """Heuristic score: higher is better."""
    score = 0.0
    budget = prefs.get("budget")
    if isinstance(budget, (int, float)):
        # Reward fitting under budget; larger remaining budget gives tiny bonus
        if bike.price_usd <= budget:
            score += 3.0
            score += max(0.0, (budget - bike.price_usd) / max(budget, 1))
        else:
            score -= 2.0

    desired_category = prefs.get("category")
    if desired_category and bike.category.lower() == str(desired_category).lower():
        score += 3.0

    desired_terrain = prefs.get("terrain")
    if desired_terrain and str(desired_terrain).lower() in [t.lower() for t in bike.terrain]:
        score += 2.0

    motorized = prefs.get("motorized")
    if motorized is True and bike.motor is not None:
        score += 2.0
    if motorized is False and bike.motor is None:
        score += 1.0

    weight_pref = prefs.get("lightweight")
    if weight_pref is True:
        score += max(0.0, 12.0 - bike.weight_kg) * 0.2

    brand_pref = prefs.get("brand")
    if brand_pref and bike.brand.lower() == str(brand_pref).lower():
        score += 1.5

    return score


def recommend_bikes(prefs: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
    candidates = filter_bikes(
        max_price=prefs.get("budget"),
        category=prefs.get("category"),
        brand=prefs.get("brand"),
        terrain=prefs.get("terrain"),
        motorized=prefs.get("motorized"),
    )
    if not candidates:
        candidates = _catalog()
    ranked = sorted(candidates, key=lambda b: score_bike(b, prefs), reverse=True)
    return [asdict(b) for b in ranked[:limit]]


def summarize_bike(b: Dict[str, Any]) -> str:
    bits = [
        f"{b['name']} by {b['brand']} ({b['category']})",
        f"${b['price_usd']}",
        f"{b['frame']} frame",
        f"{b['groupset']}",
        f"{b['wheel_size']} wheels",
        f"{b['suspension']} suspension",
        f"{b['brakes']} brakes",
    ]
    if b.get("motor"):
        bits.append(f"motor: {b['motor']} {b.get('battery_wh', '')}Wh")
    return ", ".join([str(x) for x in bits if str(x).strip()])


