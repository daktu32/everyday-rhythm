"""
Note - Individual rhythm game note representation
"""

import os
import sys
from typing import Tuple

# Add src to path for imports (must be before local imports)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Local imports after path setup
from utils.config import Config  # noqa: E402

# Game constants
GAME_AREA = {
    "NOTE_LANE_X": 400,  # Center of screen
    "NOTE_LANE_WIDTH": 100,
    "HIT_ZONE_Y": 500,  # Near bottom
    "NOTE_SPAWN_Y": -50,  # Above screen
    "NOTE_SPEED": 300,  # pixels per second (default)
}

TIMING_WINDOWS = {
    "PERFECT": 25,  # ±25ms (updated for F-03 spec)
    "GOOD": 50,  # ±50ms (updated for F-03 spec)
    "MISS": 100,  # >50ms (updated for F-03 spec)
}


class Note:
    """Represents a single rhythm game note"""

    def __init__(self, hit_time: float, lane: int = 0, note_type: str = "tap"):
        """
        Initialize a note

        Args:
            hit_time: Time in milliseconds when note should be hit
            lane: Lane number (0 = center, expandable for multi-lane)
            note_type: Note type ('tap', 'hold', etc.)
        """
        self.hit_time = hit_time
        self.lane = lane
        self.note_type = note_type
        self.y_position = GAME_AREA["NOTE_SPAWN_Y"]
        self.is_active = True
        self.is_hit = False
        self.is_judged = False

        if Config.is_debug():
            print(f"Note created: hit_time={hit_time}ms, lane={lane}")

    def update(self, current_time: float, note_speed: float) -> None:
        """
        Update note position based on current time

        Args:
            current_time: Current game time in milliseconds
            note_speed: Speed of note movement in pixels per second
        """
        if not self.is_active:
            return

        # Calculate how far the note should have traveled
        # Time until hit (negative means past hit time)
        time_to_hit = self.hit_time - current_time

        # Distance from hit zone (negative means below hit zone)
        distance_from_hit_zone = (time_to_hit / 1000.0) * note_speed

        # Calculate Y position (hit zone + distance)
        self.y_position = GAME_AREA["HIT_ZONE_Y"] - distance_from_hit_zone

    def get_position(self) -> Tuple[int, int]:
        """
        Get current screen position of the note

        Returns:
            Tuple of (x, y) screen coordinates
        """
        x = GAME_AREA["NOTE_LANE_X"] + (self.lane * 100)  # Offset for different lanes
        y = int(self.y_position)
        return (x, y)

    def is_hittable(self, current_time: float) -> bool:
        """
        Check if note is within hittable timing window

        Args:
            current_time: Current game time in milliseconds

        Returns:
            True if note can be hit at current time
        """
        time_diff = abs(current_time - self.hit_time)
        return time_diff <= TIMING_WINDOWS["GOOD"]

    def is_missed(self, current_time: float) -> bool:
        """
        Check if note has been missed (past timing window)

        Args:
            current_time: Current game time in milliseconds

        Returns:
            True if note is past the miss window
        """
        time_diff = current_time - self.hit_time
        return time_diff > TIMING_WINDOWS["MISS"]

    def get_timing_judgment(self, input_time: float) -> str:
        """
        Get timing judgment for input

        Args:
            input_time: Time when input was received in milliseconds

        Returns:
            Judgment string: 'PERFECT', 'GOOD', or 'MISS'
        """
        time_diff = abs(input_time - self.hit_time)

        if time_diff <= TIMING_WINDOWS["PERFECT"]:
            return "PERFECT"
        elif time_diff <= TIMING_WINDOWS["GOOD"]:
            return "GOOD"
        else:
            return "MISS"

    def hit(self) -> None:
        """Mark note as hit"""
        self.is_hit = True
        self.is_active = False

        if Config.is_debug():
            print(f"Note hit at time {self.hit_time}ms")

    def miss(self) -> None:
        """Mark note as missed"""
        self.is_hit = False
        self.is_active = False

        if Config.is_debug():
            print(f"Note missed at time {self.hit_time}ms")

    def get_info(self) -> dict:
        """Get note information for debugging"""
        return {
            "hit_time": self.hit_time,
            "lane": self.lane,
            "note_type": self.note_type,
            "y_position": self.y_position,
            "is_active": self.is_active,
            "is_hit": self.is_hit,
            "is_judged": self.is_judged,
            "screen_position": self.get_position(),
        }

    def get_timing_diff(self, input_time: float) -> float:
        """
        Calculate timing difference between input and note timing

        Args:
            input_time: Time when input was received

        Returns:
            Timing difference in milliseconds (positive = late, negative = early)
        """
        return input_time - self.hit_time

    def is_within_window(self, input_time: float, window: float) -> bool:
        """
        Check if input time is within specified timing window

        Args:
            input_time: Time when input was received
            window: Timing window in milliseconds (±window)

        Returns:
            True if input is within timing window
        """
        time_diff = abs(input_time - self.hit_time)
        return time_diff <= window
