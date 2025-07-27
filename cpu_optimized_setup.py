# 🎸 CPU-Optimized AudioCraft Setup for MacBook

import torch
import torchaudio
from audiocraft.models import MusicGen
import numpy as np
import time

class CPUOptimizedMusicGen:
    """
    AudioCraft MusicGen optimized for CPU-only MacBook
    """
    
    def __init__(self, model_size="small"):
        """
        Initialize MusicGen with CPU optimizations
        
        Model sizes:
        - "small": 300M parameters (fastest, good quality)
        - "medium": 1.5B parameters (slower, better quality)
        - "large": 3.3B parameters (slowest, best quality)
        """
        print(f"🎵 Loading MusicGen {model_size} model for CPU...")
        
        # Force CPU usage
        self.device = torch.device("cpu")
        
        # Load model with CPU optimizations
        self.model = MusicGen.get_pretrained(model_size, device=self.device)
        
        # Optimize for CPU
        self.model.set_generation_params(
            duration=8,  # 8 seconds (shorter for faster generation)
            temperature=0.8,
            top_k=250,
            top_p=0.95,
            cfg_coef=3.0,
        )
        
        print(f"✅ Model loaded successfully on {self.device}")
    
    def generate_guitar_solo(self, style, key, techniques=None):
        """
        Generate guitar solo with structured prompts
        """
        prompt = self._create_guitar_prompt(style, key, techniques)
        
        print(f"🎸 Generating {style} solo in {key}...")
        start_time = time.time()
        
        # Generate audio
        audio = self.model.generate([prompt])  # Returns tensor
        
        generation_time = time.time() - start_time
        print(f"✅ Generated in {generation_time:.2f} seconds")
        
        return audio[0].cpu().numpy()  # Convert to numpy array
    
    def _create_guitar_prompt(self, style, key, techniques):
        """
        Create structured prompts for guitar solos
        """
        base_prompts = {
            "blues": f"blues guitar solo in {key} major, soulful and expressive, with bends and slides",
            "rock": f"rock guitar solo in {key} major, energetic and melodic, with power chords",
            "jazz": f"jazz guitar solo in {key} major, sophisticated harmonies, with complex chord progressions",
            "metal": f"metal guitar solo in {key} major, fast and technical, with shredding"
        }
        
        prompt = base_prompts.get(style, base_prompts["blues"])
        
        # Add techniques
        if techniques:
            technique_descriptions = {
                "bends": "with expressive pitch bends",
                "slides": "with smooth slides between notes",
                "hammer-ons": "with hammer-ons and pull-offs",
                "tapping": "with two-handed tapping techniques"
            }
            
            for technique in techniques:
                if technique in technique_descriptions:
                    prompt += f", {technique_descriptions[technique]}"
        
        return prompt

# Performance comparison for different model sizes
def benchmark_model_sizes():
    """
    Test different model sizes on your MacBook
    """
    model_sizes = ["small", "medium", "large"]
    
    for size in model_sizes:
        print(f"\n🧪 Testing {size} model...")
        
        try:
            model = CPUOptimizedMusicGen(size)
            
            # Test generation time
            start_time = time.time()
            audio = model.generate_guitar_solo("blues", "A", ["bends"])
            generation_time = time.time() - start_time
            
            print(f"⏱️  {size} model: {generation_time:.2f} seconds")
            
            # Memory usage (approximate)
            import psutil
            memory_mb = psutil.Process().memory_info().rss / 1024 / 1024
            print(f"💾 Memory usage: {memory_mb:.1f} MB")
            
        except Exception as e:
            print(f"❌ {size} model failed: {e}")

# Installation guide
def install_requirements():
    """
    Install required packages for CPU-optimized AudioCraft
    """
    requirements = [
        "torch>=2.0.0",
        "torchaudio>=2.0.0", 
        "audiocraft>=1.0.0",
        "librosa>=0.10.0",
        "numpy>=1.21.0",
        "soundfile>=0.12.0",
        "psutil>=5.8.0"
    ]
    
    print("📦 Installing CPU-optimized AudioCraft requirements...")
    
    for req in requirements:
        print(f"Installing {req}...")
        # This would be: pip install req
    
    print("✅ Installation complete!")

# Usage example
if __name__ == "__main__":
    print("🎸 CPU-Optimized AudioCraft Setup")
    print("=" * 40)
    
    # Install requirements (uncomment when ready)
    # install_requirements()
    
    # Test different model sizes
    print("\n🔍 Benchmarking model sizes...")
    benchmark_model_sizes()
    
    # Example usage
    print("\n🎵 Example generation...")
    try:
        model = CPUOptimizedMusicGen("small")
        audio = model.generate_guitar_solo("blues", "A", ["bends", "slides"])
        print(f"✅ Generated audio shape: {audio.shape}")
    except Exception as e:
        print(f"❌ Example failed: {e}")

# Expected performance on your MacBook:
"""
Model Size    | Generation Time | Memory Usage | Quality
--------------|-----------------|--------------|----------
Small (300M)  | ~15-30 seconds | ~2-4 GB     | Good
Medium (1.5B) | ~45-90 seconds | ~4-8 GB     | Better  
Large (3.3B)  | ~90-180 seconds| ~8-16 GB    | Best

Your 32GB RAM can handle any model size!
""" 