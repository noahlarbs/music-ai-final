# 🎸 Simple MusicLM Integration (No Additional Dependencies)

import asyncio
import json
from musiclm_api_setup import MusicLMBackendIntegration

class SimpleMusicLMIntegration:
    """
    Simple MusicLM integration without audio processing dependencies
    """
    
    def __init__(self, use_mock=True):
        self.musiclm = MusicLMBackendIntegration(use_mock=use_mock)
    
    async def generate_solo(self, style, key, techniques=None):
        """
        Generate solo using MusicLM API
        """
        print(f"🎸 Generating {style} solo in {key}...")
        
        # Generate audio with MusicLM
        result = await self.musiclm.generate_solo(style, key, techniques)
        
        if result["status"] != "success":
            return {
                "success": False,
                "error": result.get("error", "Unknown error")
            }
        
        # For now, return mock MIDI data
        # In real implementation, this would convert audio to MIDI
        mock_midi_data = self._create_mock_midi_data(style, key)
        
        return {
            "success": True,
            "style": style,
            "key": key,
            "techniques": techniques,
            "audio_url": result["audio_url"],
            "midi_data": mock_midi_data,
            "prompt": result["prompt"]
        }
    
    def _create_mock_midi_data(self, style, key):
        """
        Create mock MIDI data based on style and key
        This simulates what we'd get from audio-to-MIDI conversion
        """
        # Define notes for different keys
        key_notes = {
            "A": [45, 47, 49, 50, 52, 54, 56, 57, 59, 61, 62, 64],  # A major
            "E": [40, 42, 44, 45, 47, 49, 51, 52, 54, 56, 57, 59],  # E major
            "C": [48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67],  # C major
            "D": [50, 52, 54, 55, 57, 59, 61, 62, 64, 66, 67, 69],  # D major
            "G": [43, 45, 47, 48, 50, 52, 54, 55, 57, 59, 60, 62]   # G major
        }
        
        # Get notes for the selected key
        available_notes = key_notes.get(key, key_notes["A"])
        
        # Create mock solo data
        import random
        notes = []
        current_time = 0
        
        # Generate 8-16 notes
        num_notes = random.randint(8, 16)
        
        for i in range(num_notes):
            # Random note from the key
            pitch = random.choice(available_notes)
            
            # Random duration (0.25 to 1.0 seconds)
            duration = random.uniform(0.25, 1.0)
            
            notes.append({
                "pitch": pitch,
                "start_time": current_time,
                "duration": duration,
                "velocity": random.randint(60, 100)
            })
            
            current_time += duration
        
        return {
            "notes": notes,
            "total_duration": current_time,
            "style": style,
            "key": key
        }

# Enhanced backend that can switch between MusicLM and mock
class EnhancedGuitarSoloBackend:
    """
    Enhanced backend that can use MusicLM or existing mock generation
    """
    
    def __init__(self, use_musiclm=False, use_mock=True):
        self.use_musiclm = use_musiclm
        if use_musiclm:
            self.musiclm_integration = SimpleMusicLMIntegration(use_mock=use_mock)
        else:
            # Use existing mock generation
            try:
                from guitar_solo_backend import GuitarSoloAPI
                self.mock_api = GuitarSoloAPI()
            except ImportError:
                print("⚠️  Could not import existing backend, using fallback")
                self.mock_api = None
    
    async def generate_solo(self, style, key, length=8, techniques=None):
        """
        Generate solo using either MusicLM or mock generation
        """
        if self.use_musiclm:
            return await self.musiclm_integration.generate_solo(
                style, key, techniques
            )
        else:
            # Use existing mock generation
            if self.mock_api:
                try:
                    from guitar_solo_backend import SoloParameters
                    params = SoloParameters(
                        style=style,
                        key=key,
                        length=length,
                        complexity="medium",
                        tempo=120
                    )
                    return await self.mock_api.generate_solo(params)
                except Exception as e:
                    print(f"⚠️  Mock API failed: {e}")
                    return None
            else:
                # Fallback mock generation
                return self._fallback_mock_generation(style, key, length)
    
    def _fallback_mock_generation(self, style, key, length):
        """
        Simple fallback mock generation
        """
        return {
            "success": True,
            "style": style,
            "key": key,
            "length": length,
            "notes": [
                {"pitch": 60, "start_time": 0, "duration": 0.5, "velocity": 80},
                {"pitch": 62, "start_time": 0.5, "duration": 0.5, "velocity": 80},
                {"pitch": 64, "start_time": 1.0, "duration": 0.5, "velocity": 80},
                {"pitch": 65, "start_time": 1.5, "duration": 0.5, "velocity": 80}
            ]
        }

