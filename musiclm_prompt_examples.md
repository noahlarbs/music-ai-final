# 🎵 MusicLM Structured Prompt Examples

## 🎯 **The Challenge: Audio → MIDI → Tablature**

MusicLM outputs **audio files**, not MIDI. We need to:
1. **Create structured prompts** from user selections
2. **Convert audio to MIDI** using pitch detection
3. **Generate tablature** from MIDI

## 📝 **Structured Prompt Examples**

### **User Selection:**
- Style: Blues
- Key: A major
- Length: 8 bars
- Techniques: Bends, Slides

### **Generated MusicLM Prompt:**
```
"blues guitar solo in A major, soulful and expressive, 8 bars, with bends and slides, 
call-and-response phrasing, pentatonic scale runs, 120 BPM, clean electric guitar tone"
```

### **More Examples:**

#### **Rock Solo (E major, 16 bars, Power Chords)**
```
"rock guitar solo in E major, energetic and melodic, 16 bars, with power chords and fast runs, 
distorted electric guitar, 140 BPM, aggressive phrasing with palm muting"
```

#### **Jazz Solo (C major, 12 bars, Complex Harmonies)**
```
"jazz guitar solo in C major, sophisticated harmonies, 12 bars, with complex chord progressions, 
clean jazz guitar tone, 100 BPM, chromatic passing tones and altered scales"
```

#### **Metal Solo (D minor, 8 bars, Shredding)**
```
"metal guitar solo in D minor, fast and technical, 8 bars, with shredding and tapping, 
high gain distortion, 160 BPM, harmonic minor scale runs and sweep picking"
```

## 🔄 **Complete Pipeline Example**

```python
# User makes selections in the UI
user_selections = {
    "style": "blues",
    "key": "A",
    "length": 8,
    "techniques": ["bends", "slides"]
}

# 1. Create structured prompt
prompt = create_musiclm_prompt(user_selections)
# Result: "blues guitar solo in A major, soulful and expressive, 8 bars, with bends and slides..."

# 2. Call MusicLM API
audio_file = await musiclm_api.generate(prompt, duration=16)

# 3. Convert audio to MIDI
midi_file = audio_to_midi_converter.convert(audio_file)

# 4. Generate tablature
tablature = midi_to_tablature_converter.convert(midi_file)
```

## 🎼 **Prompt Engineering Strategy**

### **Style-Specific Elements:**
```python
style_prompts = {
    "blues": {
        "mood": "soulful and expressive",
        "scales": "pentatonic scale runs",
        "phrasing": "call-and-response phrasing",
        "techniques": "bends and slides",
        "tempo": "120 BPM"
    },
    "rock": {
        "mood": "energetic and melodic",
        "scales": "power chords and fast runs",
        "phrasing": "aggressive phrasing",
        "techniques": "palm muting and power chords",
        "tempo": "140 BPM"
    },
    "jazz": {
        "mood": "sophisticated harmonies",
        "scales": "chromatic passing tones",
        "phrasing": "complex chord progressions",
        "techniques": "altered scales",
        "tempo": "100 BPM"
    },
    "metal": {
        "mood": "fast and technical",
        "scales": "harmonic minor scale runs",
        "phrasing": "sweep picking",
        "techniques": "shredding and tapping",
        "tempo": "160 BPM"
    }
}
```

### **Key-Specific Elements:**
```python
key_prompts = {
    "A": "A major",
    "E": "E major", 
    "C": "C major",
    "D": "D minor",
    "G": "G major"
}
```

### **Technique-Specific Elements:**
```python
technique_prompts = {
    "bends": "with expressive pitch bends",
    "slides": "with smooth slides between notes",
    "hammer-ons": "with hammer-ons and pull-offs",
    "tapping": "with two-handed tapping techniques",
    "vibrato": "with wide vibrato",
    "sweep": "with sweep picking arpeggios"
}
```

## ⚠️ **Challenges with Audio-to-MIDI Conversion**

### **1. Pitch Detection Accuracy**
- **Problem**: Audio contains harmonics, noise, effects
- **Solution**: Use advanced pitch detection algorithms (librosa.piptrack)

### **2. Note Onset Detection**
- **Problem**: Guitar techniques like slides blur note boundaries
- **Solution**: Use onset detection + pitch tracking

### **3. Guitar-Specific Issues**
- **Problem**: Bends, slides, vibrato don't translate well to MIDI
- **Solution**: Post-process MIDI to add guitar techniques

### **4. Timing Accuracy**
- **Problem**: Audio timing vs MIDI timing differences
- **Solution**: Quantize to grid and adjust for human feel

## 🎯 **Alternative: Direct MIDI Generation**

Instead of Audio → MIDI conversion, consider:

### **1. AudioCraft with MIDI Output**
```python
# Some models can output MIDI directly
model = load_audiocraft_model("musicgen-midi")
midi = model.generate_midi(prompt)
```

### **2. Custom Guitar Model**
```python
# Train a model specifically for guitar MIDI generation
model = GuitarMIDIModel()
midi = model.generate(style, key, techniques)
```

### **3. Hybrid Approach**
```python
# Use MusicLM for style, then apply guitar-specific rules
audio = musiclm.generate(prompt)
midi = apply_guitar_rules(audio_to_midi(audio))
```

## 📊 **Quality Comparison**

| Method | Audio Quality | MIDI Accuracy | Guitar Techniques | Setup Complexity |
|--------|---------------|---------------|-------------------|------------------|
| MusicLM + Audio→MIDI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| AudioCraft Local | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Custom Guitar Model | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🚀 **Recommended Approach**

### **Phase 1: MusicLM + Audio→MIDI**
- **Pros**: High audio quality, immediate implementation
- **Cons**: Complex conversion pipeline
- **Timeline**: 2-3 weeks

### **Phase 2: AudioCraft Local**
- **Pros**: Better MIDI output, no API costs
- **Cons**: Requires GPU, more setup
- **Timeline**: 1-2 months

### **Phase 3: Custom Guitar Model**
- **Pros**: Perfect for guitar, direct MIDI output
- **Cons**: Significant development time
- **Timeline**: 3-6 months

The key insight: **MusicLM gives us high-quality musical intelligence**, but we need to solve the **audio-to-MIDI conversion challenge** to get proper tablature. 