"""
Unit tests for Note class
"""
import pytest
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from gameplay.note import Note


class TestNote:
    """Test cases for Note class"""
    
    def test_note_initialization(self):
        """Test Note initializes correctly"""
        # Act
        note = Note(hit_time=1000.0, lane=0)
        
        # Assert
        assert note.hit_time == 1000.0
        assert note.lane == 0
        assert note.y_position == -50  # Default spawn position
        assert note.is_active == True
        assert note.is_hit == False
    
    def test_note_initialization_with_custom_lane(self):
        """Test Note with custom lane"""
        # Act
        note = Note(hit_time=2000.0, lane=1)
        
        # Assert
        assert note.hit_time == 2000.0
        assert note.lane == 1
    
    def test_note_position_calculation(self):
        """Test note position calculation"""
        # Arrange
        note = Note(hit_time=1000.0)
        note_speed = 300.0  # pixels per second
        
        # Act - Note should be at spawn when current_time is much less than hit_time
        note.update(current_time=0.0, note_speed=note_speed)
        spawn_pos = note.get_position()
        
        # Act - Note should move down as time progresses
        note.update(current_time=500.0, note_speed=note_speed)
        mid_pos = note.get_position()
        
        # Act - Note should be at hit zone at hit_time
        note.update(current_time=1000.0, note_speed=note_speed)
        hit_pos = note.get_position()
        
        # Assert
        assert spawn_pos[1] < mid_pos[1] < hit_pos[1]  # Y position increases (moves down)
        assert hit_pos[1] == 500  # Should be at hit zone Y position
    
    def test_note_x_position_based_on_lane(self):
        """Test note X position based on lane"""
        # Arrange
        note_lane_0 = Note(hit_time=1000.0, lane=0)
        note_lane_1 = Note(hit_time=1000.0, lane=1)
        
        # Act
        pos_0 = note_lane_0.get_position()
        pos_1 = note_lane_1.get_position()
        
        # Assert
        assert pos_0[0] == 400  # Lane 0 at center
        assert pos_1[0] == 500  # Lane 1 offset (if implemented)
    
    def test_note_is_hittable(self):
        """Test note hittable timing window"""
        # Arrange
        note = Note(hit_time=1000.0)
        
        # Act & Assert - Too early
        assert note.is_hittable(current_time=800.0) == False
        
        # Act & Assert - Within window
        assert note.is_hittable(current_time=950.0) == True
        assert note.is_hittable(current_time=1000.0) == True
        assert note.is_hittable(current_time=1050.0) == True
        
        # Act & Assert - Too late
        assert note.is_hittable(current_time=1200.0) == False
    
    def test_note_is_missed(self):
        """Test note miss detection"""
        # Arrange
        note = Note(hit_time=1000.0)
        
        # Act & Assert - Not missed yet
        assert note.is_missed(current_time=1000.0) == False
        assert note.is_missed(current_time=1100.0) == False
        
        # Act & Assert - Missed
        assert note.is_missed(current_time=1250.0) == True
    
    def test_note_hit_state(self):
        """Test note hit state management"""
        # Arrange
        note = Note(hit_time=1000.0)
        
        # Act
        note.hit()
        
        # Assert
        assert note.is_hit == True
        assert note.is_active == False
    
    def test_note_miss_state(self):
        """Test note miss state management"""
        # Arrange
        note = Note(hit_time=1000.0)
        
        # Act
        note.miss()
        
        # Assert
        assert note.is_hit == False
        assert note.is_active == False
    
    def test_note_update_with_different_speeds(self):
        """Test note movement with different speeds"""
        # Arrange
        note = Note(hit_time=2000.0)
        
        # Act - Slow speed
        note.update(current_time=1000.0, note_speed=200.0)
        slow_pos = note.get_position()
        
        # Reset note
        note = Note(hit_time=2000.0)
        
        # Act - Fast speed
        note.update(current_time=1000.0, note_speed=400.0)
        fast_pos = note.get_position()
        
        # Assert - Faster speed should result in higher Y position (further up, not yet at hit zone)
        # At current_time=1000, hit_time=2000, so 1 second remaining
        # Slow: 500 - (1.0 * 200) = 300
        # Fast: 500 - (1.0 * 400) = 100
        assert fast_pos[1] < slow_pos[1]  # Fast speed note is higher up (smaller Y)
    
    def test_note_timing_windows(self):
        """Test timing window constants"""
        # Arrange
        note = Note(hit_time=1000.0)
        
        # Act & Assert - Test timing window boundaries (updated for F-03 spec)
        # Good window: ±50ms (hittable window)
        assert note.is_hittable(current_time=950.0) == True   # -50ms
        assert note.is_hittable(current_time=1050.0) == True  # +50ms
        
        # Outside hittable window
        assert note.is_hittable(current_time=949.0) == False  # -51ms
        assert note.is_hittable(current_time=1051.0) == False # +51ms
    
    def test_note_judgment_timing(self):
        """Test timing judgment calculation"""
        # Arrange
        note = Note(hit_time=1000.0)
        
        # Act & Assert - Perfect timing (±25ms)
        judgment = note.get_timing_judgment(input_time=1000.0)
        assert judgment == 'PERFECT'
        
        judgment = note.get_timing_judgment(input_time=1025.0)
        assert judgment == 'PERFECT'
        
        # Act & Assert - Good timing (±50ms)
        judgment = note.get_timing_judgment(input_time=1040.0)
        assert judgment == 'GOOD'
        
        judgment = note.get_timing_judgment(input_time=960.0)
        assert judgment == 'GOOD'
        
        # Act & Assert - Miss (>50ms)
        judgment = note.get_timing_judgment(input_time=1060.0)
        assert judgment == 'MISS'
        
        judgment = note.get_timing_judgment(input_time=940.0)
        assert judgment == 'MISS'
    
    def test_note_timing_difference_calculation(self):
        """Test timing difference calculation for scoring"""
        # Arrange
        note = Note(hit_time=1000.0)
        
        # Act & Assert - Early timing
        timing_diff = note.get_timing_diff(input_time=980.0)
        assert timing_diff == -20.0  # 20ms early
        
        # Act & Assert - Late timing
        timing_diff = note.get_timing_diff(input_time=1030.0)
        assert timing_diff == 30.0  # 30ms late
        
        # Act & Assert - Perfect timing
        timing_diff = note.get_timing_diff(input_time=1000.0)
        assert timing_diff == 0.0  # Exact timing
    
    def test_note_within_window_check(self):
        """Test timing window checking for different judgment types"""
        # Arrange
        note = Note(hit_time=1000.0)
        
        # Act & Assert - Perfect window (±25ms)
        assert note.is_within_window(input_time=1020.0, window=25.0) == True
        assert note.is_within_window(input_time=980.0, window=25.0) == True
        assert note.is_within_window(input_time=1030.0, window=25.0) == False
        
        # Act & Assert - Good window (±50ms)
        assert note.is_within_window(input_time=1045.0, window=50.0) == True
        assert note.is_within_window(input_time=955.0, window=50.0) == True
        assert note.is_within_window(input_time=1060.0, window=50.0) == False
    
    def test_note_multiple_types(self):
        """Test different note types (future expansion)"""
        # Arrange - Regular tap note
        tap_note = Note(hit_time=1000.0, note_type='tap')
        
        # Assert
        assert tap_note.note_type == 'tap'
        assert tap_note.hit_time == 1000.0
        
        # Future implementation for hold notes, slide notes, etc.
        # hold_note = Note(hit_time=1000.0, note_type='hold', duration=500.0)
        # assert hold_note.note_type == 'hold'
        # assert hold_note.duration == 500.0
    
    def test_note_judgment_boundary_cases(self):
        """Test edge cases for timing judgment"""
        # Arrange
        note = Note(hit_time=1000.0)
        
        # Act & Assert - Exact boundary cases
        # Perfect/Good boundary at ±25ms
        assert note.get_timing_judgment(input_time=1025.0) == 'PERFECT'
        assert note.get_timing_judgment(input_time=1026.0) == 'GOOD'
        assert note.get_timing_judgment(input_time=975.0) == 'PERFECT'
        assert note.get_timing_judgment(input_time=974.0) == 'GOOD'
        
        # Good/Miss boundary at ±50ms  
        assert note.get_timing_judgment(input_time=1050.0) == 'GOOD'
        assert note.get_timing_judgment(input_time=1051.0) == 'MISS'
        assert note.get_timing_judgment(input_time=950.0) == 'GOOD'
        assert note.get_timing_judgment(input_time=949.0) == 'MISS'
