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
from audio.audio_manager import AudioManager  # noqa: E402


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

        # Audio system
        self.audio_manager = AudioManager()

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
                    # Toggle audio playback
                    if self.audio_manager.current_music:
                        if self.audio_manager.is_playing():
                            self.audio_manager.pause_music()
                            if Config.is_debug():
                                print("Audio paused")
                        else:
                            if self.audio_manager.is_paused:
                                self.audio_manager.resume_music()
                                if Config.is_debug():
                                    print("Audio resumed")
                            else:
                                self.audio_manager.play_music()
                                if Config.is_debug():
                                    print("Audio started")
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

        # Render audio info if available
        if Config.is_debug() and self.audio_manager.current_music:
            self._render_debug_info()

        # Update display
        pygame.display.flip()

    def _render_debug_info(self) -> None:
        """Render debug information"""
        font = pygame.font.Font(None, 24)
        y_offset = 10

        # Audio info
        audio_info = self.audio_manager.get_audio_info()
        if audio_info:
            info_lines = [
                f"Audio: {os.path.basename(audio_info.get('file_path', 'None'))}",
                f"Time: {audio_info.get('current_time_ms', 0):.0f}ms / {audio_info.get('duration_ms', 0):.0f}ms",
                f"Playing: {audio_info.get('is_playing', False)}",
                f"Volume: {audio_info.get('volume', 0):.1f}",
            ]

            for line in info_lines:
                text = font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (10, y_offset))
                y_offset += 25

    def tick(self) -> None:
        """Maintain target frame rate"""
        self.clock.tick(Config.TARGET_FPS)

    def cleanup(self) -> None:
        """Clean up resources"""
        if Config.is_debug():
            print("Cleaning up game resources...")

        # Cleanup audio
        if hasattr(self, 'audio_manager'):
            self.audio_manager.cleanup()

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

    def load_audio(self, file_path: str) -> bool:
        """Load audio file for playback"""
        return self.audio_manager.load_music(file_path)

    def play_audio(self) -> None:
        """Start audio playback"""
        self.audio_manager.play_music()

    def stop_audio(self) -> None:
        """Stop audio playback"""
        self.audio_manager.stop_music()

    def set_volume(self, volume: float) -> None:
        """Set audio volume (0.0 - 1.0)"""
        self.audio_manager.set_volume(volume)
