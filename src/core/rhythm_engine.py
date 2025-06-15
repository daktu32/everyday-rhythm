"""
RhythmEngine - Core rhythm game logic and state management
"""

import os
import sys
from typing import List, Dict, Any, Optional

# Add src to path for imports (must be before local imports)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Local imports after path setup
from utils.config import Config  # noqa: E402
from gameplay.note import Note  # noqa: E402
from audio.audio_manager import AudioManager  # noqa: E402
from audio.audio_analyzer import AudioAnalyzer  # noqa: E402


class JudgmentResult:
    """Represents a judgment result for timing evaluation"""

    def __init__(self, judgment: str, timing_diff: float, score_gained: int, combo_multiplier: float):
        """
        Initialize judgment result

        Args:
            judgment: Judgment type ('perfect', 'good', 'miss')
            timing_diff: Timing difference in milliseconds
            score_gained: Score gained from this judgment
            combo_multiplier: Current combo multiplier
        """
        self.judgment = judgment
        self.timing_diff = timing_diff
        self.score_gained = score_gained
        self.combo_multiplier = combo_multiplier


class RhythmEngine:
    """Main rhythm game engine managing gameplay logic"""

    def __init__(
        self,
        audio_manager: AudioManager = None,
        audio_analyzer: AudioAnalyzer = None,
        timing_window: Dict[str, float] = None,
    ):
        """Initialize the rhythm engine"""
        self.audio_manager = audio_manager
        self.audio_analyzer = audio_analyzer

        # Timing configuration
        self.timing_window = timing_window or {
            "perfect": 25.0,  # ±25ms
            "good": 50.0,  # ±50ms
        }

        # Game state
        self.notes: List[Note] = []
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.is_playing = False
        self.game_start_time = 0.0

        # Statistics
        self.perfect_count = 0
        self.good_count = 0
        self.miss_count = 0

        # Legacy compatibility
        self.perfect_hits = 0
        self.good_hits = 0
        self.misses = 0

        if Config.is_debug():
            print("RhythmEngine initialized")

    def start_game(self, audio_file: str) -> bool:
        """
        Start a new rhythm game with the given audio file

        Args:
            audio_file: Path to audio file

        Returns:
            True if game started successfully
        """
        if Config.is_debug():
            print(f"Starting game with audio: {audio_file}")

        # Load audio
        if not self.audio_manager.load_music(audio_file):
            if Config.is_debug():
                print("Failed to load audio file")
            return False

        # Generate notes from audio analysis
        self._generate_notes(audio_file)

        # Start audio playback
        self.audio_manager.play_music()
        self.is_playing = True
        self.game_start_time = 0.0  # Will be set by first update

        if Config.is_debug():
            print(f"Game started with {len(self.notes)} notes")

        return True

    def _generate_notes(self, audio_file: str) -> None:
        """Generate notes from audio analysis"""
        beats = self.audio_analyzer.get_beats(audio_file)

        # If no beats detected, generate fallback pattern
        if not beats:
            if Config.is_debug():
                print("No beats detected, generating fallback pattern")
            # Generate simple pattern: one note every second for 10 seconds
            beats = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

        self.notes = []
        for beat_time in beats:
            # Convert beat time from seconds to milliseconds
            hit_time = beat_time * 1000.0
            note = Note(hit_time=hit_time, lane=0)
            self.notes.append(note)

        if Config.is_debug():
            print(f"Generated {len(self.notes)} notes from beats")

    def update_legacy(self, current_time: float) -> None:
        """Legacy update method for compatibility"""
        if not self.is_playing:
            return

        # Set game start time on first update
        if self.game_start_time == 0.0:
            self.game_start_time = current_time

        # Calculate game time
        game_time = current_time - self.game_start_time

        # Update all active notes
        active_notes = 0
        for note in self.notes:
            if note.is_active:
                active_notes += 1
                note.update(game_time, note_speed=300.0)

                # Check for missed notes
                if note.is_missed(game_time):
                    note.miss()
                    self.misses += 1
                    self.combo = 0

        # Check if game should end (all notes processed and audio finished)
        if active_notes == 0 and not self.audio_manager.is_playing():
            if Config.is_debug():
                print("All notes processed and audio finished")
            # Don't auto-end, let player exit manually

    def handle_input(self, key_pressed: bool) -> None:
        """Handle player input"""
        if not self.is_playing or not key_pressed:
            return

        current_time = self.audio_manager.get_current_time()

        # Find the closest hittable note
        closest_note = None
        closest_distance = float("inf")

        for note in self.notes:
            if note.is_active and note.is_hittable(current_time):
                distance = abs(current_time - note.hit_time)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_note = note

        if closest_note:
            # Hit the note
            judgment = closest_note.get_timing_judgment(current_time)
            closest_note.hit()

            # Update score and stats
            self._update_score(judgment)

            if Config.is_debug():
                print(f"Hit note: {judgment}, Score: {self.score}")

    def _update_score(self, judgment: str) -> None:
        """Update score based on judgment"""
        score_values = {"PERFECT": 1000, "GOOD": 500, "MISS": 0}

        points = score_values.get(judgment, 0)
        self.score += points

        if judgment == "PERFECT":
            self.perfect_hits += 1
            self.combo += 1
        elif judgment == "GOOD":
            self.good_hits += 1
            self.combo += 1
        else:
            self.combo = 0

    def get_game_state(self) -> Dict[str, Any]:
        """Get current game state"""
        active_notes = [note for note in self.notes if note.is_active]

        return {
            "score": self.score,
            "combo": self.combo,
            "is_playing": self.is_playing,
            "active_notes": len(active_notes),
            "total_notes": len(self.notes),
            "perfect_hits": self.perfect_hits,
            "good_hits": self.good_hits,
            "misses": self.misses,
        }

    def pause_game(self) -> None:
        """Pause the game"""
        if self.is_playing:
            self.audio_manager.pause_music()
            self.is_playing = False

    def resume_game(self) -> None:
        """Resume the game"""
        if not self.is_playing:
            self.audio_manager.resume_music()
            self.is_playing = True

    def end_game(self) -> Dict[str, Any]:
        """End the game and return final results"""
        self.audio_manager.stop_music()
        self.is_playing = False

        total_notes = len(self.notes)
        accuracy = 0.0
        if total_notes > 0:
            accuracy = (self.perfect_hits + self.good_hits) / total_notes * 100

        results = {
            "final_score": self.score,
            "total_notes": total_notes,
            "perfect_hits": self.perfect_hits,
            "good_hits": self.good_hits,
            "misses": self.misses,
            "accuracy": accuracy,
            "max_combo": self.combo,
        }

        if Config.is_debug():
            print(f"Game ended: {results}")

        return results

    def add_note(self, note: Note) -> None:
        """
        Add a note to the rhythm engine

        Args:
            note: Note to add
        """
        self.notes.append(note)
        if Config.is_debug():
            print(f"Added note at time {note.hit_time}ms")

    def process_input(self, input_time: float = None) -> Optional[JudgmentResult]:
        """
        Process player input and evaluate timing

        Args:
            input_time: Time of input (uses audio manager if not provided)

        Returns:
            JudgmentResult if note was hit, None otherwise
        """
        if input_time is None and self.audio_manager:
            input_time = self.audio_manager.get_current_time() * 1000  # Convert to ms

        if input_time is None:
            return None

        # Find the closest hittable note
        closest_note = None
        closest_distance = float("inf")

        for note in self.notes:
            if note.is_active and not note.is_judged:
                # Check if within good timing window
                timing_diff = abs(input_time - note.hit_time)
                if timing_diff <= self.timing_window["good"]:
                    if timing_diff < closest_distance:
                        closest_distance = timing_diff
                        closest_note = note

        if closest_note:
            # Judge the timing
            timing_diff = input_time - closest_note.hit_time
            judgment = self._judge_timing(abs(timing_diff))

            # Mark note as judged
            closest_note.is_judged = True
            closest_note.hit()

            # Update score and stats
            self._update_score_new(judgment)

            # Create judgment result
            score_gained = self._calculate_score_gain(judgment)
            combo_multiplier = self._get_combo_multiplier()
            result = JudgmentResult(judgment, timing_diff, score_gained, combo_multiplier)

            if Config.is_debug():
                print(f"Processed input: {judgment}, timing_diff={timing_diff:.1f}ms")

            return result

        return None

    def update(self, current_time: float) -> List[JudgmentResult]:
        """
        Update engine state and process missed notes

        Args:
            current_time: Current game time in seconds

        Returns:
            List of miss judgment results
        """
        if not self.is_playing:
            return []

        # Convert to milliseconds for consistency
        current_time_ms = current_time * 1000

        miss_results = []

        # Check for missed notes
        for note in self.notes:
            if note.is_active and not note.is_judged:
                # Check if note is missed (past good timing window)
                time_since_note = current_time_ms - note.hit_time
                if time_since_note > self.timing_window["good"]:
                    # Mark as missed
                    note.is_judged = True
                    note.miss()

                    # Update stats
                    self._update_score_new("miss")

                    # Create miss result
                    miss_result = JudgmentResult("miss", time_since_note, 0, 1.0)
                    miss_results.append(miss_result)

                    if Config.is_debug():
                        print(f"Note missed: time_diff={time_since_note:.1f}ms")

        return miss_results

    def get_score(self) -> int:
        """Get current score"""
        return self.score

    def get_combo(self) -> int:
        """Get current combo count"""
        return self.combo

    def clear(self) -> None:
        """Clear all engine state"""
        self.notes.clear()
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.perfect_count = 0
        self.good_count = 0
        self.miss_count = 0

        # Legacy compatibility
        self.perfect_hits = 0
        self.good_hits = 0
        self.misses = 0

        if Config.is_debug():
            print("RhythmEngine state cleared")

    def _judge_timing(self, timing_diff: float) -> str:
        """
        Judge timing based on timing difference

        Args:
            timing_diff: Absolute timing difference in milliseconds

        Returns:
            Judgment string: 'perfect', 'good', or 'miss'
        """
        if timing_diff <= self.timing_window["perfect"]:
            return "perfect"
        elif timing_diff <= self.timing_window["good"]:
            return "good"
        else:
            return "miss"

    def _update_score_new(self, judgment: str) -> None:
        """
        Update score and statistics for new API

        Args:
            judgment: Judgment result ('perfect', 'good', 'miss')
        """
        score_values = {"perfect": 1000, "good": 500, "miss": 0}

        # Calculate combo multiplier
        combo_multiplier = self._get_combo_multiplier()

        # Calculate points
        base_points = score_values.get(judgment, 0)
        points = int(base_points * combo_multiplier)
        self.score += points

        # Update combo and stats
        if judgment == "perfect":
            self.perfect_count += 1
            self.perfect_hits += 1  # Legacy compatibility
            self.combo += 1
        elif judgment == "good":
            self.good_count += 1
            self.good_hits += 1  # Legacy compatibility
            self.combo += 1
        elif judgment == "miss":
            self.miss_count += 1
            self.misses += 1  # Legacy compatibility
            self.combo = 0

        # Update max combo
        self.max_combo = max(self.max_combo, self.combo)

    def _get_combo_multiplier(self) -> float:
        """Get combo multiplier based on current combo"""
        if self.combo < 10:
            return 1.0
        elif self.combo < 20:
            return 1.1
        else:
            return 1.2

    def get_active_notes(self, current_time: float) -> List[Note]:
        """
        Get notes that should be visible on screen
        
        Args:
            current_time: Current time in milliseconds
            
        Returns:
            List of active notes to display
        """
        # Show notes within the UI visibility window (2 seconds ahead)
        visibility_window = 2000.0  # ms
        
        visible_notes = []
        for note in self.notes:
            if not note.is_judged:
                # Show notes that will hit within the next 2 seconds
                time_to_hit = note.hit_time - current_time
                if -100 <= time_to_hit <= visibility_window:  # Allow small buffer for past notes
                    visible_notes.append(note)
        
        return visible_notes

    def _calculate_score_gain(self, judgment: str) -> int:
        """
        Calculate score gained for a judgment
        
        Args:
            judgment: Judgment type
            
        Returns:
            Score points gained
        """
        score_values = {"perfect": 1000, "good": 500, "miss": 0}
        base_points = score_values.get(judgment, 0)
        combo_multiplier = self._get_combo_multiplier()
        return int(base_points * combo_multiplier)
