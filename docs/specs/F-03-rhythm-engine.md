# F-03: Rhythm Engine

**Date**: 2025-06-15  
**Status**: In Progress  
**Priority**: P0 (Must-Have)  
**Dependencies**: F-01 (Basic Game Framework), F-02 (Audio System)

## Summary

Implement the core rhythm game engine that generates notes based on audio analysis, handles player input timing, evaluates performance, and provides visual feedback for an engaging rhythm game experience.

## User Stories

- **As a player**, I want to see notes falling down the screen in sync with the music so that I can anticipate when to press keys
- **As a player**, I want my key presses to be judged accurately so that I feel the game is fair and responsive
- **As a player**, I want to see my score and accuracy so that I can track my performance
- **As a player**, I want visual feedback when I hit or miss notes so that I understand my timing
- **As a developer**, I want the rhythm engine to automatically generate playable content from any audio file

## Technical Requirements

### Core Components
- **RhythmEngine**: Main rhythm game logic and state management
- **NoteGenerator**: Automatic note generation from audio analysis
- **InputJudge**: Timing evaluation and scoring system
- **UIRenderer**: Visual rendering of notes, score, and feedback
- **GameplayState**: Track current game state and progress

### Gameplay Mechanics
- **Note Types**: Single tap notes (expandable to holds, slides)
- **Timing Windows**: Perfect (±50ms), Good (±100ms), Miss (>100ms)
- **Scoring System**: 1000 points per Perfect, 500 per Good, 0 per Miss
- **Accuracy Tracking**: Percentage of Perfect/Good hits
- **Combo System**: Consecutive hits multiplier

### Visual Design
- **Note Lane**: Single vertical lane for simplicity
- **Note Speed**: Configurable fall speed based on BPM
- **Hit Zone**: Visual indicator at bottom of screen
- **Feedback**: Color-coded judgment text and effects
- **UI Elements**: Score, accuracy, combo counter

## Acceptance Criteria

### Functional Requirements
- [ ] Generate notes automatically from audio beat detection
- [ ] Display notes falling down the screen in sync with music
- [ ] Detect space key presses with accurate timing
- [ ] Judge timing accuracy within defined windows
- [ ] Display real-time score and accuracy
- [ ] Show visual feedback for hits and misses
- [ ] Handle game start, pause, and end states

### Performance Requirements
- [ ] Input latency < 20ms for responsive gameplay
- [ ] Stable 60 FPS during gameplay
- [ ] Smooth note animation without stuttering
- [ ] Accurate timing synchronization with audio

### Quality Requirements
- [ ] Consistent difficulty scaling based on audio complexity
- [ ] Clear visual distinction between different judgment types
- [ ] Intuitive UI layout and information display
- [ ] Graceful handling of edge cases (no beats detected, etc.)

## Implementation Plan

### Phase 1: Core Rhythm Engine
1. Create RhythmEngine class with game state management
2. Implement basic note data structure
3. Add timing calculation and synchronization
4. Create input handling and judgment system

### Phase 2: Note Generation
1. Integrate with AudioAnalyzer for beat detection
2. Implement NoteGenerator with configurable difficulty
3. Add note timing and positioning logic
4. Create note lifecycle management

### Phase 3: Visual Rendering
1. Implement UIRenderer for game elements
2. Add note rendering and animation
3. Create judgment feedback system
4. Implement score and UI display

### Phase 4: Gameplay Integration
1. Connect all components in GameManager
2. Add game state transitions
3. Implement pause/resume functionality
4. Add end-game results screen

## Files to Create/Modify

```
src/core/rhythm_engine.py        # Main rhythm game engine
src/gameplay/note_generator.py   # Automatic note generation
src/gameplay/input_judge.py      # Timing evaluation system
src/ui/ui_renderer.py           # Visual rendering system
src/gameplay/note.py            # Note data structure
tests/unit/test_rhythm_engine.py # Unit tests
tests/integration/test_gameplay.py # Integration tests
```

