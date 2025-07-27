# 🎸 AI Guitar Solo Generator - Model Explanation

## 🤖 Current Model Status

### **What Model Are We Using?**

Currently, the system uses a **mock/placeholder generation system** that simulates AI behavior. Here's the breakdown:

#### **Phase 1: Mock Generation (Current)**
- **Purpose**: Demonstrates the framework and UI
- **How it works**: Uses mathematical algorithms to generate musically coherent patterns
- **Input**: Style, key, length, tempo, complexity
- **Output**: MIDI notes that follow the selected key and style

#### **Phase 2: Real AI Integration (Planned)**
- **MusicLM (Google)**: Text-to-music generation
- **AudioCraft (Meta)**: Open-source music generation
- **Custom Models**: Fine-tuned for guitar solos

## 🔧 How the Current System Works

### **1. Input Processing**
```python
# User selects these parameters:
style = "blues"           # Guitar style
key = "A"                 # Musical key
length_bars = 8           # Solo length
tempo = 120              # BPM
complexity = "medium"     # Difficulty level
```

### **2. Key-Aware Generation**
```python
# System looks up the key information:
key_info = {
    'A': {
        'notes': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
        'type': 'major'
    }
}

# Only uses notes that belong to the selected key
available_notes = [69, 71, 61, 62, 64, 66, 68]  # MIDI numbers
```

### **3. Style-Specific Patterns**
```python
# Different styles use different scale patterns:
scale_patterns = {
    'blues': [0, 3, 5, 6, 7, 10],      # Blues scale
    'rock': [0, 2, 4, 5, 7, 9, 11],    # Major scale
    'metal': [0, 2, 4, 5, 7, 9, 11],   # Minor scale
    'jazz': [0, 2, 3, 5, 7, 8, 10, 11] # Jazz scale
}
```

### **4. Note Generation Algorithm**
```python
for beat in range(total_beats):
    if random() < 0.8:  # 80% chance of playing a note
        note_pitch = random.choice(available_notes)
        note_pitch += random.choice([-12, 0, 12])  # Octave variation
        note_pitch = max(40, min(88, note_pitch))  # Guitar range
        
        notes.append({
            "pitch": note_pitch,
            "startTime": beat * beat_duration,
            "endTime": start_time + beat_duration * 0.8,
            "velocity": random.randint(60, 100)
        })
```

## 📊 What Inputs Does It Use?

### **Required Inputs:**
1. **Style** (`blues`, `rock`, `metal`, `jazz`, `country`, `classical`, `funk`)
2. **Key** (`A`, `E`, `Dm`, `G`, etc.)
3. **Length** (4, 8, 12, or 16 bars)
4. **Tempo** (60-200 BPM)
5. **Complexity** (`simple`, `medium`, `complex`, `virtuoso`)

### **Optional Inputs:**
1. **Custom Style Description** (text)
2. **Chord Progression** (e.g., "Am G F E")
3. **MIDI File Upload** (for influence)

### **How Inputs Are Used:**

#### **Style Input:**
- Determines scale patterns (blues pentatonic vs. jazz modes)
- Sets default tempo and complexity
- Influences note selection probability

#### **Key Input:**
- Filters available notes to only those in the key
- Determines major vs. minor scale patterns
- Sets the tonal center for the entire solo

#### **Length Input:**
- Calculates total beats: `length_bars * 4`
- Determines solo duration in seconds
- Affects note density and phrasing

#### **Tempo Input:**
- Sets beat duration: `60.0 / tempo`
- Influences note timing and rhythm
- Affects overall energy of the solo

#### **Complexity Input:**
- Changes note density (more notes = higher complexity)
- Affects octave range and variation
- Influences velocity (dynamics) range

## 🎵 Output Format

### **MIDI Data Structure:**
```json
{
    "notes": [
        {
            "pitch": 69,        // MIDI note number (A4)
            "startTime": 0.0,   // Start time in seconds
            "endTime": 0.5,     // End time in seconds
            "velocity": 80       // Note velocity (0-127)
        }
    ],
    "totalTime": 8.0,          // Total duration
    "tempo": 120,              // BPM
    "style": "blues",          // Style used
    "key": "A",                // Musical key
    "length_bars": 8,          // Number of bars
    "complexity": "medium"     // Complexity level
}
```

## 🔮 Real AI Model Integration

### **MusicLM Integration (Planned):**
```python
# Text prompt generation
prompt = f"{style_description}, {complexity_desc}, {length_desc} solo in the key of {key} at {tempo} BPM"

# API call to MusicLM
response = await musiclm_api.generate(
    prompt=prompt,
    duration=length_bars * 2,
    temperature=complexity_to_temperature(complexity)
)
```

### **AudioCraft Integration (Planned):**
```python
# Local model inference
model = load_audiocraft_model()
audio = model.generate(
    text_prompt=prompt,
    duration=length_bars * 2,
    temperature=complexity_to_temperature(complexity)
)
```

## 🎼 Notation Types

### **Sheet Music:**
- Uses VexFlow library
- Displays standard musical notation
- Shows note names, clefs, time signatures
- Professional music notation format

### **Guitar Tablature:**
- Shows fret positions on guitar strings
- String numbers (1-6) and fret numbers (0-24)
- Guitar-specific notation
- Easier for guitarists to read

## 🔧 Technical Architecture

```
User Input → Parameter Processing → Key Lookup → Style Pattern Selection → 
Note Generation → MIDI Conversion → Notation Rendering → Audio Playback
```

### **Key Components:**
1. **Frontend**: HTML/JS interface with real-time feedback
2. **Backend**: Python API with model integration
3. **Notation Engine**: VexFlow for sheet music and tablature
4. **Audio Engine**: Web Audio API for playback
5. **MIDI Processing**: Note conversion and export

## 🚀 Future Enhancements

### **Real AI Models:**
1. **MusicLM API**: Direct integration with Google's model
2. **AudioCraft Local**: Run Meta's model locally
3. **Custom Training**: Fine-tune models on guitar solo datasets

### **Advanced Features:**
1. **Chord Progression Analysis**: Generate solos that fit specific chord progressions
2. **Guitar Technique Simulation**: Bends, slides, hammer-ons, pull-offs
3. **Style Transfer**: Mix multiple styles together
4. **Real-time Collaboration**: Multiple users creating solos together

## 💡 Why This Approach?

### **Current Mock System Benefits:**
- ✅ **Fast**: Instant generation
- ✅ **Reliable**: No API dependencies
- ✅ **Educational**: Shows how AI music generation works
- ✅ **Framework Ready**: Easy to swap in real AI models

### **Real AI Benefits:**
- 🎵 **Musical Quality**: Much more sophisticated patterns
- 🎸 **Style Accuracy**: Better genre-specific characteristics
- 🎼 **Complexity**: More nuanced and interesting solos
- 🎯 **Creativity**: Truly novel musical ideas

## 🔍 Debugging the VexFlow Issue

The "missing variable vex" error occurs because:
1. VexFlow library might not be loading properly
2. Variable scope issues in the JavaScript
3. CDN loading problems

**Solution**: Added try-catch blocks and error handling to gracefully handle VexFlow errors.

---

**Next Steps**: 
1. Test the fixed VexFlow implementation
2. Integrate with real AI models (MusicLM/AudioCraft)
3. Add more sophisticated guitar techniques
4. Implement chord progression analysis 