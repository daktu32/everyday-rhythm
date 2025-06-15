#!/usr/bin/env python3
"""
Everyday Rhythm - Main Entry Point

A simple rhythm game using Pygame with Amazon Q Developer integration
for automatic stage generation.
"""

import sys
import os
import argparse
from src.core.game_manager import GameManager
from src.utils.config import Config


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Everyday Rhythm - Simple Rhythm Game')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--stage', type=str, help='Load specific stage file')
    parser.add_argument('--test-mode', action='store_true', help='Run in test mode')
    parser.add_argument('--audio', type=str, help='Load and play audio file for testing')
    parser.add_argument('--volume', type=float, default=0.7, help='Set audio volume (0.0-1.0)')
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
            if args.audio and os.path.exists(args.audio):
                print(f"Testing audio file: {args.audio}")
                if game_manager.load_audio(args.audio):
                    print("Audio loaded successfully")
                    game_manager.set_volume(args.volume)
                    print(f"Volume set to: {args.volume}")
                else:
                    print("Failed to load audio file")
            return 0
        
        # Load audio file if provided
        if args.audio:
            import os  # Ensure os is available in this scope
            if os.path.exists(args.audio):
                print(f"Loading audio file: {args.audio}")
                if game_manager.load_audio(args.audio):
                    game_manager.set_volume(args.volume)
                    print("Audio loaded, starting rhythm game...")
                    # Start rhythm game mode automatically
                    if game_manager.start_rhythm_game(args.audio):
                        print("Rhythm game mode started!")
                        print("Controls:")
                        print("  SPACE: Hit notes")
                        print("  ESC: Exit rhythm game")
                    else:
                        print("Failed to start rhythm game mode")
                        game_manager.play_audio()
                        print("Audio playback started. Press SPACE to pause/resume, ESC to quit.")
                else:
                    print(f"Failed to load audio file: {args.audio}")
            else:
                print(f"Audio file not found: {args.audio}")
        else:
            print("No audio file provided. Starting in debug mode.")
            print("Supported audio formats: WAV, MP3, OGG, FLAC")
            print("Load an audio file with --audio <file> to play the rhythm game.")
        
        print("About to start game loop...")
        # Start the game
        game_manager.run()
        print("Game loop ended")
        
        if Config.is_debug():
            print("Game ended normally")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        return 0
    except Exception as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