## API Design

### RhythmEngine Class
```python
class RhythmEngine:
    def __init__(self, audio_manager: AudioManager, audio_analyzer: AudioAnalyzer)
    def start_game(self, audio_file: str) -> bool
    def update(self, current_time: float) -> None
    def handle_input(self, key_pressed: bool) -> None
    def get_game_state(self) -> Dict[str, Any]
    def pause_game(self) -> None
    def resume_game(self) -> None
    def end_game(self) -> Dict[str, Any]
```

### Note Class
```python
class Note:
    def __init__(self, hit_time: float, lane: int = 0)
    def update(self, current_time: float, note_speed: float) -> None
    def get_position(self) -> Tuple[int, int]
    def is_hittable(self, current_time: float) -> bool
    def is_missed(self, current_time: float) -> bool
```

### InputJudge Class
```python
class InputJudge:
    def judge_timing(self, note_time: float, input_time: float) -> str
    def calculate_score(self, judgment: str) -> int
    def update_accuracy(self, judgment: str) -> None
    def get_stats(self) -> Dict[str, Any]
```

## Game Configuration

### Timing Windows (milliseconds)
```python
TIMING_WINDOWS = {
    'perfect': 25.0,   # ±25ms for perfect timing
    'good': 50.0,      # ±50ms for good timing
    'miss_threshold': 100.0  # >50ms is considered miss
}
```

### Scoring System
```python
SCORE_VALUES = {
    'perfect': 1000,
    'good': 500,
    'miss': 0
}

COMBO_MULTIPLIERS = {
    (0, 9): 1.0,      # 0-9 combo: no bonus
    (10, 19): 1.1,    # 10-19 combo: 1.1x multiplier
    (20, float('inf')): 1.2  # 20+ combo: 1.2x multiplier
}
```

### Visual Constants
```python
GAME_AREA = {
    'NOTE_LANE_X': 400,      # Center of screen
    'NOTE_LANE_WIDTH': 100,
    'HIT_ZONE_Y': 500,       # Near bottom
    'NOTE_SPAWN_Y': -50,     # Above screen
    'NOTE_SPEED': 300        # pixels per second
}
```

## Testing Strategy

### Unit Tests
```python
def test_rhythm_engine_initialization():
    """Test RhythmEngine initializes correctly"""
    
def test_note_generation_from_beats():
    """Test automatic note generation from audio beats"""
    
def test_timing_judgment_accuracy():
    """Test input timing evaluation within windows"""
    
def test_score_calculation():
    """Test scoring system with different judgments"""
    
def test_note_positioning_and_movement():
    """Test note visual positioning and animation"""
```

### Integration Tests
- Full gameplay loop with audio playback
- Note generation from real audio files
- Input timing accuracy verification
- Performance testing during gameplay

## Success Metrics

### Gameplay Success
- [ ] Notes appear in sync with music beats
- [ ] Input timing feels responsive and accurate
- [ ] Scoring system provides meaningful feedback
- [ ] Visual feedback is clear and immediate
- [ ] Game maintains stable performance

### Technical Success
- [ ] Input latency consistently < 20ms
- [ ] 60 FPS maintained during gameplay
- [ ] Memory usage remains stable
- [ ] Audio-visual synchronization accurate

## Risk Assessment

### Technical Risks
- **Audio-visual sync**: Mitigate with precise timing calculations
- **Input latency**: Optimize input handling pipeline
- **Performance**: Profile and optimize rendering code
- **Beat detection accuracy**: Implement fallback note patterns

### Mitigation Strategies
- Comprehensive timing accuracy testing
- Performance profiling during development
- Fallback mechanisms for poor beat detection
- User-configurable timing offset for calibration

---

**Next Steps**: Begin implementation with RhythmEngine class and basic note system  
**Estimated Effort**: 2-3 days  
**Dependencies**: F-01, F-02 (Complete)
