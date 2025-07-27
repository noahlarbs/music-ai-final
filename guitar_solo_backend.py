#!/usr/bin/env python3
"""
AI Guitar Solo Generator Backend
Integrates with modern AI music generation models
"""

import os
import json
import asyncio
import aiohttp
import numpy as np
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    key: str = "C"  # Musical key (e.g., "C", "Am", "G#")
    custom_description: Optional[str] = None
    chord_progression: Optional[List[str]] = None
    influence_midi: Optional[str] = None

class MusicAIGenerator:
    """Base class for AI music generation models"""
    
    def __init__(self):
        self.models = {}
        self.initialized = False
    
    async def initialize(self):
        """Initialize all models"""
        raise NotImplementedError
    
    async def generate_solo(self, params: SoloParameters) -> Dict:
        """Generate a guitar solo based on parameters"""
        raise NotImplementedError

class MusicLMGenerator(MusicAIGenerator):
    """Google's MusicLM integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.api_key = api_key or os.getenv("MUSICLM_API_KEY")
        self.base_url = "https://api.musiclm.google.com/v1"
    
    async def initialize(self):
        """Initialize MusicLM model"""
        if not self.api_key:
            logger.warning("MusicLM API key not found. Using mock generation.")
            return
        
        try:
            # Initialize MusicLM client
            # This would be the actual MusicLM API initialization
            logger.info("MusicLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MusicLM: {e}")
    
    async def generate_solo(self, params: SoloParameters) -> Dict:
        """Generate solo using MusicLM"""
        
        # Create text prompt based on style
        prompt = self._create_prompt(params)
        
        if not self.api_key:
            # Return mock data for development
            return self._generate_mock_solo(params)
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "prompt": prompt,
                    "duration": params.length_bars * 2,  # Convert bars to seconds
                    "temperature": self._get_temperature(params.complexity)
                }
                
                async with session.post(
                    f"{self.base_url}/generate",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return self._process_musiclm_response(result, params)
                    else:
                        logger.error(f"MusicLM API error: {response.status}")
                        return self._generate_mock_solo(params)
                        
        except Exception as e:
            logger.error(f"Error generating with MusicLM: {e}")
            return self._generate_mock_solo(params)
    
    def _create_prompt(self, params: SoloParameters) -> str:
        """Create a text prompt for MusicLM"""
        
        style_descriptions = {
            GuitarStyle.BLUES: "blues guitar solo with bends, slides, and pentatonic scales",
            GuitarStyle.ROCK: "rock guitar solo with power chords and melodic phrases",
            GuitarStyle.METAL: "metal shredding with fast runs and technical passages",
            GuitarStyle.JAZZ: "jazz guitar solo with complex harmonies and improvisation",
            GuitarStyle.COUNTRY: "country guitar with twang and traditional licks",
            GuitarStyle.CLASSICAL: "classical guitar with arpeggios and fingerpicking",
            GuitarStyle.FUNK: "funk guitar with rhythmic grooves and syncopation"
        }
        
        base_description = style_descriptions.get(params.style, params.custom_description or "guitar solo")
        
        # Add complexity modifiers
        complexity_modifiers = {
            "simple": "simple and melodic",
            "medium": "moderate complexity",
            "complex": "complex and technical",
            "virtuoso": "virtuoso level with advanced techniques"
        }
        
        complexity_desc = complexity_modifiers.get(params.complexity, "")
        
        # Add key information
        key_desc = f"in the key of {params.key}"
        
        # Add tempo information
        tempo_desc = f"at {params.tempo} BPM"
        
        # Add length information
        length_desc = f"{params.length_bars} bar"
        
        prompt = f"{base_description}, {complexity_desc}, {length_desc} solo {key_desc} {tempo_desc}"
        
        if params.chord_progression:
            chords = " ".join(params.chord_progression)
            prompt += f" over chord progression: {chords}"
        
        return prompt
    
    def _get_temperature(self, complexity: str) -> float:
        """Get temperature based on complexity"""
        return {
            "simple": 0.7,
            "medium": 0.8,
            "complex": 0.9,
            "virtuoso": 1.0
        }.get(complexity, 0.8)
    
    def _process_musiclm_response(self, response: Dict, params: SoloParameters) -> Dict:
        """Process MusicLM API response"""
        # This would convert MusicLM's audio output to MIDI
        # For now, return mock data
        return self._generate_mock_solo(params)
    
    def _generate_mock_solo(self, params: SoloParameters) -> Dict:
        """Generate mock solo data for development"""
        
        # Key information database
        key_info = {
            'C': {'notes': ['C', 'D', 'E', 'F', 'G', 'A', 'B'], 'type': 'major'},
            'G': {'notes': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'], 'type': 'major'},
            'D': {'notes': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'], 'type': 'major'},
            'A': {'notes': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'], 'type': 'major'},
            'E': {'notes': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'], 'type': 'major'},
            'B': {'notes': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'], 'type': 'major'},
            'F#': {'notes': ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'], 'type': 'major'},
            'C#': {'notes': ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'], 'type': 'major'},
            'F': {'notes': ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'], 'type': 'major'},
            'Bb': {'notes': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'], 'type': 'major'},
            'Eb': {'notes': ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'], 'type': 'major'},
            'Ab': {'notes': ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'], 'type': 'major'},
            'Db': {'notes': ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'], 'type': 'major'},
            'Gb': {'notes': ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F'], 'type': 'major'},
            'Cb': {'notes': ['Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb'], 'type': 'major'},
            'Am': {'notes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'], 'type': 'minor'},
            'Em': {'notes': ['E', 'F#', 'G', 'A', 'B', 'C', 'D'], 'type': 'minor'},
            'Bm': {'notes': ['B', 'C#', 'D', 'E', 'F#', 'G', 'A'], 'type': 'minor'},
            'F#m': {'notes': ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E'], 'type': 'minor'},
            'C#m': {'notes': ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B'], 'type': 'minor'},
            'G#m': {'notes': ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#'], 'type': 'minor'},
            'D#m': {'notes': ['D#', 'E#', 'F#', 'G#', 'A#', 'B', 'C#'], 'type': 'minor'},
            'A#m': {'notes': ['A#', 'B#', 'C#', 'D#', 'E#', 'F#', 'G#'], 'type': 'minor'},
            'Dm': {'notes': ['D', 'E', 'F', 'G', 'A', 'Bb', 'C'], 'type': 'minor'},
            'Gm': {'notes': ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F'], 'type': 'minor'},
            'Cm': {'notes': ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'], 'type': 'minor'},
            'Fm': {'notes': ['F', 'G', 'Ab', 'Bb', 'C', 'Db', 'Eb'], 'type': 'minor'},
            'Bbm': {'notes': ['Bb', 'C', 'Db', 'Eb', 'F', 'Gb', 'Ab'], 'type': 'minor'},
            'Ebm': {'notes': ['Eb', 'F', 'Gb', 'Ab', 'Bb', 'Cb', 'Db'], 'type': 'minor'},
            'Abm': {'notes': ['Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'Gb'], 'type': 'minor'}
        }
        
        # Get key information
        key_data = key_info.get(params.key, key_info['C'])  # Default to C if key not found
        key_notes = key_data['notes']
        key_type = key_data['type']
        
        # Convert note names to MIDI numbers
        note_to_midi = {
            'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65, 'F#': 66,
            'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71, 'Bb': 70, 'Eb': 63,
            'Ab': 68, 'Db': 61, 'Gb': 66, 'Cb': 59, 'Fb': 64, 'E#': 65, 'B#': 72
        }
        
        # Get available notes in the key
        available_notes = []
        for note in key_notes:
            midi_note = note_to_midi.get(note, 60)
            available_notes.append(midi_note)
        
        # Define scale patterns for different styles (relative to key)
        scale_patterns = {
            GuitarStyle.BLUES: [0, 3, 5, 6, 7, 10],  # Blues scale
            GuitarStyle.ROCK: [0, 2, 4, 5, 7, 9, 11],  # Major scale
            GuitarStyle.METAL: [0, 2, 4, 5, 7, 9, 11],  # Minor scale
            GuitarStyle.JAZZ: [0, 2, 3, 5, 7, 8, 10, 11],  # Jazz scale
            GuitarStyle.COUNTRY: [0, 2, 4, 5, 7, 9, 11],  # Major scale
            GuitarStyle.CLASSICAL: [0, 2, 4, 5, 7, 9, 11],  # Major scale
            GuitarStyle.FUNK: [0, 2, 4, 5, 7, 9, 11]  # Major scale
        }
        
        # Use key-appropriate scale pattern
        if key_type == 'minor' and params.style in [GuitarStyle.ROCK, GuitarStyle.COUNTRY, GuitarStyle.CLASSICAL, GuitarStyle.FUNK]:
            # Use minor scale for minor keys
            pattern = [0, 2, 3, 5, 7, 8, 10]
        else:
            pattern = scale_patterns.get(params.style, [0, 2, 4, 5, 7, 9, 11])
        
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

class AudioCraftGenerator(MusicAIGenerator):
    """Meta's AudioCraft/MusicGen integration"""
    
    def __init__(self):
        super().__init__()
        self.model = None
    
    async def initialize(self):
        """Initialize AudioCraft model"""
        try:
            # This would initialize the AudioCraft model
            # For now, we'll use mock generation
            logger.info("AudioCraft initialized (mock mode)")
        except Exception as e:
            logger.error(f"Failed to initialize AudioCraft: {e}")
    
    async def generate_solo(self, params: SoloParameters) -> Dict:
        """Generate solo using AudioCraft"""
        # AudioCraft implementation would go here
        # For now, return mock data
        generator = MusicLMGenerator()
        return generator._generate_mock_solo(params)

