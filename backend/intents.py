"""Minimal intent parsing to extract buyer preferences from free text."""

import re
from typing import Dict, Any


CATEGORY_KEYWORDS = {
    "road": ["road", "racing"],
    "mountain": ["mtb", "mountain", "trail", "downhill", "enduro"],
    "hybrid": ["hybrid", "fitness"],
    "gravel": ["gravel"],
    "city": ["city", "commute", "commuter", "urban"],
    "e-bike": ["e-bike", "ebike", "electric"],
}

TERRAIN_KEYWORDS = {
    "paved": ["paved", "tarmac", "asphalt", "road"],
    "gravel": ["gravel"],
    "trail": ["trail", "singletrack", "mtb", "mountain"],
    "urban": ["city", "commute", "urban"],
}


def parse_preferences(text: str) -> Dict[str, Any]:
    """Extracts a small set of preferences from a user utterance.

    Returns keys among: budget (int), category (str), terrain (str), brand (str),
    motorized (bool), lightweight (bool)
    """
    prefs: Dict[str, Any] = {}
    t = text.lower()

    # Budget like: under 1500, max 2k, $1000, 1,500, 2k, 2,500 dollars
    money_pattern = re.search(r"(\$?\s*(\d{1,3}(?:[\.,]\d{3})*|\d+)(?:\s*(k|k\+))?)|((\d+(?:[\.,]\d+)?)\s*k)", t)
    if money_pattern:
        raw = money_pattern.group(0)
        digits = re.findall(r"\d+(?:[\.,]\d+)?", raw)
        if digits:
            number = digits[0].replace(",", "").replace(".", "")
            try:
                value = int(number)
                if "k" in raw:
                    value *= 1000
                prefs["budget"] = value
            except ValueError:
                pass
    if any(x in t for x in ["under ", "below ", "max "]):
        # heuristic: budget already covered; nothing extra
        pass

    # Category
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(k in t for k in kws):
            prefs["category"] = cat
            break

    # Terrain
    for terr, kws in TERRAIN_KEYWORDS.items():
        if any(k in t for k in kws):
            prefs["terrain"] = terr
            break

    # Brand
    brand_match = re.search(r"\b(giant|trek|specialized|canyon|cannondale|metro|alpine|peak|volt|terra)\b", t)
    if brand_match:
        prefs["brand"] = brand_match.group(1).title()

    # Motorized intent
    if any(x in t for x in ["e-bike", "ebike", "electric", "motor", "battery", "assist"]):
        prefs["motorized"] = True
    if any(x in t for x in ["non-electric", "acoustic", "without motor", "no motor"]):
        prefs["motorized"] = False

    # Lightweight preference
    if any(x in t for x in ["lightweight", "lighter", "light weight", "as light as"]):
        prefs["lightweight"] = True

    return prefs


