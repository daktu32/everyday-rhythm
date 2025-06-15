"""
GameManager - Core game state management and main game loop
"""

import pygame
import sys
import os

# Add src to path for imports (must be before local imports)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Local imports after path setup
from utils.config import Config  # noqa: E402


class GameManager:
    """Manages the main game loop and core game state"""

    def __init__(self):
        """Initialize the game manager"""
        # Initialize pygame
        pygame.init()
        pygame.mixer.init(buffer=Config.AUDIO_BUFFER_SIZE)

        # Create game window
        self.screen = pygame.display.set_mode(Config.get_window_size())
        pygame.display.set_caption("Everyday Rhythm")

        # Game state
        self.running = False
        self.clock = pygame.time.Clock()

        # Debug info
        if Config.is_debug():
            print(
                f"Game initialized - Window: {Config.get_window_size()}, "
                f"FPS: {Config.TARGET_FPS}"
            )

    def run(self) -> None:
        """Main game loop"""
        self.running = True

        if Config.is_debug():
            print("Starting game loop...")

        try:
            while self.running:
                # Handle events
                space_pressed = self.handle_events()

                # Update game state
                self.update()

                # Render frame
                self.render()

                # Maintain target FPS
                self.tick()

                # Debug: Log space key presses
                if space_pressed and Config.is_debug():
                    print("Space key pressed!")

        except Exception as e:
            print(f"Game loop error: {e}")
            if Config.is_debug():
                raise
        finally:
            self.cleanup()

    def handle_events(self) -> bool:
        """Handle pygame events"""
        space_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

        return space_pressed

    def update(self) -> None:
        """Update game state"""
        # Placeholder for game logic updates
        pass

    def render(self) -> None:
        """Render the current frame"""
        # Clear screen with black background
        self.screen.fill((0, 0, 0))

        # Placeholder for game rendering

        # Update display
        pygame.display.flip()

    def tick(self) -> None:
        """Maintain target frame rate"""
        self.clock.tick(Config.TARGET_FPS)

    def cleanup(self) -> None:
        """Clean up resources"""
        if Config.is_debug():
            print("Cleaning up game resources...")

        pygame.quit()

    def get_fps(self) -> float:
        """Get current FPS"""
        return self.clock.get_fps()

    def is_running(self) -> bool:
        """Check if game is currently running"""
        return self.running

    def stop(self) -> None:
        """Stop the game loop"""
        self.running = False
