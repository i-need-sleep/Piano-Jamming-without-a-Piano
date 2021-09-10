importScripts("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@1.4.0/dist/tf.min.js");
importScripts("https://cdn.jsdelivr.net/npm/@magenta/music@^1.23.0/es6/core.js");
importScripts("https://cdn.jsdelivr.net/npm/@magenta/music@^1.23.0/es6/music_rnn.js");

var improv_rnn = new music_rnn.MusicRNN(
    "https://storage.googleapis.com/magentadata/js/checkpoints/music_rnn/chord_pitches_improv"
  )

improv_rnn.initialize()

self.onmessage = async (e) => {
    let note_seq = e.data.sequence
    let prog = e.data.prog

    improv_rnn
    .continueSequence(note_seq, 16, 1, prog)
    .then((cont_out) => {
      postMessage({cont_out: cont_out})
    })
  };