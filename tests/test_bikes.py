"""Tests for the bikes module."""

import pytest
from bikes import (
    Bike,
    _catalog,
    list_bikes,
    filter_bikes,
    score_bike,
    recommend_bikes,
    summarize_bike,
)


class TestBikeCatalog:
    """Test bike catalog functionality."""

    def test_catalog_not_empty(self):
        """Test that the catalog contains bikes."""
        bikes = _catalog()
        assert len(bikes) > 0
        assert all(isinstance(bike, Bike) for bike in bikes)

    def test_bike_attributes(self):
        """Test that bikes have all required attributes."""
        bikes = _catalog()
        for bike in bikes:
            assert hasattr(bike, 'id')
            assert hasattr(bike, 'name')
            assert hasattr(bike, 'brand')
            assert hasattr(bike, 'category')
            assert hasattr(bike, 'price_usd')
            assert hasattr(bike, 'terrain')

    def test_list_bikes_returns_dicts(self):
        """Test that list_bikes returns dictionaries."""
        bikes = list_bikes()
        assert isinstance(bikes, list)
        assert all(isinstance(bike, dict) for bike in bikes)
        assert len(bikes) > 0


class TestFilterBikes:
    """Test bike filtering functionality."""

    def test_filter_by_price(self):
        """Test filtering bikes by maximum price."""
        filtered = filter_bikes(max_price=1000)
        assert all(bike.price_usd <= 1000 for bike in filtered)

    def test_filter_by_category(self):
        """Test filtering bikes by category."""
        filtered = filter_bikes(category="road")
        assert all(bike.category.lower() == "road" for bike in filtered)

    def test_filter_by_brand(self):
        """Test filtering bikes by brand."""
        filtered = filter_bikes(brand="Metro")
        assert all(bike.brand.lower() == "metro" for bike in filtered)

    def test_filter_by_terrain(self):
        """Test filtering bikes by terrain."""
        filtered = filter_bikes(terrain="urban")
        assert all("urban" in [t.lower() for t in bike.terrain] for bike in filtered)

    def test_filter_by_motorized(self):
        """Test filtering bikes by motorization."""
        # Test electric bikes
        electric = filter_bikes(motorized=True)
        assert all(bike.motor is not None for bike in electric)

        # Test non-electric bikes
        non_electric = filter_bikes(motorized=False)
        assert all(bike.motor is None for bike in non_electric)

    def test_filter_combinations(self):
        """Test filtering with multiple criteria."""
        filtered = filter_bikes(
            max_price=2000,
            category="mountain",
            motorized=False
        )
        for bike in filtered:
            assert bike.price_usd <= 2000
            assert bike.category.lower() == "mountain"
            assert bike.motor is None


class TestScoreBike:
    """Test bike scoring functionality."""

    def test_score_with_budget(self):
        """Test scoring with budget preference."""
        bikes = _catalog()
        prefs = {"budget": 1500}
        
        for bike in bikes:
            score = score_bike(bike, prefs)
            if bike.price_usd <= 1500:
                assert score > 0
            else:
                assert score < 0

    def test_score_with_category(self):
        """Test scoring with category preference."""
        bikes = _catalog()
        prefs = {"category": "road"}
        
        for bike in bikes:
            score = score_bike(bike, prefs)
            if bike.category.lower() == "road":
                assert score >= 3.0

    def test_score_with_terrain(self):
        """Test scoring with terrain preference."""
        bikes = _catalog()
        prefs = {"terrain": "urban"}
        
        for bike in bikes:
            score = score_bike(bike, prefs)
            if "urban" in [t.lower() for t in bike.terrain]:
                assert score >= 2.0

    def test_score_with_motorized(self):
        """Test scoring with motorization preference."""
        bikes = _catalog()
        prefs = {"motorized": True}
        
        for bike in bikes:
            score = score_bike(bike, prefs)
            if bike.motor is not None:
                assert score >= 2.0

    def test_score_with_lightweight(self):
        """Test scoring with lightweight preference."""
        bikes = _catalog()
        prefs = {"lightweight": True}
        
        for bike in bikes:
            score = score_bike(bike, prefs)
            if bike.weight_kg < 12.0:
                assert score > 0

    def test_score_with_brand(self):
        """Test scoring with brand preference."""
        bikes = _catalog()
        prefs = {"brand": "Metro"}
        
        for bike in bikes:
            score = score_bike(bike, prefs)
            if bike.brand.lower() == "metro":
                assert score >= 1.5


