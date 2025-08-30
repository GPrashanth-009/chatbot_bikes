"""Pytest configuration and common fixtures."""

import pytest
import os
from unittest.mock import Mock, patch


@pytest.fixture(autouse=True)
def mock_openai_api_key():
    """Mock OpenAI API key for all tests."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        yield


@pytest.fixture
def sample_bike_data():
    """Sample bike data for testing."""
    return {
        "id": "test-bike-1",
        "name": "Test Mountain Bike",
        "brand": "TestBrand",
        "category": "mountain",
        "price_usd": 1200,
        "terrain": ["trail", "mountain"],
        "weight_kg": 14.5,
        "motor": None,
        "battery_wh": None,
        "frame_material": "aluminum",
        "wheel_size": "29\"",
        "gears": "21-speed",
        "brakes": "disc",
        "suspension": "front",
        "description": "A great test mountain bike for trail riding."
    }


@pytest.fixture
def sample_user_preferences():
    """Sample user preferences for testing."""
    return {
        "budget": 1500,
        "category": "mountain",
        "terrain": "trail",
        "brand": "TestBrand",
        "motorized": False,
        "lightweight": True
    }


@pytest.fixture
def sample_chat_messages():
    """Sample chat messages for testing."""
    return [
        {"role": "system", "content": "You are a helpful bike shopping assistant."},
        {"role": "user", "content": "I need a mountain bike under $1500"},
        {"role": "assistant", "content": "I can help you find a great mountain bike!"}
    ]


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch("llm.OpenAI") as mock_openai:
        mock_client = Mock()
        mock_openai.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_streamlit():
    """Mock Streamlit for testing."""
    with patch("streamlit_app.st") as mock_st:
        yield mock_st


@pytest.fixture(scope="session")
def test_environment():
    """Set up test environment variables."""
    original_env = os.environ.copy()
    
    # Set test environment variables
    test_env = {
        "OPENAI_API_KEY": "test-key-12345",
        "OPENAI_MODEL": "gpt-3.5-turbo",
        "STREAMLIT_SERVER_PORT": "8501",
        "STREAMLIT_SERVER_ADDRESS": "localhost"
    }
    
    os.environ.update(test_env)
    
    yield test_env
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    for item in items:
        # Mark tests based on their location
        if "test_" in item.nodeid and "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "test_" in item.nodeid:
            item.add_marker(pytest.mark.unit)