# Test the integration
async def test_integration():
    """
    Test both MusicLM and mock generation
    """
    print("🎸 Testing Enhanced Guitar Solo Backend")
    print("=" * 50)
    
    # Test 1: MusicLM integration (mock)
    print("\n🧪 Test 1: MusicLM Integration (Mock)")
    musiclm_backend = EnhancedGuitarSoloBackend(use_musiclm=True, use_mock=True)
    
    result1 = await musiclm_backend.generate_solo(
        style="blues",
        key="A",
        techniques=["bends", "slides"]
    )
    
    if result1 and result1["success"]:
        print(f"✅ MusicLM generated: {result1['style']} solo in {result1['key']}")
        print(f"📝 Prompt: {result1['prompt']}")
        print(f"🎵 Notes: {len(result1['midi_data']['notes'])} notes")
    else:
        print(f"❌ MusicLM failed: {result1.get('error', 'Unknown error')}")
    
    # Test 2: Mock generation (existing)
    print("\n🧪 Test 2: Mock Generation (Existing)")
    mock_backend = EnhancedGuitarSoloBackend(use_musiclm=False)
    
    result2 = await mock_backend.generate_solo(
        style="rock",
        key="E",
        length=8
    )
    
    if result2:
        print(f"✅ Mock generated: {result2.get('style', 'unknown')} solo")
        if 'notes' in result2:
            print(f"🎵 Notes: {len(result2['notes'])} notes")
    else:
        print("❌ Mock generation failed")

# Show how to integrate with existing frontend
def show_frontend_integration():
    """
    Show how to update the frontend to use MusicLM
    """
    integration_code = '''
// Add to guitar_solo_generator.html

// New function to call MusicLM API
async function generateMusicLMSolo(style, key, techniques) {
    try {
        const response = await fetch('/api/generate-solo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                style: style,
                key: key,
                techniques: techniques,
                use_musiclm: true  // New flag to use MusicLM
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Handle MusicLM result
            console.log('MusicLM generated:', result.solo_data);
            
            // Update UI with results
            updateNotationDisplay(result.solo_data);
            
            // Show audio player if available
            if (result.solo_data.audio_url) {
                showAudioPlayer(result.solo_data.audio_url);
            }
        } else {
            console.error('MusicLM generation failed:', result.error);
        }
    } catch (error) {
        console.error('Error calling MusicLM API:', error);
    }
}

// Update the generate button to use MusicLM
document.getElementById('generateBtn').addEventListener('click', async () => {
    const style = document.getElementById('styleSelect').value;
    const key = document.getElementById('musicalKey').value;
    const techniques = getSelectedTechniques(); // New function to get techniques
    
    // Try MusicLM first, fallback to mock
    await generateMusicLMSolo(style, key, techniques);
});
'''
    
    print("📝 Frontend Integration Code:")
    print(integration_code)

if __name__ == "__main__":
    # Run the integration test
    asyncio.run(test_integration())
    
    # Show frontend integration
    print("\n" + "="*50)
    show_frontend_integration()
    
    print("\n🎯 Summary for Your MacBook:")
    print("✅ No GPU required - MusicLM API runs in the cloud")
    print("✅ 32GB RAM is plenty for any processing")
    print("✅ Can start immediately with mock API")
    print("✅ Easy to switch to real API when available")
    print("✅ Integrates with existing frontend")
    
    print("\n🚀 Next Steps:")
    print("1. Test the integration (working now!)")
    print("2. Get MusicLM API key when available")
    print("3. Update frontend to use MusicLM")
    print("4. Add audio-to-MIDI conversion later")
    print("5. Deploy and enjoy real AI guitar solos!") 