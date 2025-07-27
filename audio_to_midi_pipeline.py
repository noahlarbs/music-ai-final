# 🎸 Audio-to-MIDI Pipeline for MusicLM Integration

import librosa
import numpy as np
import pretty_midi
from scipy.signal import find_peaks
import soundfile as sf

class AudioToMIDIConverter:
    """
    Converts MusicLM audio output to MIDI for tablature generation
    """
    
    def __init__(self):
        self.sample_rate = 22050
        self.hop_length = 512
        self.frame_length = 2048
        
    def convert_audio_to_midi(self, audio_file_path, output_midi_path):
        """
        Main conversion pipeline: Audio → MIDI
        """
        print(f"🎵 Converting {audio_file_path} to MIDI...")
        
        # Step 1: Load and preprocess audio
        audio, sr = self._load_audio(audio_file_path)
        
        # Step 2: Extract pitch information
        pitches, magnitudes = self._extract_pitches(audio, sr)
        
        # Step 3: Detect note onsets and durations
        notes = self._detect_notes(pitches, magnitudes)
        
        # Step 4: Create MIDI file
        midi_file = self._create_midi_file(notes)
        
        # Step 5: Save MIDI
        midi_file.write(output_midi_path)
        print(f"✅ MIDI saved to {output_midi_path}")
        
        return output_midi_path
    
    def _load_audio(self, audio_file_path):
        """Load and resample audio file"""
        audio, sr = librosa.load(audio_file_path, sr=self.sample_rate)
        return audio, sr
    
    def _extract_pitches(self, audio, sr):
        """Extract pitch information using librosa"""
        # Use piptrack for pitch detection
        pitches, magnitudes = librosa.piptrack(
            y=audio,
            sr=sr,
            hop_length=self.hop_length,
            frame_length=self.frame_length,
            threshold=0.1
        )
        return pitches, magnitudes
    
    def _detect_notes(self, pitches, magnitudes):
        """
        Convert pitch information to discrete notes
        This is the most challenging part!
        """
        notes = []
        threshold = 0.1
        
        # Process each time frame
        for frame_idx in range(pitches.shape[1]):
            frame_pitches = pitches[:, frame_idx]
            frame_magnitudes = magnitudes[:, frame_idx]
            
            # Find peaks in magnitude (strongest frequencies)
            peaks, _ = find_peaks(frame_magnitudes, height=threshold)
            
            for peak_idx in peaks:
                pitch = frame_pitches[peak_idx]
                magnitude = frame_magnitudes[peak_idx]
                
                if pitch > 0 and magnitude > threshold:
                    # Convert frequency to MIDI note number
                    midi_note = int(round(12 * np.log2(pitch / 440) + 69))
                    
                    # Only include notes in guitar range (E2 to E6)
                    if 40 <= midi_note <= 88:
                        notes.append({
                            'note': midi_note,
                            'time': frame_idx * self.hop_length / self.sample_rate,
                            'velocity': int(magnitude * 100)
                        })
        
        return self._merge_adjacent_notes(notes)
    
    def _merge_adjacent_notes(self, notes):
        """Merge consecutive notes of the same pitch"""
        if not notes:
            return []
        
        merged = []
        current_note = notes[0].copy()
        
        for note in notes[1:]:
            # If same note and within 0.1 seconds, extend duration
            if (note['note'] == current_note['note'] and 
                note['time'] - current_note['time'] < 0.1):
                current_note['duration'] = note['time'] - current_note['time']
            else:
                # End current note and start new one
                if 'duration' not in current_note:
                    current_note['duration'] = 0.1  # Default duration
                merged.append(current_note)
                current_note = note.copy()
        
        # Add final note
        if 'duration' not in current_note:
            current_note['duration'] = 0.1
        merged.append(current_note)
        
        return merged
    
    def _create_midi_file(self, notes):
        """Create MIDI file from detected notes"""
        midi = pretty_midi.PrettyMIDI()
        guitar_program = pretty_midi.Instrument(program=25)  # Acoustic Guitar
        
        for note_data in notes:
            # Convert time to MIDI ticks
            start_time = note_data['time']
            end_time = start_time + note_data['duration']
            
            # Create MIDI note
            note = pretty_midi.Note(
                velocity=note_data['velocity'],
                pitch=note_data['note'],
                start=start_time,
                end=end_time
            )
            guitar_program.notes.append(note)
        
        midi.instruments.append(guitar_program)
        return midi

# Example usage with MusicLM integration
class MusicLMToTablature:
    """
    Complete pipeline: MusicLM → Audio → MIDI → Tablature
    """
    
    def __init__(self, musiclm_api_key):
        self.musiclm_api_key = musiclm_api_key
        self.converter = AudioToMIDIConverter()
    
    async def generate_solo_with_musiclm(self, style, key, length, techniques):
        """
        Complete generation pipeline
        """
        # Step 1: Create structured prompt for MusicLM
        prompt = self._create_musiclm_prompt(style, key, length, techniques)
        
        # Step 2: Call MusicLM API
        audio_file = await self._call_musiclm_api(prompt)
        
        # Step 3: Convert audio to MIDI
        midi_file = self.converter.convert_audio_to_midi(
            audio_file, 
            "temp_solo.mid"
        )
        
        # Step 4: Generate tablature from MIDI
        tablature = self._generate_tablature_from_midi(midi_file)
        
        return {
            'audio_file': audio_file,
            'midi_file': midi_file,
            'tablature': tablature
        }
    
    def _create_musiclm_prompt(self, style, key, length, techniques):
        """
        Create structured prompts for MusicLM
        """
        prompts = {
            "blues": f"blues guitar solo in {key} major, soulful and expressive, {length} bars, with bends and slides",
            "rock": f"rock guitar solo in {key} major, energetic and melodic, {length} bars, with power chords and fast runs",
            "jazz": f"jazz guitar solo in {key} major, sophisticated harmonies, {length} bars, with complex chord progressions",
            "metal": f"metal guitar solo in {key} major, fast and technical, {length} bars, with shredding and tapping"
        }
        
        # Add technique-specific instructions
        technique_prompts = {
            "bends": "with expressive pitch bends",
            "slides": "with smooth slides between notes",
            "hammer-ons": "with hammer-ons and pull-offs",
            "tapping": "with two-handed tapping techniques"
        }
        
        base_prompt = prompts.get(style, prompts["blues"])
        
        # Add selected techniques
        for technique in techniques:
            if technique in technique_prompts:
                base_prompt += f", {technique_prompts[technique]}"
        
        return base_prompt
    
    async def _call_musiclm_api(self, prompt):
        """
        Call MusicLM API (mock implementation)
        """
        # This would be the actual API call
        # For now, we'll simulate it
        print(f"🎵 Calling MusicLM with prompt: {prompt}")
        
        # Simulate API call
        import time
        time.sleep(2)  # Simulate processing time
        
        # Return path to generated audio file
        return "generated_solo.wav"
    
    def _generate_tablature_from_midi(self, midi_file):
        """
        Convert MIDI to guitar tablature
        """
        # This would use the existing tablature generation logic
        # from guitar_solo_generator.html
        pass

# Example usage
if __name__ == "__main__":
    # Test the conversion pipeline
    converter = AudioToMIDIConverter()
    
    # This would be called after MusicLM generates audio
    # converter.convert_audio_to_midi("musiclm_output.wav", "solo.mid")
    
    print("🎸 Audio-to-MIDI conversion pipeline ready!")
    print("📝 Next: Integrate with MusicLM API") 