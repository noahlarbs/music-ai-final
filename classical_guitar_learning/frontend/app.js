// Initialize Magenta.js models
const mvae = new mm.MusicVAE('https://storage.googleapis.com/magentadata/js/checkpoints/music_vae/mel_4bar_med_lokl_q2');
const midime = new mm.MidiMe({epochs: 100});

// Global variables
let noteSeq1 = null;
let quantNoteSeq1 = null;
let isTraining = false;
let isModelReady = false;

// DOM elements
const uploadButton = document.getElementById('uploadButton');
const trainButton = document.getElementById('trainButton');
const sampleButton = document.getElementById('sample');
const octaveSelector = document.getElementById('octaveSelector');
const temperatureSlider = document.getElementById('temperatureSlider');
const tempValueSpan = document.getElementById('tempValue');
const positionSelector = document.getElementById('positionSelector');
const initializationText = document.getElementById('initialization');
const epochsText = document.getElementById('epochsText');
const notationDiv = document.getElementById('notation');
const fileInput = document.getElementById('input');

// Event Listeners
uploadButton.addEventListener('click', upload);
trainButton.addEventListener('click', train);
sampleButton.addEventListener('click', sampleModel);
temperatureSlider.addEventListener('input', () => {
    tempValueSpan.textContent = temperatureSlider.value;
});

const TUNINGS = {
    standard: [64, 59, 55, 50, 45, 40] // EADGBe
};

const FRET_COUNT = 19;

/**
 * Returns all possible fret/string combinations for a given MIDI note.
 * @param {number} midi - The MIDI note number.
 * @param {Array<number>} tuning - The tuning of the guitar.
 * @returns {Array<{string: number, fret: number}>}
 */
function noteToFret(midi, tuning = TUNINGS.standard) {
    const locations = [];
    for (let i = 0; i < tuning.length; i++) {
        const fret = midi - tuning[i];
        if (fret >= 0 && fret <= FRET_COUNT) {
            locations.push({ string: i + 1, fret });
        }
    }
    return locations;
}

/**
 * Selects the best fret/string location based on the desired position.
 * @param {Array<{string: number, fret: number}>} locations - Possible locations for a note.
 * @param {number} position - The desired fretboard position.
 * @returns {{string: number, fret: number}|null}
 */
function getBestLocation(locations, position) {
    if (locations.length === 0) return null;
    if (position === 0) { // Automatic
        return locations.sort((a, b) => a.fret - b.fret)[0];
    }

    const validLocations = locations.filter(loc => {
        if (loc.fret === 0) return false;
        return loc.fret >= position && loc.fret < position + 5;
    });

    if (validLocations.length > 0) {
        return validLocations[0];
    } else if (locations.length > 0) {
        // Fallback to the lowest possible fret if no ideal position is found
        return locations.sort((a, b) => Math.abs(a.fret - position) - Math.abs(b.fret - position))[0];
    }
    return null;
}


/**
 * Updates the UI and button states based on the application's current state.
 */
function updateButtonStates() {
    if (isTraining) {
        trainButton.disabled = true;
        sampleButton.disabled = true;
        uploadButton.disabled = true;
        trainButton.textContent = '🧠 Training...';
    } else {
        trainButton.disabled = false;
        uploadButton.disabled = false;
        trainButton.textContent = '🧠 Train with File';
        sampleButton.disabled = !isModelReady;
    }
}

/**
 * Renders the MIDI note sequence to the screen using VexFlow.
 * @param {mm.NoteSequence} noteSeq - The NoteSequence to render.
 */
const renderMidi = (noteSeq) => {
    vexFlowRendering(noteSeq.notes);
};

/**
 * Uses VexFlow to render the notes as sheet music.
 * @param {Array<mm.NoteSequence.Note>} notes - An array of notes to render.
 */
const vexFlowRendering = (notes) => {
    clearNotation();
    
    const selectedPosition = parseInt(positionSelector.value, 10);
    
    // Convert notes to VexFlow format with positional information
    const formattedNotes = notes.map(note => {
        const locations = noteToFret(note.pitch);
        const bestLocation = getBestLocation(locations, selectedPosition);
        
        // Create the basic note string for VexFlow
        const vexNote = `${makeVex(note.pitch)}/q`;
        
        // Store location info for annotations (we'll add this feature back later)
        return {
            vexNote: vexNote,
            location: bestLocation,
            originalPitch: note.pitch
        };
    });
    
    // Use the original working VexFlow approach
    const vf = new Vex.Flow.Factory({
        renderer: { elementId: 'notation', width: 1000, height: 600 }
    });
    const score = vf.EasyScore();
    let yOffset = 10;
    
    // Create note groups
    let noteGroups = [];
    const notesPerGroup = 4;
    for (let i = 0; i < formattedNotes.length; i += notesPerGroup) {
        const group = formattedNotes.slice(i, i + notesPerGroup);
        const groupString = group.map(n => n.vexNote).join(", ");
        noteGroups.push({
            notes: groupString,
            locations: group.map(n => n.location)
        });
    }

    noteGroups.forEach((group, index) => {
        // Create a new system for each group of notes
        const system = vf.System({ x: 10, y: yOffset, width: 950, spaceBetweenStaves: 10 });
        system.addStave({
            voices: [score.voice(score.notes(group.notes, { stem: 'up' }))]
        }).addClef('treble').addTimeSignature('4/4');
        yOffset += 120;
    });

    vf.draw();
};

