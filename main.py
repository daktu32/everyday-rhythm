#!/usr/bin/env python3
"""
Everyday Rhythm - Main Entry Point

A simple rhythm game using Pygame with Amazon Q Developer integration
for automatic stage generation.
"""

import sys
import argparse
from src.core.game_manager import GameManager
from src.utils.config import Config


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Everyday Rhythm - Simple Rhythm Game')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--stage', type=str, help='Load specific stage file')
    parser.add_argument('--test-mode', action='store_true', help='Run in test mode')
    return parser.parse_args()


def main():
    """Main game entry point"""
    args = parse_arguments()
    
    # Override debug mode if specified
    if args.debug:
        import os
        os.environ['DEBUG_MODE'] = 'true'
        # Reload config to pick up the change
        Config.DEBUG_MODE = True
    
    try:
        # Validate configuration
        Config.validate()
        
        if Config.is_debug():
            print("=== Everyday Rhythm ===")
            print(f"Debug mode: {Config.DEBUG_MODE}")
            print(f"Window size: {Config.get_window_size()}")
            print(f"Target FPS: {Config.TARGET_FPS}")
            print(f"Audio buffer: {Config.AUDIO_BUFFER_SIZE}")
            if Config.AMAZON_Q_API_KEY:
                print("Amazon Q API: Configured")
            else:
                print("Amazon Q API: Not configured")
            print("========================")
        
        # Create and run game
        game_manager = GameManager()
        
        if args.test_mode:
            print("Test mode: Game initialized successfully")
            return 0
        
        # Start the game
        game_manager.run()
        
        if Config.is_debug():
            print("Game ended normally")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        return 0
    except Exception as e:
        print(f"Error starting game: {e}")
        if Config.is_debug():
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
