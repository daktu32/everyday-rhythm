#!/usr/bin/env python3
"""
Simple test for rhythm game
"""
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from core.game_manager import GameManager
from utils.config import Config

def main():
    """Test rhythm game"""
    # Enable debug mode
    os.environ["DEBUG"] = "1"
    
    print("=== Rhythm Game Test ===")
    
    try:
        # Initialize game manager
        game_manager = GameManager()
        print("GameManager initialized")
        
        # Load audio
        audio_file = "tests/fixtures/test_medium.wav"
        if os.path.exists(audio_file):
            print(f"Loading audio: {audio_file}")
            if game_manager.load_audio(audio_file):
                print("Audio loaded successfully")
                
                # Start rhythm game
                print("Starting rhythm game...")
                if game_manager.start_rhythm_game(audio_file):
                    print("Rhythm game started!")
                    print(f"Notes: {len(game_manager.rhythm_engine.notes)}")
                    print("Starting game loop...")
                    
                    # Run for a short time
                    import time
                    start_time = time.time()
                    while time.time() - start_time < 3.0 and game_manager.running:
                        game_manager.handle_events()
                        game_manager.update()
                        game_manager.render()
                        game_manager.tick()
                    
                    print("Test completed")
                else:
                    print("Failed to start rhythm game")
            else:
                print("Failed to load audio")
        else:
            print(f"Audio file not found: {audio_file}")
        
        game_manager.cleanup()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
