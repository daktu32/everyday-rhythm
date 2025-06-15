"""
Configuration management for Everyday Rhythm
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for game settings"""

    # Amazon Q Developer API
    AMAZON_Q_API_KEY: Optional[str] = os.getenv("AMAZON_Q_API_KEY")
    AMAZON_Q_ENDPOINT: str = os.getenv(
        "AMAZON_Q_ENDPOINT", "https://api.amazonq.developer"
    )

    # Game Configuration
    GAME_WINDOW_WIDTH: int = int(os.getenv("GAME_WINDOW_WIDTH", "800"))
    GAME_WINDOW_HEIGHT: int = int(os.getenv("GAME_WINDOW_HEIGHT", "600"))
    AUDIO_BUFFER_SIZE: int = int(os.getenv("AUDIO_BUFFER_SIZE", "1024"))
    TARGET_FPS: int = int(os.getenv("TARGET_FPS", "60"))

    # Development
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration settings"""
        errors = []

        # Check required settings
        if cls.GAME_WINDOW_WIDTH <= 0:
            errors.append("GAME_WINDOW_WIDTH must be positive")

        if cls.GAME_WINDOW_HEIGHT <= 0:
            errors.append("GAME_WINDOW_HEIGHT must be positive")

        if cls.TARGET_FPS <= 0:
            errors.append("TARGET_FPS must be positive")

        if cls.AUDIO_BUFFER_SIZE <= 0:
            errors.append("AUDIO_BUFFER_SIZE must be positive")

        # Warn about missing API key (not required for basic functionality)
        if not cls.AMAZON_Q_API_KEY and cls.DEBUG_MODE:
            print("Warning: AMAZON_Q_API_KEY not set. Stage generation will not work.")

        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")

        return True

    @classmethod
    def get_window_size(cls) -> tuple[int, int]:
        """Get window dimensions as tuple"""
        return (cls.GAME_WINDOW_WIDTH, cls.GAME_WINDOW_HEIGHT)

    @classmethod
    def is_debug(cls) -> bool:
        """Check if debug mode is enabled"""
        return cls.DEBUG_MODE
