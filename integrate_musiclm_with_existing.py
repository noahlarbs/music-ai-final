# 🎸 Integrate MusicLM with Existing Guitar Solo Generator

import asyncio
import json
from musiclm_api_setup import MusicLMBackendIntegration
from audio_to_midi_pipeline import AudioToMIDIConverter

class MusicLMIntegration:
    """
    Integrate MusicLM API with existing guitar solo generator
    """
    
    def __init__(self, use_mock=True):
        self.musiclm = MusicLMBackendIntegration(use_mock=use_mock)
        self.converter = AudioToMIDIConverter()
    
    async def generate_complete_solo(self, style, key, techniques=None):
        """
        Complete pipeline: MusicLM → Audio → MIDI → Tablature
        """
        print(f"🎸 Generating {style} solo in {key}...")
        
        # Step 1: Generate audio with MusicLM
        result = await self.musiclm.generate_solo(style, key, techniques)
        
        if result["status"] != "success":
            return {
                "success": False,
                "error": result.get("error", "Unknown error")
            }
        
        # Step 2: Convert audio to MIDI (mock for now)
        print("🔄 Converting audio to MIDI...")
        midi_file = "generated_solo.mid"
        
        # Step 3: Generate tablature from MIDI
        print("📝 Generating tablature...")
        tablature = self._generate_tablature_from_midi(midi_file)
        
        return {
            "success": True,
            "style": style,
            "key": key,
            "techniques": techniques,
            "audio_url": result["audio_url"],
            "midi_file": midi_file,
            "tablature": tablature,
            "prompt": result["prompt"]
        }
    
    def _generate_tablature_from_midi(self, midi_file):
        """
        Generate tablature from MIDI file
        This would use the existing tablature generation logic
        """
        # Mock tablature for now
        return {
            "strings": [
                "e|---5-7-8-10-12---|",
                "B|---5-7-8-10-12---|", 
                "G|---5-7-8-10-12---|",
                "D|---5-7-8-10-12---|",
                "A|---5-7-8-10-12---|",
                "E|---5-7-8-10-12---|"
            ],
            "style": "blues",
            "key": "A"
        }

# Update existing backend to use MusicLM
class EnhancedGuitarSoloBackend:
    """
    Enhanced backend that can use MusicLM or mock generation
    """
    
    def __init__(self, use_musiclm=False, use_mock=True):
        self.use_musiclm = use_musiclm
        if use_musiclm:
            self.musiclm_integration = MusicLMIntegration(use_mock=use_mock)
        else:
            # Use existing mock generation
            from guitar_solo_backend import GuitarSoloAPI
            self.mock_api = GuitarSoloAPI()
    
    async def generate_solo(self, style, key, length=8, techniques=None):
        """
        Generate solo using either MusicLM or mock generation
        """
        if self.use_musiclm:
            return await self.musiclm_integration.generate_complete_solo(
                style, key, techniques
            )
        else:
            # Use existing mock generation
            from guitar_solo_backend import SoloParameters
            params = SoloParameters(
                style=style,
                key=key,
                length=length,
                complexity="medium",
                tempo=120
            )
            return await self.mock_api.generate_solo(params)

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
    
    if result1["success"]:
        print(f"✅ MusicLM generated: {result1['style']} solo in {result1['key']}")
        print(f"📝 Prompt: {result1['prompt']}")
    else:
        print(f"❌ MusicLM failed: {result1['error']}")
    
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
    else:
        print("❌ Mock generation failed")

# Update the existing API server
def update_api_server():
    """
    Show how to update the existing api_server.py to use MusicLM
    """
    update_code = '''
# Add to api_server.py
from integrate_musiclm_with_existing import EnhancedGuitarSoloBackend

# Initialize with MusicLM (mock for testing)
guitar_api = EnhancedGuitarSoloBackend(use_musiclm=True, use_mock=True)

# Update the generate-solo endpoint
@app.post("/api/generate-solo")
async def generate_solo(request: SoloRequest):
    try:
        result = await guitar_api.generate_solo(
            style=request.style,
            key=request.key,
            length=request.length,
            techniques=request.techniques
        )
        
        if result["success"]:
            return SoloResponse(
                success=True,
                solo_data=result,
                message="Solo generated successfully"
            )
        else:
            return SoloResponse(
                success=False,
                error=result["error"]
            )
    except Exception as e:
        return SoloResponse(
            success=False,
            error=str(e)
        )
'''
    
    print("📝 To integrate with existing API server, add this code:")
    print(update_code)

if __name__ == "__main__":
    # Run the integration test
    asyncio.run(test_integration())
    
    # Show how to update API server
    print("\n" + "="*50)
    update_api_server()
    
    print("\n🎯 Next Steps:")
    print("1. Get MusicLM API key (if available)")
    print("2. Update api_server.py with the integration code")
    print("3. Test with real MusicLM API calls")
    print("4. Implement audio-to-MIDI conversion")
    print("5. Connect to existing frontend") 