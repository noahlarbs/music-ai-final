#!/usr/bin/env python3
"""
Test script for key-aware guitar solo generation
"""

import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional

class GuitarStyle(Enum):
    BLUES = "blues"
    ROCK = "rock"
    METAL = "metal"
    JAZZ = "jazz"
    COUNTRY = "country"
    CLASSICAL = "classical"
    FUNK = "funk"
    CUSTOM = "custom"

@dataclass
class SoloParameters:
    style: GuitarStyle
    length_bars: int
    tempo: int
    complexity: str
    key: str = "C"

def generate_key_aware_solo(params: SoloParameters) -> Dict:
    """Generate mock solo data with key awareness"""
    
    # Key information database
    key_info = {
        'C': {'notes': ['C', 'D', 'E', 'F', 'G', 'A', 'B'], 'type': 'major'},
        'G': {'notes': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'], 'type': 'major'},
        'D': {'notes': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'], 'type': 'major'},
        'A': {'notes': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'], 'type': 'major'},
        'E': {'notes': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'], 'type': 'major'},
        'Am': {'notes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'], 'type': 'minor'},
        'Em': {'notes': ['E', 'F#', 'G', 'A', 'B', 'C', 'D'], 'type': 'minor'},
        'Dm': {'notes': ['D', 'E', 'F', 'G', 'A', 'Bb', 'C'], 'type': 'minor'},
    }
    
    # Get key information
    key_data = key_info.get(params.key, key_info['C'])
    key_notes = key_data['notes']
    key_type = key_data['type']
    
    # Convert note names to MIDI numbers
    note_to_midi = {
        'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65, 'F#': 66,
        'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71, 'Bb': 70
    }
    
    # Get available notes in the key
    available_notes = []
    for note in key_notes:
        midi_note = note_to_midi.get(note, 60)
        available_notes.append(midi_note)
    
    print(f"Key: {params.key} ({key_type})")
    print(f"Available notes: {key_notes}")
    print(f"MIDI notes: {available_notes}")
    
    # Generate notes based on key and style
    notes = []
    beats_per_bar = 4
    total_beats = params.length_bars * beats_per_bar
    beat_duration = 60.0 / params.tempo  # seconds per beat
    
    for beat in range(total_beats):
        # Add some randomness to note selection
        if np.random.random() < 0.8:  # 80% chance of playing a note
            # Choose from available notes in the key
            note_pitch = np.random.choice(available_notes)
            
            # Add octave variation
            octave_shift = np.random.choice([-12, 0, 12])
            note_pitch += octave_shift
            
            # Ensure note is in guitar range (E2 to E6)
            note_pitch = max(40, min(88, note_pitch))
            
            start_time = beat * beat_duration
            end_time = start_time + beat_duration * 0.8  # Note duration
            
            notes.append({
                "pitch": int(note_pitch),
                "startTime": start_time,
                "endTime": end_time,
                "velocity": np.random.randint(60, 100)
            })
    
    return {
        "notes": notes,
        "totalTime": total_beats * beat_duration,
        "tempo": params.tempo,
        "style": params.style.value,
        "key": params.key,
        "length_bars": params.length_bars,
        "complexity": params.complexity
    }

def main():
    """Test key-aware generation with different keys"""
    
    test_cases = [
        ("blues", "A", "Blues in A"),
        ("rock", "E", "Rock in E"),
        ("jazz", "Dm", "Jazz in D minor"),
        ("metal", "B", "Metal in B")
    ]
    
    for style, key, description in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {description}")
        print(f"{'='*50}")
        
        params = SoloParameters(
            style=GuitarStyle(style),
            length_bars=4,
            tempo=120,
            complexity="medium",
            key=key
        )
        
        result = generate_key_aware_solo(params)
        
        print(f"Generated {len(result['notes'])} notes")
        print(f"Duration: {result['totalTime']:.2f} seconds")
        print(f"Key: {result['key']}")
        print(f"Style: {result['style']}")
        
        # Show first few notes
        print("First 5 notes:")
        for i, note in enumerate(result['notes'][:5]):
            note_name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][note['pitch'] % 12]
            octave = (note['pitch'] // 12) - 1
            print(f"  {i+1}. {note_name}{octave} (MIDI: {note['pitch']})")

if __name__ == "__main__":
    main() 