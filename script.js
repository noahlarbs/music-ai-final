// Music and AI, 2023
// Dartmouth College
// CS 89/189 MUS14, Prof. Michael Casey
//edited by noahlarbalestier, student of Prof. Michael Casey, Dartmouth College. May 2024


// Each bundle exports a global object with the name of the bundle, e.g.:
// music_vae - VAE bundle, defined by magenta, e.g.: new music_vae.MusicVAE(checkpoint)
//      core - Magenta core functions, e.g.: core.Player()

//checkpoint = 'https://storage.googleapis.com/download.magenta.tensorflow.org/'
//model = 'tfjs_checkpoints/music_vae/trio_4bar_lokl_small_q1'
//Using model/checkpoints found online from: https://github.com/magenta/magenta-js/blob/master/music/checkpoints/README.md
//Using the Trio was not the best way to go about it, these models just made it sound so bad.
//my first iteration is just messing around wiht different checkpoints. I have an absolute mess in my garage band right now,
//but this was really cool to experiment with. 
const mvae = new music_vae.MusicVAE('https://storage.googleapis.com/magentadata/js/checkpoints/music_vae/mel_16bar_small_q2');

// output quantized inotelist to midi
function sampleMVAE(temp=1.0) {
    mvae.sample(1, temp).then(
        (samps) => {
            console.log(samps[0].notes);
            playNoteListMIDI(samps[0].notes);
        }) 
}

// function to influence music generation with a given notesequence
function influenceSample(inputSequence) {
    mvae.encode([inputSequence]).then((latentVector) => {
        mvae.decode(latentVector, 0.1 /* temperature */).then((decoded) => {
            console.log(decoded[0].notes);
            playNoteListMIDI(decoded[0].notes);
        });
    });
}
// make a function call that plays something, then encodes and decodes that very sequence again... i.ie. in playnotelist midi
//store notes as played in proper format and encode/decode/play again
// load and influence using a midi file input
function loadAndInfluence() {
    
    const fileInput = document.getElementById('midiFileInput');
    const file = fileInput.files[0];
    if (file) {
        
        const reader = new FileReader();
        reader.onload = function(e) {
            const midiArray = new Uint8Array(e.target.result);
            core.midiToSequenceProto(midiArray).then((sequence) => {
            //using this alert to see if playNoteListMidi is called, which it is. I guess this means I am having a problem either taking in the file or processing midi?
            //alert showing pobject Object, I wish I could debug this I just don't know how sadly
                alert('called')
                influenceSample(sequence);
            });
        };
        reader.readAsArrayBuffer(file);
    } else {
        alert('Please select a MIDI file.');
    }
}

// initializes the musicvae model
async function startProgram() {
    await mvae.initialize()
}

startProgram(); // initializes the model and waits for user interaction

