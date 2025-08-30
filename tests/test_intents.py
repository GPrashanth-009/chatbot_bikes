"""Tests for the intents module."""

import pytest
from intents import parse_preferences, CATEGORY_KEYWORDS, TERRAIN_KEYWORDS


class TestParsePreferences:
    """Test preference parsing functionality."""

    def test_parse_budget(self):
        """Test parsing budget from various formats."""
        test_cases = [
            ("I want a bike under $1000", {"budget": 1000}),
            ("My budget is 1500 dollars", {"budget": 1500}),
            ("Looking for something around 2k", {"budget": 2000}),
            ("Maximum 2500", {"budget": 2500}),
            ("Below 800", {"budget": 800}),
            ("Around 1,500", {"budget": 1500}),
            ("Under 3k", {"budget": 3000}),
        ]
        
        for text, expected in test_cases:
            result = parse_preferences(text)
            assert result.get("budget") == expected["budget"]

    def test_parse_category(self):
        """Test parsing bike categories."""
        test_cases = [
            ("I want a road bike", {"category": "road"}),
            ("Looking for mountain bikes", {"category": "mountain"}),
            ("Need a hybrid", {"category": "hybrid"}),
            ("Gravel bike please", {"category": "gravel"}),
            ("City bike for commuting", {"category": "city"}),
            ("Electric bike", {"category": "e-bike"}),
            ("E-bike for urban riding", {"category": "e-bike"}),
        ]
        
        for text, expected in test_cases:
            result = parse_preferences(text)
            assert result.get("category") == expected["category"]

    def test_parse_terrain(self):
        """Test parsing terrain preferences."""
        test_cases = [
            ("For paved roads", {"terrain": "paved"}),
            ("Gravel trails", {"terrain": "gravel"}),
            ("Mountain trails", {"terrain": "trail"}),
            ("Urban commuting", {"terrain": "urban"}),
            ("City riding", {"terrain": "urban"}),
        ]
        
        for text, expected in test_cases:
            result = parse_preferences(text)
            assert result.get("terrain") == expected["terrain"]

    def test_parse_brand(self):
        """Test parsing brand preferences."""
        test_cases = [
            ("I like Metro bikes", {"brand": "Metro"}),
            ("Prefer Alpine", {"brand": "Alpine"}),
            ("Looking for Peak bikes", {"brand": "Peak"}),
            ("Volt brand", {"brand": "Volt"}),
            ("Terra bikes", {"brand": "Terra"}),
        ]
        
        for text, expected in test_cases:
            result = parse_preferences(text)
            assert result.get("brand") == expected["brand"]

    def test_parse_motorized(self):
        """Test parsing motorization preferences."""
        test_cases = [
            ("Electric bike", {"motorized": True}),
            ("E-bike", {"motorized": True}),
            ("With motor", {"motorized": True}),
            ("Battery assist", {"motorized": True}),
            ("Non-electric", {"motorized": False}),
            ("Without motor", {"motorized": False}),
            ("Acoustic bike", {"motorized": False}),
        ]
        
        for text, expected in test_cases:
            result = parse_preferences(text)
            assert result.get("motorized") == expected["motorized"]

    def test_parse_lightweight(self):
        """Test parsing lightweight preferences."""
        test_cases = [
            ("Lightweight bike", {"lightweight": True}),
            ("As light as possible", {"lightweight": True}),
            ("Lighter weight", {"lightweight": True}),
        ]
        
        for text, expected in test_cases:
            result = parse_preferences(text)
            assert result.get("lightweight") == expected["lightweight"]

    def test_parse_multiple_preferences(self):
        """Test parsing multiple preferences from one text."""
        text = "I want a lightweight mountain bike under $2000 for trails"
        result = parse_preferences(text)
        
        assert result.get("budget") == 2000
        assert result.get("category") == "mountain"
        assert result.get("terrain") == "trail"
        assert result.get("lightweight") is True

    def test_parse_complex_query(self):
        """Test parsing a complex user query."""
        text = "Looking for an electric Metro bike around 3k for urban commuting"
        result = parse_preferences(text)
        
        assert result.get("budget") == 3000
        assert result.get("category") == "e-bike"
        assert result.get("brand") == "Metro"
        assert result.get("terrain") == "urban"
        assert result.get("motorized") is True

    def test_parse_no_preferences(self):
        """Test parsing text with no preferences."""
        text = "Hello, can you help me?"
        result = parse_preferences(text)
        
        assert result == {}

    def test_parse_case_insensitive(self):
        """Test that parsing is case insensitive."""
        text = "ROAD BIKE UNDER $1000"
        result = parse_preferences(text)
        
        assert result.get("category") == "road"
        assert result.get("budget") == 1000

    def test_parse_budget_edge_cases(self):
        """Test budget parsing edge cases."""
        test_cases = [
            ("$500", {"budget": 500}),
            ("1,000", {"budget": 1000}),
            ("2.5k", {"budget": 2500}),
            ("1.5k", {"budget": 1500}),
        ]
        
        for text, expected in test_cases:
            result = parse_preferences(text)
            assert result.get("budget") == expected["budget"]

    def test_parse_invalid_budget(self):
        """Test parsing invalid budget formats."""
        text = "Budget is abc dollars"
        result = parse_preferences(text)
        
        assert "budget" not in result

    def test_parse_category_keywords(self):
        """Test that all category keywords are recognized."""
        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                text = f"I want a {keyword} bike"
                result = parse_preferences(text)
                assert result.get("category") == category

    def test_parse_terrain_keywords(self):
        """Test that all terrain keywords are recognized."""
        for terrain, keywords in TERRAIN_KEYWORDS.items():
            for keyword in keywords:
                text = f"For {keyword} riding"
                result = parse_preferences(text)
                assert result.get("terrain") == terrain

    def test_parse_preference_priority(self):
        """Test that the first matching category is selected."""
        text = "I want a mountain road bike"  # Contains both mountain and road
        result = parse_preferences(text)
        
        # Should match the first category found (mountain comes before road in dict)
        assert result.get("category") == "mountain"

    def test_parse_empty_string(self):
        """Test parsing empty string."""
        result = parse_preferences("")
        assert result == {}

    def test_parse_whitespace_only(self):
        """Test parsing whitespace-only string."""
        result = parse_preferences("   \n\t   ")
        assert result == {}


class TestIntegration:
    """Integration tests for preference parsing."""

    def test_real_world_queries(self):
        """Test parsing realistic user queries."""
        queries = [
            "I need a bike for commuting in the city, budget around $800",
            "Looking for a mountain bike under 1500 for trail riding",
            "Electric bike for urban use, max 3000",
            "Lightweight road bike around 2k",
            "Hybrid bike for paved roads, budget 1200",
        ]
        
        for query in queries:
            result = parse_preferences(query)
            # Should extract at least one preference
            assert len(result) > 0

    def test_preference_consistency(self):
        """Test that parsing is consistent across multiple calls."""
        text = "Mountain bike under $2000 for trails"
        
        result1 = parse_preferences(text)
        result2 = parse_preferences(text)
        
        assert result1 == result2
