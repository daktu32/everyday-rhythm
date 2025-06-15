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
from audio.audio_analyzer import AudioAnalyzer  # noqa: E402
from core.rhythm_engine import RhythmEngine  # noqa: E402
from ui.ui_renderer import UIRenderer  # noqa: E402


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
        self.audio_analyzer = AudioAnalyzer()

        # Rhythm game system
        self.rhythm_engine = RhythmEngine(self.audio_manager, self.audio_analyzer)
        self.ui_renderer = UIRenderer(self.screen, Config())
        
        # Game state
        self.current_music_name = "No Music"
        self.last_judgment_result = None
        self.paused = False

        # Game mode
        self.in_rhythm_mode = False

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
            print(f"Initial rhythm mode: {self.in_rhythm_mode}")

        try:
            frame_count = 0
            while self.running:
                # Handle events
                space_pressed = self.handle_events()

                # Update game state
                self.update()

                # Render frame
                self.render()

                # Maintain target FPS
                self.tick()

                # Debug: Log first few frames
                frame_count += 1
                if Config.is_debug() and frame_count <= 5:
                    print(f"Frame {frame_count}: running={self.running}, rhythm_mode={self.in_rhythm_mode}")

                # Debug: Log space key presses
                if space_pressed and Config.is_debug() and not self.in_rhythm_mode:
                    print("Space key pressed!")

        except Exception as e:
            print(f"Game loop error: {e}")
            if Config.is_debug():
                raise
        finally:
            if Config.is_debug():
                print("Game loop ended")
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
                    if self.in_rhythm_mode:
                        # Handle rhythm game input
                        current_time = self.audio_manager.get_current_time()
                        result = self.rhythm_engine.process_input(current_time)
                        if result:
                            self.last_judgment_result = result
                            self.ui_renderer.add_judgment_feedback(result)
                    else:
                        # Toggle audio playback
                        if self.audio_manager.current_music:
                            if self.audio_manager.is_playing():
                                self.audio_manager.pause_music()
                                self.paused = True
                                if Config.is_debug():
                                    print("Audio paused")
                            else:
                                if self.audio_manager.is_paused:
                                    self.audio_manager.resume_music()
                                    self.paused = False
                                    if Config.is_debug():
                                        print("Audio resumed")
                                else:
                                    self.audio_manager.play_music()
                                    self.paused = False
                                    if Config.is_debug():
                                        print("Audio started")
                elif event.key == pygame.K_ESCAPE:
                    if self.in_rhythm_mode:
                        # Exit rhythm mode
                        self.end_rhythm_game()
                    else:
                        self.running = False

        return space_pressed

    def update(self) -> None:
        """Update game state"""
        if self.in_rhythm_mode:
            # Update rhythm game
            current_time = self.audio_manager.get_current_time()
            self.rhythm_engine.update(current_time)
            
            # Update UI renderer
            dt = self.clock.get_time()  # デルタタイム（ミリ秒）
            self.ui_renderer.update(dt)

    def render(self) -> None:
        """Render the current frame"""
        if self.in_rhythm_mode:
            # Render rhythm game
            self.render_rhythm_game()
        else:
            # Render menu/debug mode
            self.render_menu_mode()
            # Update display (only in menu mode, rhythm mode handles its own display update)
            pygame.display.flip()

    def render_rhythm_game(self) -> None:
        """Render rhythm game mode"""
        # Get current game state
        current_time = self.audio_manager.get_current_time()
        active_notes = self.rhythm_engine.get_active_notes(current_time)
        
        # Calculate music progress
        audio_info = self.audio_manager.get_audio_info()
        duration = audio_info.get('duration_ms', 1)
        progress = current_time / duration if duration > 0 else 0.0
        
        # Create UI state dictionary
        ui_state = {
            'notes': active_notes,
            'current_time': current_time,
            'score': self.rhythm_engine.get_score(),
            'combo': self.rhythm_engine.get_combo(),
            'multiplier': self.rhythm_engine._get_combo_multiplier(),
            'last_judgment': self.last_judgment_result,
            'music_name': self.current_music_name,
            'progress': progress,
            'paused': self.paused
        }
        
        # Render complete frame
        self.ui_renderer.render_frame(ui_state)

    def render_menu_mode(self) -> None:
        """Render menu/debug mode"""
        # Clear screen with black background
        self.screen.fill((0, 0, 0))

        # Render audio info if available
        if Config.is_debug():
            self._render_debug_info()

    def _render_debug_info(self) -> None:
        """Render debug information"""
        font = pygame.font.Font(None, 24)
        y_offset = 10

        info_lines = []
        
        # Audio info
        if self.audio_manager.current_music:
            audio_info = self.audio_manager.get_audio_info()
            info_lines.extend([
                f"Audio: {os.path.basename(audio_info.get('file_path', 'None'))}",
                f"Time: {audio_info.get('current_time_ms', 0):.0f}ms / {audio_info.get('duration_ms', 0):.0f}ms",
                f"Playing: {audio_info.get('is_playing', False)}",
                f"Volume: {audio_info.get('volume', 0):.1f}",
            ])
        else:
            info_lines.append("No audio loaded")
        
        # Game mode info
        info_lines.extend([
            "",
            f"Rhythm Mode: {self.in_rhythm_mode}",
            f"Notes: {len(self.rhythm_engine.notes) if hasattr(self.rhythm_engine, 'notes') else 0}",
            "",
            "Controls:",
            "  SPACE: Hit notes (in rhythm mode) / Toggle audio",
            "  ESC: Exit rhythm mode / Quit game"
        ])

        for line in info_lines:
            if line:  # Skip empty lines
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
        success = self.audio_manager.load_music(file_path)
        if success:
            self.current_music_name = os.path.basename(file_path)
        return success

    def play_audio(self) -> None:
        """Start audio playback"""
        self.audio_manager.play_music()

    def stop_audio(self) -> None:
        """Stop audio playback"""
        self.audio_manager.stop_music()

    def set_volume(self, volume: float) -> None:
        """Set audio volume (0.0 - 1.0)"""
        self.audio_manager.set_volume(volume)

    def start_rhythm_game(self, audio_file: str = None) -> bool:
        """Start rhythm game mode"""
        if Config.is_debug():
            print(f"start_rhythm_game called with: {audio_file}")
            print(f"Current audio loaded: {self.audio_manager.current_music is not None}")
        
        if audio_file:
            if not self.load_audio(audio_file):
                if Config.is_debug():
                    print("Failed to load audio in start_rhythm_game")
                return False
        elif not self.audio_manager.current_music:
            if Config.is_debug():
                print("No audio loaded for rhythm game")
            return False

        # Start rhythm game
        current_file = audio_file or self.audio_manager.current_file_path
        if Config.is_debug():
            print(f"Starting rhythm engine with file: {current_file}")
        
        if self.rhythm_engine.start_game(current_file):
            self.in_rhythm_mode = True
            if Config.is_debug():
                print("Rhythm game mode started")
                print(f"Notes generated: {len(self.rhythm_engine.notes)}")
                print(f"in_rhythm_mode set to: {self.in_rhythm_mode}")
            return True
        else:
            if Config.is_debug():
                print("Failed to start rhythm engine")
            return False

    def end_rhythm_game(self) -> dict:
        """End rhythm game mode and return results"""
        if self.in_rhythm_mode:
            results = self.rhythm_engine.end_game()
            self.in_rhythm_mode = False
            if Config.is_debug():
                print("Rhythm game mode ended")
            return results
        return {}
