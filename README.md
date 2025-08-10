# Classical Guitar Learning Platform

A lightweight web application for practicing classical guitar. The project combines a Flask
REST API with a browser-based frontend that uses Magenta.js to render and generate musical
exercises.

## Features

- Upload MIDI files for analysis and training.
- Generate scale, chord, and exercise data via the API.
- Track practice progress in JSON files.

## Project Structure

```
music-ai-final/
├── classical_guitar_learning/
│   ├── backend/   # Flask API
│   └── frontend/  # Static HTML/JS interface
├── requirements.txt
└── README.md
```

## Getting Started

### Backend

```bash
pip install -r requirements.txt
python classical_guitar_learning/backend/main.py
```

The API will be available at `http://localhost:5000`.

### Frontend

Open `classical_guitar_learning/frontend/index.html` in your browser to use the interface.

## Next Steps

- Add authentication and a persistent database for user data.
- Bundle frontend assets with a build tool.
- Add automated tests for the API and UI.