// Map of MIDI pitch values to note names
const noteMap = new Map([
    [0, 'C'], [1, 'C#'], [2, 'D'], [3, 'D#'], [4, 'E'], [5, 'F'],
    [6, 'F#'], [7, 'G'], [8, 'G#'], [9, 'A'], [10, 'A#'], [11, 'B']
]);

/**
 * Converts a MIDI pitch number to a VexFlow-compatible note string (e.g., "C4").
 * @param {number} note - The MIDI pitch number.
 * @returns {string} The VexFlow note string.
 */
const makeVex = (note) => {
    const newO = parseInt(octaveSelector.value, 10);          
    const noteName = noteMap.get(note % 12);          
    const octave = Math.floor(note / 12) - 1;
    const adjustedOctave = octave + newO;
    return `${noteName}${adjustedOctave}`;
};

/**
 * Handles the MIDI file upload process.
 */
async function upload() {
    const file = fileInput.files[0];
    if (file) {
        try {
            isModelReady = false;
            updateButtonStates();
            epochsText.innerHTML = "Epoch 0 / 100";
            
            noteSeq1 = await mm.blobToNoteSequence(file);
            quantNoteSeq1 = mm.sequences.quantizeNoteSequence(noteSeq1, 4);

            const displayedNotes = mm.sequences.clone(quantNoteSeq1);
            displayedNotes.notes = quantNoteSeq1.notes.slice(0, 16);
            renderMidi(displayedNotes);
            
            console.log("Successfully uploaded and displayed MIDI file");
        } catch (error) {
            console.error("Error uploading MIDI file:", error);
            alert("Error uploading MIDI file. Please try a different file.");
        }
    }
}

/**
 * Trains the MidiMe model with the uploaded MIDI file.
 */
async function train() {
    if (!quantNoteSeq1) {
        alert("Please upload a MIDI file first!");
        return;
    }
    
    isTraining = true;
    updateButtonStates();
    
    try {
        initializationText.style.visibility = "visible";
        
        // Re-initialize the models to start fresh for each training session
        await mvae.initialize();
        await midime.initialize();
        
        const data = await mvae.encode([quantNoteSeq1]);

        await midime.train(data, async (epoch) => {
            epochsText.innerHTML = `Epoch ${epoch + 1} / 100`;
        });
        
        console.log("Training completed successfully");
        epochsText.innerHTML = "✅ Training Complete! Ready to Sample.";
        isModelReady = true;

    } catch (error) {
        console.error("Error during training:", error);
        epochsText.innerHTML = "❌ Training Failed. Please try again.";
    } finally {
        isTraining = false;
        initializationText.style.visibility = "hidden";
        updateButtonStates();
    }
}

/**
 * Clears the notation display.
 */
const clearNotation = () => {
    notationDiv.innerHTML = ''; // Clear the content of the notation div
};

/**
 * Generates a new musical sample from the trained model.
 */
async function sampleModel() {
    if (!isModelReady) {
        alert("Please train the model on a MIDI file first!");
        return;
    }
    try {
        const temperature = parseFloat(temperatureSlider.value);
        console.log(`Sampling with temperature: ${temperature}`);
        
        const sample = await midime.sample(8);
        const sequences = await mvae.decode(sample, temperature);
        const playableSample = mm.sequences.concatenate([...sequences]);
        
        console.log("Generated notes:", playableSample.notes.map(n => n.pitch));

        if (playableSample.notes.length > 16) {
            playableSample.notes = playableSample.notes.slice(0, 16);
        }
        renderMidi(playableSample);
        
        console.log("Generated new sample successfully");
    } catch (error) {
        console.error("Error generating sample:", error);
        alert("Error generating sample. Make sure you've trained the model.");
    }
}

// Initialize the models when the script loads
async function startProgram() {
    try {
        initializationText.style.visibility = "visible";
        // Initialize VAE once at the start
        await mvae.initialize();
        console.log("Magenta.js models initialized successfully.");
    } catch (error) {
        console.error("Error initializing models:", error);
    } finally {
        initializationText.style.visibility = "hidden";
        updateButtonStates();
    }
}

startProgram();

