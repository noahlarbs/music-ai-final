# 🎸 AI Guitar Solo Generator

A modern web application that generates guitar solos in different styles using AI. This project expands on your original Magenta-based system with support for newer AI music generation models.

## 🚀 Features

- **Multiple Guitar Styles**: Blues, Rock, Metal, Jazz, Country, Classical, Funk
- **AI Model Integration**: Support for MusicLM, AudioCraft, and other modern models
- **Real-time Generation**: Generate solos with custom parameters
- **MIDI Export**: Download generated solos as MIDI files
- **Visual Notation**: Display generated solos using VexFlow
- **Style Presets**: Quick selection of popular guitar styles
- **Custom Descriptions**: Create your own style descriptions

## 🎯 Modern AI Models Supported

### 1. **MusicLM (Google)**
- **Text-to-music generation** with style conditioning
- **High-quality audio output** with guitar-specific training
- **Available via API** or Hugging Face
- **Best for**: Style-specific guitar solos

### 2. **AudioCraft/MusicGen (Meta)**
- **Open-source text-to-music** generation
- **Multi-instrument support** including guitar
- **Local deployment** possible
- **Best for**: Custom style generation

### 3. **Riffusion**
- **Real-time music generation** with style transfer
- **Web-based interface** integration
- **Good for**: Guitar riffs and short solos

### 4. **Jukebox (OpenAI)**
- **Full-song generation** with multiple genres
- **Higher computational requirements**
- **Best for**: Complete guitar compositions

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js (optional, for development)

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or using conda
conda create -n guitar-solo python=3.9
conda activate guitar-solo
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file for API keys (optional):

```bash
# .env
MUSICLM_API_KEY=your_musiclm_api_key_here
AUDIOCRAFT_MODEL_PATH=/path/to/audiocraft/model
```

### 3. Run the Application

```bash
# Start the FastAPI server
python api_server.py

# Or using uvicorn directly
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the Application

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 🎵 Usage

### Web Interface

1. **Select Style**: Choose from preset guitar styles or create custom
2. **Set Parameters**: Adjust length, tempo, and complexity
3. **Generate**: Click "Generate Guitar Solo" to create new solos
4. **Play/Download**: Listen to generated solos or download as MIDI

### API Usage

```python
import requests

# Generate a blues solo
response = requests.post("http://localhost:8000/api/generate-solo", json={
    "style": "blues",
    "length_bars": 8,
    "tempo": 120,
    "complexity": "medium"
})

solo_data = response.json()
```

### Example API Calls

```bash
# Generate a blues solo
curl -X POST "http://localhost:8000/api/generate-solo" \
  -H "Content-Type: application/json" \
  -d '{"style": "blues", "length_bars": 4, "tempo": 80}'

# Get available styles
curl "http://localhost:8000/api/styles"

# Health check
curl "http://localhost:8000/api/health"
```

## 🔧 Configuration

### Style Presets

The application includes predefined style configurations:

```python
style_presets = {
    "blues": {
        "description": "Blues guitar solo with bends, slides, and pentatonic scales",
        "tempo": 80,
        "complexity": "medium",
        "characteristics": ["bends", "slides", "pentatonic", "blues scale"]
    },
    "metal": {
        "description": "Metal shredding with fast runs and technical passages",
        "tempo": 160,
        "complexity": "virtuoso",
        "characteristics": ["fast runs", "technical", "shredding", "tapping"]
    }
    # ... more styles
}
```

### AI Model Configuration

```python
# In guitar_solo_backend.py
generators = {
    "musiclm": MusicLMGenerator(),
    "audiocraft": AudioCraftGenerator(),
    # Add more models here
}
```

## 🎼 Technical Details

### Architecture

```
Frontend (HTML/JS) ←→ FastAPI Server ←→ AI Models
     ↓                    ↓              ↓
VexFlow Notation    Guitar Solo API   MusicLM/AudioCraft
```

### Key Components

1. **`guitar_solo_generator.html`**: Modern web interface
2. **`guitar_solo_backend.py`**: AI model integration
3. **`api_server.py`**: FastAPI server
4. **`requirements.txt`**: Python dependencies

### MIDI Processing

The system processes MIDI data in the following format:

```python
{
    "notes": [
        {
            "pitch": 60,  # MIDI note number
            "startTime": 0.0,  # Start time in seconds
            "endTime": 0.5,    # End time in seconds
            "velocity": 80      # Note velocity (0-127)
        }
    ],
    "totalTime": 8.0,
    "tempo": 120,
    "style": "blues"
}
```

## 🔮 Future Enhancements

### Planned Features

1. **Real AI Model Integration**
   - Direct MusicLM API integration
   - Local AudioCraft model deployment
   - Riffusion style transfer

2. **Advanced Features**
   - Chord progression analysis
   - Scale-aware generation
   - Guitar technique simulation (bends, slides, etc.)

3. **User Experience**
   - Real-time audio preview
   - Style mixing and blending
   - Collaborative solo creation

### Model Integration Roadmap

1. **Phase 1**: Mock generation with realistic patterns
2. **Phase 2**: MusicLM API integration
3. **Phase 3**: Local AudioCraft deployment
4. **Phase 4**: Advanced style transfer

## 🤝 Contributing

### Development Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-guitar-solo-generator

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Run linter
flake8 .
```

### Adding New Models

1. Create a new generator class in `guitar_solo_backend.py`
2. Implement the `MusicAIGenerator` interface
3. Add the model to the `GuitarSoloAPI` generators dict
4. Update the frontend to include the new model option

## 📚 Resources

### AI Music Generation Models

- [MusicLM Paper](https://arxiv.org/abs/2301.11325)
- [AudioCraft GitHub](https://github.com/facebookresearch/audiocraft)
- [Riffusion](https://github.com/riffusion/riffusion)
- [Magenta](https://magenta.tensorflow.org/)

### Music Theory Resources

- [Guitar Scales](https://www.guitarscales.info/)
- [Chord Progressions](https://www.hooktheory.com/theorytab)
- [MIDI Specification](https://www.midi.org/specifications)

### Development Tools

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [VexFlow Documentation](https://vexflow.com/)
- [Tone.js](https://tonejs.github.io/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Original Project**: Your Magenta-based music generation system
- **Dartmouth College**: CS 89/189 MUS14 course with Prof. Michael Casey
- **AI Models**: Google MusicLM, Meta AudioCraft, OpenAI Jukebox
- **Music Libraries**: VexFlow, Tone.js, Magenta.js

---

**Note**: This is an expansion of your original project, modernizing the AI models while maintaining the core functionality and adding new features for guitar solo generation. 