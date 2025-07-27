# 🎵 MusicLM API Integration (No Local GPU Required)

import aiohttp
import asyncio
import json
import base64
from typing import Dict, List, Optional

class MusicLMAPI:
    """
    MusicLM API integration for cloud-based generation
    No local GPU required!
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.musiclm.google.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_guitar_solo(self, style: str, key: str, techniques: List[str] = None) -> Dict:
        """
        Generate guitar solo using MusicLM API
        """
        prompt = self._create_musiclm_prompt(style, key, techniques)
        
        payload = {
            "text_prompt": prompt,
            "duration": 16,  # 16 seconds
            "temperature": 0.8,
            "top_k": 250,
            "top_p": 0.95
        }
        
        print(f"🎵 Calling MusicLM API with prompt: {prompt}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/generate",
                headers=self.headers,
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "audio_url": result.get("audio_url"),
                        "duration": result.get("duration"),
                        "prompt": prompt
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"API Error {response.status}: {error_text}",
                        "prompt": prompt
                    }
    
    def _create_musiclm_prompt(self, style: str, key: str, techniques: List[str] = None) -> str:
        """
        Create structured prompts for MusicLM
        """
        base_prompts = {
            "blues": f"blues guitar solo in {key} major, soulful and expressive, with bends and slides, call-and-response phrasing, pentatonic scale runs, 120 BPM, clean electric guitar tone",
            "rock": f"rock guitar solo in {key} major, energetic and melodic, with power chords and fast runs, distorted electric guitar, 140 BPM, aggressive phrasing with palm muting",
            "jazz": f"jazz guitar solo in {key} major, sophisticated harmonies, with complex chord progressions, clean jazz guitar tone, 100 BPM, chromatic passing tones and altered scales",
            "metal": f"metal guitar solo in {key} major, fast and technical, with shredding and tapping, high gain distortion, 160 BPM, harmonic minor scale runs and sweep picking"
        }
        
        prompt = base_prompts.get(style, base_prompts["blues"])
        
        # Add specific techniques
        if techniques:
            technique_descriptions = {
                "bends": "with expressive pitch bends and vibrato",
                "slides": "with smooth slides between notes",
                "hammer-ons": "with hammer-ons and pull-offs for fluid playing",
                "tapping": "with two-handed tapping techniques",
                "vibrato": "with wide vibrato and expression",
                "sweep": "with sweep picking arpeggios"
            }
            
            for technique in techniques:
                if technique in technique_descriptions:
                    prompt += f", {technique_descriptions[technique]}"
        
        return prompt

# Mock implementation for testing (no API key required)
class MockMusicLMAPI:
    """
    Mock MusicLM API for testing without real API key
    """
    
    def __init__(self):
        self.base_url = "https://api.musiclm.google.com/v1"
    
    async def generate_guitar_solo(self, style: str, key: str, techniques: List[str] = None) -> Dict:
        """
        Mock generation that simulates API response
        """
        prompt = self._create_musiclm_prompt(style, key, techniques)
        
        print(f"🎵 [MOCK] Calling MusicLM API with prompt: {prompt}")
        
        # Simulate API delay
        await asyncio.sleep(2)
        
        # Return mock response
        return {
            "success": True,
            "audio_url": "https://example.com/generated_solo.wav",
            "duration": 16,
            "prompt": prompt,
            "mock": True
        }
    
    def _create_musiclm_prompt(self, style: str, key: str, techniques: List[str] = None) -> str:
        """
        Same prompt creation logic as real API
        """
        base_prompts = {
            "blues": f"blues guitar solo in {key} major, soulful and expressive, with bends and slides, call-and-response phrasing, pentatonic scale runs, 120 BPM, clean electric guitar tone",
            "rock": f"rock guitar solo in {key} major, energetic and melodic, with power chords and fast runs, distorted electric guitar, 140 BPM, aggressive phrasing with palm muting",
            "jazz": f"jazz guitar solo in {key} major, sophisticated harmonies, with complex chord progressions, clean jazz guitar tone, 100 BPM, chromatic passing tones and altered scales",
            "metal": f"metal guitar solo in {key} major, fast and technical, with shredding and tapping, high gain distortion, 160 BPM, harmonic minor scale runs and sweep picking"
        }
        
        prompt = base_prompts.get(style, base_prompts["blues"])
        
        if techniques:
            technique_descriptions = {
                "bends": "with expressive pitch bends and vibrato",
                "slides": "with smooth slides between notes",
                "hammer-ons": "with hammer-ons and pull-offs for fluid playing",
                "tapping": "with two-handed tapping techniques"
            }
            
            for technique in techniques:
                if technique in technique_descriptions:
                    prompt += f", {technique_descriptions[technique]}"
        
        return prompt

# Integration with existing backend
class MusicLMBackendIntegration:
    """
    Integrate MusicLM with existing guitar solo backend
    """
    
    def __init__(self, use_mock=True):
        if use_mock:
            self.api = MockMusicLMAPI()
        else:
            # You would need a real API key here
            api_key = "your_musiclm_api_key_here"
            self.api = MusicLMAPI(api_key)
    
    async def generate_solo(self, style: str, key: str, techniques: List[str] = None):
        """
        Generate solo using MusicLM API
        """
        result = await self.api.generate_guitar_solo(style, key, techniques)
        
        if result["success"]:
            # Convert audio to MIDI (using the pipeline we created)
            # This would use the audio_to_midi_pipeline.py
            return {
                "audio_url": result["audio_url"],
                "prompt": result["prompt"],
                "status": "success"
            }
        else:
            return {
                "error": result["error"],
                "status": "failed"
            }

# Example usage
async def test_musiclm_integration():
    """
    Test MusicLM integration
    """
    print("🎸 Testing MusicLM API Integration")
    print("=" * 40)
    
    # Use mock for testing
    integration = MusicLMBackendIntegration(use_mock=True)
    
    # Test different styles
    test_cases = [
        {"style": "blues", "key": "A", "techniques": ["bends", "slides"]},
        {"style": "rock", "key": "E", "techniques": ["hammer-ons"]},
        {"style": "jazz", "key": "C", "techniques": []},
        {"style": "metal", "key": "D", "techniques": ["tapping", "sweep"]}
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['style']} solo in {test_case['key']}")
        
        result = await integration.generate_solo(
            test_case["style"],
            test_case["key"], 
            test_case["techniques"]
        )
        
        if result["status"] == "success":
            print(f"✅ Generated: {result['audio_url']}")
            print(f"📝 Prompt: {result['prompt']}")
        else:
            print(f"❌ Failed: {result['error']}")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_musiclm_integration())

# Installation requirements for MusicLM API:
"""
pip install aiohttp
pip install asyncio

No GPU required! Just internet connection and API key.
""" 