class TestRecommendBikes:
    """Test bike recommendation functionality."""

    def test_recommend_with_budget(self):
        """Test recommendations with budget constraint."""
        prefs = {"budget": 1000}
        recommendations = recommend_bikes(prefs, limit=3)
        
        assert len(recommendations) <= 3
        assert all(r["price_usd"] <= 1000 for r in recommendations)

    def test_recommend_with_category(self):
        """Test recommendations with category preference."""
        prefs = {"category": "mountain"}
        recommendations = recommend_bikes(prefs, limit=3)
        
        assert len(recommendations) <= 3
        assert all(r["category"].lower() == "mountain" for r in recommendations)

    def test_recommend_with_multiple_criteria(self):
        """Test recommendations with multiple preferences."""
        prefs = {
            "budget": 2000,
            "category": "hybrid",
            "terrain": "urban"
        }
        recommendations = recommend_bikes(prefs, limit=3)
        
        assert len(recommendations) <= 3
        for rec in recommendations:
            assert rec["price_usd"] <= 2000
            assert rec["category"].lower() == "hybrid"
            assert "urban" in [t.lower() for t in rec["terrain"]]

    def test_recommend_empty_prefs(self):
        """Test recommendations with empty preferences."""
        recommendations = recommend_bikes({}, limit=3)
        assert len(recommendations) <= 3

    def test_recommend_limit(self):
        """Test that recommendations respect the limit."""
        prefs = {"budget": 5000}
        recommendations = recommend_bikes(prefs, limit=1)
        assert len(recommendations) == 1


class TestSummarizeBike:
    """Test bike summarization functionality."""

    def test_summarize_bike_format(self):
        """Test that bike summaries are properly formatted."""
        bikes = list_bikes()
        for bike in bikes:
            summary = summarize_bike(bike)
            assert isinstance(summary, str)
            assert len(summary) > 0
            assert bike["name"] in summary
            assert bike["brand"] in summary
            assert str(bike["price_usd"]) in summary

    def test_summarize_electric_bike(self):
        """Test summarization of electric bikes."""
        electric_bikes = [b for b in list_bikes() if b.get("motor")]
        if electric_bikes:
            bike = electric_bikes[0]
            summary = summarize_bike(bike)
            assert bike["motor"] in summary
            if bike.get("battery_wh"):
                assert str(bike["battery_wh"]) in summary


class TestIntegration:
    """Integration tests for the bikes module."""

    def test_full_recommendation_flow(self):
        """Test the complete recommendation flow."""
        # User preferences
        prefs = {
            "budget": 1500,
            "category": "city",
            "terrain": "urban",
            "motorized": False
        }
        
        # Get recommendations
        recommendations = recommend_bikes(prefs, limit=3)
        
        # Verify recommendations
        assert len(recommendations) <= 3
        for rec in recommendations:
            # Check budget constraint
            assert rec["price_usd"] <= 1500
            # Check category
            assert rec["category"].lower() == "city"
            # Check terrain
            assert "urban" in [t.lower() for t in rec["terrain"]]
            # Check motorization
            assert rec.get("motor") is None

    def test_scoring_consistency(self):
        """Test that scoring is consistent across different calls."""
        bikes = _catalog()
        prefs = {"budget": 2000, "category": "road"}
        
        # Get scores for all bikes
        scores = [(bike, score_bike(bike, prefs)) for bike in bikes]
        
        # Verify that scores are consistent
        for bike, score in scores:
            assert score_bike(bike, prefs) == score
