// Initialize Magenta.js models
const mvae = new mm.MusicVAE(
  "https://storage.googleapis.com/magentadata/js/checkpoints/music_vae/mel_4bar_med_lokl_q2",
);
const midime = new mm.MidiMe({ epochs: 100 });

// Global variables
let noteSeq1 = null;
let quantNoteSeq1 = null;
let isTraining = false;
let isModelReady = false;

// DOM elements
const uploadButton = document.getElementById("uploadButton");
const trainButton = document.getElementById("trainButton");
const sampleButton = document.getElementById("sample");
const octaveSelector = document.getElementById("octaveSelector");
const temperatureSlider = document.getElementById("temperatureSlider");
const tempValueSpan = document.getElementById("tempValue");
const positionSelector = document.getElementById("positionSelector");
const initializationText = document.getElementById("initialization");
const epochsText = document.getElementById("epochsText");
const notationDiv = document.getElementById("notation");
const fileInput = document.getElementById("input");

// Event Listeners
uploadButton.addEventListener("click", upload);
trainButton.addEventListener("click", train);
sampleButton.addEventListener("click", sampleModel);
temperatureSlider.addEventListener("input", () => {
  tempValueSpan.textContent = temperatureSlider.value;
});

const TUNINGS = {
  standard: [64, 59, 55, 50, 45, 40], // EADGBe
};

const FRET_COUNT = 19;

// Classical guitar position definitions
const POSITIONS = {
  1: { name: "I", fretRange: [0, 4], baseFret: 1 },
  2: { name: "II", fretRange: [2, 5], baseFret: 2 },
  3: { name: "III", fretRange: [5, 8], baseFret: 5 },
  4: { name: "IV", fretRange: [7, 10], baseFret: 7 },
  5: { name: "V", fretRange: [9, 12], baseFret: 9 },
};

/**
 * Returns all possible fret/string combinations for a given MIDI note.
 * @param {number} midi - The MIDI note number.
 * @param {Array<number>} tuning - The tuning of the guitar.
 * @returns {Array<{string: number, fret: number, finger: number}>}
 */
function noteToFret(midi, tuning = TUNINGS.standard) {
  const locations = [];
  for (let i = 0; i < tuning.length; i++) {
    const fret = midi - tuning[i];
    if (fret >= 0 && fret <= FRET_COUNT) {
      locations.push({
        string: i + 1,
        fret: fret,
        finger: 0, // Will be calculated based on position
      });
    }
  }
  return locations;
}

/**
 * Enhanced algorithm that selects the best fret/string location based on position and ergonomics.
 * @param {Array<{string: number, fret: number}>} locations - Possible locations for a note.
 * @param {number} position - The desired position (1-5, or 0 for automatic).
 * @param {Object} previousNote - Previous note info for context.
 * @returns {{string: number, fret: number, finger: number, position: number}|null}
 */
function getBestLocation(locations, position, previousNote = null) {
  if (locations.length === 0) return null;

  // If automatic, find the best overall position
  if (position === 0) {
    return getBestAutomaticLocation(locations, previousNote);
  }

  const positionInfo = POSITIONS[position];
  if (!positionInfo) return null;

  const [minFret, maxFret] = positionInfo.fretRange;
  const baseFret = positionInfo.baseFret;

  // Filter locations that fit within the position
  const validLocations = locations.filter((loc) => {
    if (loc.fret === 0) return position === 1; // Open strings only in position I
    return loc.fret >= minFret && loc.fret <= maxFret;
  });

  if (validLocations.length === 0) {
    // Fallback: find closest available location
    return locations.reduce((best, current) => {
      const currentDistance = Math.abs(current.fret - baseFret);
      const bestDistance = best ? Math.abs(best.fret - baseFret) : Infinity;
      return currentDistance < bestDistance ? current : best;
    }, null);
  }

  // Score each valid location
  let bestLocation = null;
  let bestScore = Infinity;

  for (const loc of validLocations) {
    let score = 0;

    // Calculate finger assignment
    const finger = loc.fret === 0 ? 0 : Math.max(1, loc.fret - baseFret + 1);

    // Prefer reasonable finger assignments (1-4)
    if (finger > 4) score += 10;

    // Prefer middle strings for melody
    if (loc.string === 3 || loc.string === 4) score -= 2;

    // Consider previous note context for smooth voice leading
    if (previousNote) {
      const fretDistance = Math.abs(loc.fret - previousNote.fret);
      const stringDistance = Math.abs(loc.string - previousNote.string);

      // Penalize large jumps
      score += fretDistance * 0.5;
      score += stringDistance * 1.5;

      // Reward staying in same position
      if (Math.abs(loc.fret - previousNote.fret) <= 4) score -= 3;
    }

    // Prefer locations closer to the position center
    const positionCenter = (minFret + maxFret) / 2;
    score += Math.abs(loc.fret - positionCenter) * 0.3;

    if (score < bestScore) {
      bestScore = score;
      bestLocation = {
        ...loc,
        finger: finger,
        position: position,
      };
    }
  }

  return bestLocation;
}

/**
 * Automatic position selection - finds the best overall position for a note.
 */
