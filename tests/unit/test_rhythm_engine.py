"""
Unit tests for RhythmEngine class
"""
import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.rhythm_engine import RhythmEngine
from audio.audio_manager import AudioManager
from audio.audio_analyzer import AudioAnalyzer


class TestRhythmEngine:
    """Test cases for RhythmEngine class"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        self.mock_audio_manager = Mock(spec=AudioManager)
        self.mock_audio_analyzer = Mock(spec=AudioAnalyzer)
    
    def test_rhythm_engine_initialization(self):
        """Test RhythmEngine initializes correctly"""
        # Act
        engine = RhythmEngine(self.mock_audio_manager, self.mock_audio_analyzer)
        
        # Assert
        assert engine.audio_manager == self.mock_audio_manager
        assert engine.audio_analyzer == self.mock_audio_analyzer
        assert engine.notes == []
        assert engine.score == 0
        assert engine.is_playing == False
    
    def test_start_game_success(self):
        """Test successful game start"""
        # Arrange
        engine = RhythmEngine(self.mock_audio_manager, self.mock_audio_analyzer)
        self.mock_audio_manager.load_music.return_value = True
        self.mock_audio_analyzer.get_beats.return_value = [1.0, 2.0, 3.0]
        
        # Act
        result = engine.start_game("test.wav")
        
        # Assert
        assert result == True
        assert engine.is_playing == True
        assert len(engine.notes) == 3
        self.mock_audio_manager.load_music.assert_called_once_with("test.wav")
        self.mock_audio_manager.play_music.assert_called_once()
    
    def test_start_game_audio_load_failure(self):
        """Test game start with audio load failure"""
        # Arrange
        engine = RhythmEngine(self.mock_audio_manager, self.mock_audio_analyzer)
        self.mock_audio_manager.load_music.return_value = False
        
        # Act
        result = engine.start_game("invalid.wav")
        
        # Assert
        assert result == False
        assert engine.is_playing == False
        self.mock_audio_manager.play_music.assert_not_called()
    
    def test_process_input_perfect_timing(self):
        """Test perfect timing input processing"""
        # Arrange
        engine = RhythmEngine(self.mock_audio_manager, self.mock_audio_analyzer)
        self.mock_audio_manager.get_current_time.return_value = 1.02  # 20ms after note
        # 期待される実装: ノート追加とPerfect判定
        
        # Act & Assert - 実装完了により有効化
        from gameplay.note import Note
        note = Note(hit_time=1000.0)  # Use milliseconds
        engine.add_note(note)
        result = engine.process_input(input_time=1020.0)  # 20ms late
        assert result is not None
        assert result.judgment == 'perfect'
        assert abs(result.timing_diff - 20.0) < 5.0
    
    def test_process_input_good_timing(self):
        """Test good timing input processing"""
        # Arrange
        engine = RhythmEngine(self.mock_audio_manager, self.mock_audio_analyzer)
        self.mock_audio_manager.get_current_time.return_value = 1.04  # 40ms after note
        # 期待される実装: ノート追加とGood判定
        
        # Act & Assert - 実装完了により有効化
        from gameplay.note import Note
        note = Note(hit_time=1000.0)  # Use milliseconds
        engine.add_note(note)
        result = engine.process_input(input_time=1040.0)  # 40ms late
        assert result is not None
        assert result.judgment == 'good'
        assert abs(result.timing_diff - 40.0) < 5.0
    
    def test_process_input_miss_timing(self):
        """Test miss timing input processing"""
        # Arrange
        engine = RhythmEngine(self.mock_audio_manager, self.mock_audio_analyzer)
        self.mock_audio_manager.get_current_time.return_value = 1.08  # 80ms after note
        # 期待される実装: Miss判定
        
        # Act & Assert - 実装完了により有効化
        from gameplay.note import Note
        note = Note(hit_time=1000.0)  # Use milliseconds
        engine.add_note(note)
        result = engine.process_input(input_time=1080.0)  # 80ms late (miss)
        assert result is None  # Miss範囲外は None を返す
    
    def test_update_removes_expired_notes(self):
        """Test that update removes expired notes and creates miss judgments"""
        # Arrange
        engine = RhythmEngine(self.mock_audio_manager, self.mock_audio_analyzer)
        current_time = 1.1  # 100ms after note timing
        # 期待される実装: 期限切れノートのMiss処理
        
        # Act & Assert - 実装完了により有効化
        from gameplay.note import Note
        note = Note(hit_time=1000.0)  # Use milliseconds
        engine.add_note(note)
        engine.is_playing = True  # Set playing state
        miss_results = engine.update(current_time=1.1)  # 1.1 seconds = 1100ms
        assert len(miss_results) == 1
        assert miss_results[0].judgment == 'miss'
    
    def test_score_calculation_with_combo(self):
        """Test score calculation with combo multiplier"""
        # Arrange
        engine = RhythmEngine(self.mock_audio_manager, self.mock_audio_analyzer)
        # 期待される実装: コンボによるスコア倍率
        
        # Act & Assert - 実装後に有効化
        # # 10連続Perfect（コンボ倍率1.1倍）
        # for i in range(10):
        #     engine.add_note(Note(timing=i + 1.0))
        #     self.mock_audio_manager.get_current_time.return_value = i + 1.02
        #     result = engine.process_input()
        #     assert result.judgment == 'perfect'
        # 
        # expected_score = 1000 * 9 + int(1000 * 1.1)  # 最後の1つは1.1倍
        # assert engine.get_score() == expected_score
    
    def test_clear_resets_all_state(self):
        """Test that clear resets all engine state"""
        # Arrange
        engine = RhythmEngine(self.mock_audio_manager, self.mock_audio_analyzer)
        # 期待される実装: すべての状態リセット
        
        # Act & Assert - 実装後に有効化
        # # 何らかの状態を設定
        # engine.add_note(Note(timing=1.0))
        # self.mock_audio_manager.get_current_time.return_value = 1.02
        # engine.process_input()  # スコア・コンボを設定
        # 
        # # クリア前の確認
        # assert engine.get_score() > 0
        # assert engine.get_combo() > 0
        # assert len(engine.notes) > 0
        # 
        # # クリア実行
        # engine.clear()
        # 
        # # クリア後の確認
        # assert engine.get_score() == 0
        # assert engine.get_combo() == 0
        # assert len(engine.notes) == 0
