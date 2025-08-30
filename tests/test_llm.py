"""Tests for the LLM module."""

import os
import pytest
from unittest.mock import Mock, patch
from llm import chat, _get_client


class TestLLMClient:
    """Test LLM client functionality."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm.OpenAI")
    def test_get_client_success(self, mock_openai):
        """Test successful client creation."""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        client = _get_client()
        
        mock_openai.assert_called_once_with(api_key="test-key")
        assert client == mock_client

    @patch.dict(os.environ, {}, clear=True)
    def test_get_client_no_api_key(self):
        """Test client creation without API key."""
        with pytest.raises(RuntimeError, match="OPENAI_API_KEY not set"):
            _get_client()

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm.OpenAI", None)
    def test_get_client_no_openai_package(self):
        """Test client creation without OpenAI package."""
        with pytest.raises(RuntimeError, match="openai package not installed"):
            _get_client()


class TestChatFunction:
    """Test chat function functionality."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm._get_client")
    def test_chat_success(self, mock_get_client):
        """Test successful chat completion."""
        # Mock the OpenAI client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ]
        
        result = chat(messages)
        
        assert result == "Test response"
        mock_client.chat.completions.create.assert_called_once()

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm._get_client")
    def test_chat_with_custom_model(self, mock_get_client):
        """Test chat with custom model."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [{"role": "user", "content": "Hello"}]
        
        chat(messages, model="gpt-4")
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["model"] == "gpt-4"

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "OPENAI_MODEL": "gpt-4"})
    @patch("llm._get_client")
    def test_chat_with_env_model(self, mock_get_client):
        """Test chat with model from environment."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [{"role": "user", "content": "Hello"}]
        
        chat(messages)
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["model"] == "gpt-4"

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm._get_client")
    def test_chat_with_custom_temperature(self, mock_get_client):
        """Test chat with custom temperature."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [{"role": "user", "content": "Hello"}]
        
        chat(messages, temperature=0.5)
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["temperature"] == 0.5

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm._get_client")
    def test_chat_with_custom_max_tokens(self, mock_get_client):
        """Test chat with custom max tokens."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [{"role": "user", "content": "Hello"}]
        
        chat(messages, max_output_tokens=1000)
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["max_tokens"] == 1000

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm._get_client")
    def test_chat_empty_response(self, mock_get_client):
        """Test chat with empty response."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = []
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [{"role": "user", "content": "Hello"}]
        
        result = chat(messages)
        
        assert result == ""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm._get_client")
    def test_chat_none_response(self, mock_get_client):
        """Test chat with None response."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = None
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [{"role": "user", "content": "Hello"}]
        
        result = chat(messages)
        
        assert result == ""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm._get_client")
    def test_chat_api_error(self, mock_get_client):
        """Test chat with API error."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_get_client.return_value = mock_client
        
        messages = [{"role": "user", "content": "Hello"}]
        
        with pytest.raises(Exception, match="API Error"):
            chat(messages)

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm._get_client")
    def test_chat_default_parameters(self, mock_get_client):
        """Test chat with default parameters."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [{"role": "user", "content": "Hello"}]
        
        chat(messages)
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["temperature"] == 0.2
        assert call_args[1]["max_tokens"] == 500

    def test_chat_messages_format(self):
        """Test that messages are passed correctly."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("llm._get_client") as mock_get_client:
                mock_client = Mock()
                mock_response = Mock()
                mock_response.choices = [Mock()]
                mock_response.choices[0].message.content = "Test response"
                mock_client.chat.completions.create.return_value = mock_response
                mock_get_client.return_value = mock_client
                
                messages = [
                    {"role": "system", "content": "You are helpful"},
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there"}
                ]
                
                chat(messages)
                
                call_args = mock_client.chat.completions.create.call_args
                assert call_args[1]["messages"] == messages


class TestIntegration:
    """Integration tests for LLM module."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm._get_client")
    def test_full_chat_flow(self, mock_get_client):
        """Test the complete chat flow."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "I can help you find a bike!"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [
            {"role": "system", "content": "You are a bike shopping assistant."},
            {"role": "user", "content": "I need a mountain bike under $1000"}
        ]
        
        result = chat(messages)
        
        assert result == "I can help you find a bike!"
        mock_client.chat.completions.create.assert_called_once()

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("llm._get_client")
    def test_chat_with_bike_context(self, mock_get_client):
        """Test chat with bike-specific context."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Here are some great mountain bikes under $1000"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        messages = [
            {"role": "system", "content": "You help users find bikes based on their preferences."},
            {"role": "user", "content": "I want a mountain bike for trail riding"},
            {"role": "system", "content": "Available bikes: [bike1, bike2, bike3]"}
        ]
        
        result = chat(messages)
        
        assert "mountain bikes" in result.lower()
        call_args = mock_client.chat.completions.create.call_args
        assert len(call_args[1]["messages"]) == 3