function getBestAutomaticLocation(locations, previousNote = null) {
  let bestLocation = null;
  let bestScore = Infinity;

  for (const loc of locations) {
    let score = 0;

    // Prefer lower positions for easier playing
    if (loc.fret <= 5) score -= 2;
    else if (loc.fret <= 9) score += 1;
    else score += 3;

    // Prefer middle strings
    if (loc.string >= 2 && loc.string <= 5) score -= 1;

    // Avoid very high frets unless necessary
    if (loc.fret > 12) score += 5;

    // Consider previous note context
    if (previousNote) {
      const distance =
        Math.abs(loc.fret - previousNote.fret) +
        Math.abs(loc.string - previousNote.string);
      score += distance * 0.5;
    }

    if (score < bestScore) {
      bestScore = score;
      bestLocation = {
        ...loc,
        finger:
          loc.fret === 0 ? 0 : Math.min(4, Math.max(1, (loc.fret % 4) + 1)),
        position: determinePosition(loc.fret),
      };
    }
  }

  return bestLocation;
}

/**
 * Determines which position a fret belongs to.
 */
function determinePosition(fret) {
  if (fret <= 4) return 1;
  if (fret <= 6) return 2;
  if (fret <= 8) return 3;
  if (fret <= 10) return 4;
  return 5;
}

/**
 * Updates the UI and button states based on the application's current state.
 */
function updateButtonStates() {
  if (isTraining) {
    trainButton.disabled = true;
    sampleButton.disabled = true;
    uploadButton.disabled = true;
    trainButton.textContent = "🧠 Training...";
  } else {
    trainButton.disabled = false;
    uploadButton.disabled = false;
    trainButton.textContent = "🧠 Train with File";
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
 * Uses VexFlow to render the notes as sheet music with position indicators.
 * @param {Array<mm.NoteSequence.Note>} notes - An array of notes to render.
 */
const vexFlowRendering = (notes) => {
  clearNotation();

  const selectedPosition = parseInt(positionSelector.value, 10);

  // Convert notes to VexFlow format with enhanced positional information
  let previousNote = null;
  const formattedNotes = notes.map((note, index) => {
    const locations = noteToFret(note.pitch);
    const bestLocation = getBestLocation(
      locations,
      selectedPosition,
      previousNote,
    );

    // Update previous note for context
    if (bestLocation) {
      previousNote = bestLocation;
    }

    // Create the basic note string for VexFlow
    const vexNote = `${makeVex(note.pitch)}/q`;

    // Store comprehensive location info
    return {
      vexNote: vexNote,
      location: bestLocation,
      originalPitch: note.pitch,
      noteIndex: index,
    };
  });

  // Use VexFlow to render
  const vf = new Vex.Flow.Factory({
    renderer: { elementId: "notation", width: 1000, height: 600 },
  });
  const score = vf.EasyScore();
  let yOffset = 10;

  // Create note groups
  let noteGroups = [];
  const notesPerGroup = 4;
  for (let i = 0; i < formattedNotes.length; i += notesPerGroup) {
    const group = formattedNotes.slice(i, i + notesPerGroup);
    const groupString = group.map((n) => n.vexNote).join(", ");
    noteGroups.push({
      notes: groupString,
      locations: group.map((n) => n.location),
      isFirstGroup: i === 0,
    });
  }

  noteGroups.forEach((group, groupIndex) => {
    // Create a new system for each group of notes
    const system = vf.System({
      x: 10,
      y: yOffset,
      width: 950,
      spaceBetweenStaves: 10,
    });

    // Add position indicator on the first group if a specific position is selected
    let staveOptions = {
      voices: [score.voice(score.notes(group.notes, { stem: "up" }))],
    };

    const stave = system
      .addStave(staveOptions)
      .addClef("treble")
      .addTimeSignature("4/4");

    // Add Roman numeral position indicator
    if (group.isFirstGroup && selectedPosition > 0) {
      const positionName = POSITIONS[selectedPosition]?.name;
      if (positionName) {
        // Add position marking above the staff
        const context = vf.getContext();
        context.save();
        context.setFont("Arial", 14, "bold");
        context.fillText(`Pos. ${positionName}`, 15, yOffset - 10);
        context.restore();
      }
    }

    yOffset += 120;
  });

  vf.draw();

  // Log position analysis for debugging
  if (selectedPosition > 0) {
    const positionName = POSITIONS[selectedPosition]?.name || selectedPosition;
    console.log(`🎸 Rendered in Position ${positionName}`);

    // Show fingering analysis
    const uniquePositions = new Set();
    formattedNotes.forEach((note) => {
      if (note.location) {
        uniquePositions.add(note.location.position || "auto");
        console.log(
          `Note ${note.originalPitch}: String ${note.location.string}, Fret ${note.location.fret}, Finger ${note.location.finger}`,
        );
      }
    });

    console.log(`Positions used: ${Array.from(uniquePositions).join(", ")}`);
  }
};

// Map of MIDI pitch values to note names
const noteMap = new Map([
  [0, "C"],
  [1, "C#"],
  [2, "D"],
  [3, "D#"],
  [4, "E"],
  [5, "F"],
  [6, "F#"],
  [7, "G"],
  [8, "G#"],
  [9, "A"],
  [10, "A#"],
  [11, "B"],
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
  notationDiv.innerHTML = ""; // Clear the content of the notation div
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

    console.log(
      "Generated notes:",
      playableSample.notes.map((n) => n.pitch),
    );

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
