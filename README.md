# AI Guitar Solo Generator

A web-based application to generate AI-powered guitar solos. This project allows users to specify style, key, and other parameters to create unique musical pieces.

## Features

- **Multiple Styles**: Generate solos in styles like Blues, Rock, Metal, Jazz, and Country.
- **Key-Aware Generation**: Solos are generated in the specified musical key.
- **Technique Selection**: Include techniques like bends, slides, and vibrato.
- **Tablature Display**: View the generated solo as guitar tablature using VexTab.
- **MIDI Download**: Download the generated solo as a MIDI file.

## How to Run

### Prerequisites

- Python 3.7+
- A Python virtual environment tool (like `venv`)

### 1. Setup the Backend

First, set up and run the Python backend which handles the AI generation.

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install the required Python packages
pip install -r requirements.txt

# 3. Start the FastAPI server
python3 api_server.py
```

The backend server will start on `http://localhost:8000`.

### 2. Open the Frontend

Open the `guitar_solo_generator.html` file in your web browser.

```bash
# On macOS
open guitar_solo_generator.html

# On Windows
start guitar_solo_generator.html

# On Linux
xdg-open guitar_solo_generator.html
```

You can now use the interface to generate guitar solos.

## Project Structure

- `guitar_solo_generator.html`: The main frontend file containing the UI and client-side logic.
- `api_server.py`: The FastAPI server that exposes the generation endpoints.
- `guitar_solo_backend.py`: The core backend logic for generating solos. Contains a mock generator and an (optional) integration with a SpectroStream model.
- `requirements.txt`: Python dependencies for the backend.
- `README.md`: This file. 