class GuitarSoloAPI:
    """Main API class for guitar solo generation"""
    
    def __init__(self):
        self.generators = {
            "musiclm": MusicLMGenerator(),
            "audiocraft": AudioCraftGenerator()
        }
        self.initialized = False
    
    async def initialize(self):
        """Initialize all generators"""
        if self.initialized:
            return
        
        for name, generator in self.generators.items():
            try:
                await generator.initialize()
                logger.info(f"{name} generator initialized")
            except Exception as e:
                logger.error(f"Failed to initialize {name}: {e}")
        
        self.initialized = True
    
    async def generate_solo(self, 
                          style: str,
                          length_bars: int = 8,
                          tempo: int = 120,
                          complexity: str = "medium",
                          key: str = "C",
                          custom_description: Optional[str] = None,
                          chord_progression: Optional[List[str]] = None,
                          model: str = "musiclm") -> Dict:
        """Generate a guitar solo"""
        
        if not self.initialized:
            await self.initialize()
        
        # Validate parameters
        try:
            guitar_style = GuitarStyle(style)
        except ValueError:
            guitar_style = GuitarStyle.CUSTOM
            custom_description = style
        
        params = SoloParameters(
            style=guitar_style,
            length_bars=length_bars,
            tempo=tempo,
            complexity=complexity,
            key=key,
            custom_description=custom_description,
            chord_progression=chord_progression
        )
        
        # Select generator
        generator = self.generators.get(model, self.generators["musiclm"])
        
        try:
            result = await generator.generate_solo(params)
            logger.info(f"Generated solo: {params.style.value}, {params.length_bars} bars")
            return result
        except Exception as e:
            logger.error(f"Error generating solo: {e}")
            return {"error": str(e)}

# Example usage and testing
async def main():
    """Test the guitar solo generator"""
    api = GuitarSoloAPI()
    await api.initialize()
    
    # Test different styles
    styles = ["blues", "rock", "metal", "jazz"]
    
    for style in styles:
        print(f"\nGenerating {style} solo...")
        result = await api.generate_solo(
            style=style,
            length_bars=4,
            tempo=120,
            complexity="medium"
        )
        
        if "error" not in result:
            print(f"Generated {len(result['notes'])} notes")
            print(f"Duration: {result['totalTime']:.2f} seconds")
        else:
            print(f"Error: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main()) 