from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
UPLOAD_FOLDER = "uploads"
EXERCISES_FOLDER = "exercises"
USER_DATA_FOLDER = "user_data"

# Ensure directories exist
for folder in [UPLOAD_FOLDER, EXERCISES_FOLDER, USER_DATA_FOLDER]:
    os.makedirs(folder, exist_ok=True)


@app.route("/")
def home():
    return jsonify(
        {
            "message": "Classical Guitar Learning Platform API",
            "version": "1.0.0",
            "endpoints": {
                "upload_midi": "/api/upload-midi",
                "get_exercises": "/api/exercises",
                "save_progress": "/api/progress",
                "get_scales": "/api/scales",
                "get_chords": "/api/chords",
            },
        }
    )


@app.route("/api/upload-midi", methods=["POST"])
def upload_midi():
    """Handle MIDI file uploads for training"""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if file and file.filename.lower().endswith((".mid", ".midi")):
        filename = f"{datetime.now().isoformat()}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        return jsonify(
            {
                "message": "File uploaded successfully",
                "filename": filename,
                "filepath": filepath,
            }
        )

    return jsonify({"error": "Invalid file type. Please upload a MIDI file."}), 400


@app.route("/api/exercises")
def get_exercises():
    """Get available classical guitar exercises"""
    exercises = {
        "beginner": [
            {
                "id": "scales_major_c",
                "name": "C Major Scale",
                "description": "Basic C major scale in first position",
                "difficulty": "beginner",
                "techniques": ["fingering", "position_playing"],
            },
            {
                "id": "arpeggios_basic",
                "name": "Basic Arpeggios",
                "description": "Simple arpeggiated patterns",
                "difficulty": "beginner",
                "techniques": ["fingerpicking", "arpeggios"],
            },
        ],
        "intermediate": [
            {
                "id": "scales_chromatic",
                "name": "Chromatic Scales",
                "description": "Chromatic scale exercises across the fretboard",
                "difficulty": "intermediate",
                "techniques": ["chromatic_movement", "position_shifts"],
            },
            {
                "id": "bach_invention_1",
                "name": "Bach Invention No. 1 (Simplified)",
                "description": "Simplified arrangement of Bach's first invention",
                "difficulty": "intermediate",
                "techniques": ["counterpoint", "independence"],
            },
        ],
        "advanced": [
            {
                "id": "villa_lobos_etude",
                "name": "Villa-Lobos Etude No. 1",
                "description": "Classical etude focusing on right-hand technique",
                "difficulty": "advanced",
                "techniques": ["tremolo", "advanced_fingerpicking"],
            }
        ],
    }
    return jsonify(exercises)


@app.route("/api/scales")
def get_scales():
    """Get scale patterns for classical guitar"""
    scales = {
        "major": {
            "pattern": [2, 2, 1, 2, 2, 2, 1],
            "positions": {
                "C": {"frets": [0, 2, 4, 5, 7, 9, 11], "string": 6},
                "G": {"frets": [3, 5, 7, 8, 10, 12, 14], "string": 6},
            },
        },
        "minor_natural": {
            "pattern": [2, 1, 2, 2, 1, 2, 2],
            "positions": {
                "A": {"frets": [0, 2, 3, 5, 7, 8, 10], "string": 5},
                "E": {"frets": [0, 2, 3, 5, 7, 8, 10], "string": 6},
            },
        },
    }
    return jsonify(scales)


@app.route("/api/chords")
def get_chords():
    """Get chord shapes and progressions"""
    chords = {
        "basic_triads": {
            "C_major": {
                "fingering": [0, 1, 0, 2, 3, 0],
                "strings": ["E", "A", "D", "G", "B", "E"],
                "frets": [None, 3, 2, 0, 1, 0],
            },
            "A_minor": {
                "fingering": [0, 0, 2, 2, 1, 0],
                "strings": ["E", "A", "D", "G", "B", "E"],
                "frets": [0, 0, 2, 2, 1, 0],
            },
        },
        "progressions": {
            "basic_classical": ["C", "Am", "F", "G"],
            "andalusian": ["Am", "G", "F", "E"],
        },
    }
    return jsonify(chords)


@app.route("/api/progress", methods=["POST"])
def save_progress():
    """Save user practice progress"""
    data = request.get_json()
    user_id = data.get("user_id", "anonymous")
    exercise_id = data.get("exercise_id")
    score = data.get("score", 0)
    notes_played = data.get("notes_played", [])

    progress_data = {
        "user_id": user_id,
        "exercise_id": exercise_id,
        "score": score,
        "notes_played": notes_played,
        "timestamp": datetime.now().isoformat(),
        "session_duration": data.get("session_duration", 0),
    }

    # Save to file (in production, use a proper database)
    progress_file = os.path.join(USER_DATA_FOLDER, f"{user_id}_progress.json")

    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(progress_data)

    with open(progress_file, "w") as f:
        json.dump(existing_data, f, indent=2)

    return jsonify({"message": "Progress saved successfully"})


@app.route("/api/progress/<user_id>")
def get_progress(user_id):
    """Get user progress data"""
    progress_file = os.path.join(USER_DATA_FOLDER, f"{user_id}_progress.json")

    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            progress_data = json.load(f)
        return jsonify(progress_data)
    else:
        return jsonify([])


if __name__ == "__main__":
    print("🎼 Classical Guitar Learning Platform Backend")
    print("Starting server on http://localhost:5000")
    app.run(debug=True, port=5000)
