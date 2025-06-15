"""
Integration tests for basic game functionality
"""

import pytest
import subprocess
import sys
import os
import time
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from utils.config import Config


class TestBasicIntegration:
    """Integration tests for basic game functionality"""

    def test_config_validation(self):
        """Test configuration validation works"""
        # Should not raise any exceptions with default config
        assert Config.validate() == True

    def test_config_window_size(self):
        """Test window size configuration"""
        width, height = Config.get_window_size()
        assert width > 0
        assert height > 0
        assert isinstance(width, int)
        assert isinstance(height, int)

    def test_config_debug_mode(self):
        """Test debug mode configuration"""
        debug_mode = Config.is_debug()
        assert isinstance(debug_mode, bool)

    def test_main_script_test_mode(self):
        """Test main script runs in test mode without errors"""
        # Run main.py in test mode
        result = subprocess.run(
            [sys.executable, "main.py", "--test-mode"],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.path.dirname(__file__), "..", ".."),
        )

        assert result.returncode == 0
        assert "Test mode: Game initialized successfully" in result.stdout

    def test_main_script_help(self):
        """Test main script help output"""
        result = subprocess.run(
            [sys.executable, "main.py", "--help"],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.path.dirname(__file__), "..", ".."),
        )

        assert result.returncode == 0
        assert "Everyday Rhythm" in result.stdout
        assert "--debug" in result.stdout
        assert "--test-mode" in result.stdout

    @patch.dict(os.environ, {"GAME_WINDOW_WIDTH": "1024", "GAME_WINDOW_HEIGHT": "768"})
    def test_config_environment_override(self):
        """Test configuration can be overridden by environment variables"""
        # Reload config to pick up environment changes
        from importlib import reload
        from utils import config

        reload(config)

        # Check if environment variables are respected
        width, height = config.Config.get_window_size()
        assert width == 1024
        assert height == 768

    def test_requirements_file_exists(self):
        """Test requirements.txt file exists and contains expected packages"""
        requirements_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "requirements.txt"
        )
        assert os.path.exists(requirements_path)

        with open(requirements_path, "r") as f:
            content = f.read()
            assert "pygame" in content
            assert "python-dotenv" in content
            assert "pytest" in content

    def test_env_example_file_exists(self):
        """Test .env.example file exists"""
        env_example_path = os.path.join(
            os.path.dirname(__file__), "..", "..", ".env.example"
        )
        assert os.path.exists(env_example_path)

        with open(env_example_path, "r") as f:
            content = f.read()
            assert "AMAZON_Q_API_KEY" in content
            assert "GAME_WINDOW_WIDTH" in content
            assert "TARGET_FPS" in content
