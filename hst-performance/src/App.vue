<template>
<div>

<!-- Nav Bar -->
<nav class="navbar navbar-expand-sm bg-light navbar-hover">
  <div class="collapse navbar-collapse">
    <ul class="navbar-nav mr-auto">   
          <li class="nav-item dropdown">
              <button class="dropdown-toggle btn" id="browse_samples" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  Browse Samples
              </button>
              <ul class="dropdown-menu">
                <li id="resample" v-on:click="get_data">Random Phrase</li>
                  <li v-for="song in Object.keys(this.songData)" v-bind:key="song">
                    <a class="dropdown-item dropdown-toggle">Song {{song}} {{this.songData[song]['key']}}</a>
                      <ul class="dropdown-menu">
                        <div v-for="segment in Object.keys(this.songData[song])" v-bind:key="segment">
                          <div v-if="segment != 'key'">
                            <li v-on:click="get_data"><a class="dropdown-item phraseSelect" 
                              v-bind:data-song="song"
                              v-bind:data-segment="segment">
                              Segment {{segment}} {{this.songData[song][segment]}}</a></li>
                          </div>
                        </div>
                      </ul>
                  </li>
              </ul>
          </li>
      </ul>
    <ul class="navbar-nav">
      <li class="nav-item">
        <button class="btn" disabled>Phrase ID: {{this.songID.slice(0,3)}}: {{this.songname}} {{this.songID.slice(4)}} | {{this.songkey}}</button><br> 
        <!-- <button class="btn" v-on:click="test">test</button><br>  -->
      </li>
      <li class="nav-item">
        <a tabindex="0" class="btn" role="button" data-toggle="popover" data-trigger="focus" title="Help" rel="popover"
        data-content="
        Playback: <br> 
        <ul>
          <li>r: reset</li>
          <li>n: new sample</li>
        </ul>
        Input-Fixed: <br> 
        <ul>
          <li>Mouse</li>
          <ul>
            <li>left click: select a major triad</li>
            <li>right click: select a minor triad</li>
            <li>middle click or (shift + left click): select a dominant 7th chord</li>
            <li>alt + left/right click: select a major/minor 7th chord</li>
          </ul>
          <li>Keyboard</li>
          <ul>
            <li>'1'-'=': select root</li>
            <li>shift + root: major triad</li>
            <li>ctrl + root: minor triad</li>
            <li>alt + root: moninant 7th chord</li>
            <li>alt+ shift/ctrl + root: major/minor 7th chord</li>
          </ul>
        </ul>
        Input-Movable: <br> 
        <ul>
          <li>Mouse</li>
          <ul>
            <li>left click: select a triad corresponding the the scale degree</li>
            <li>shift + left click: select a major triad</li>
            <li>ctrl + left click: select a minor triad</li>
            <li>alt + left click: select a dominant seventh chord</li>
            <li>alt + shift/ctrl + left click: select a major/minor seventh chord</li>
          </ul>
          <li>Keyboard</li>
          <ul>
            <li>1-7: select a triad corresponding the the scale degree</li>
            <li>shift + 1-7: select a major triad</li>
            <li>ctrl + 1-7: select a minor triad</li>
            <li>alt + 1-7: select a dominant seventh chord</li>
            <li>alt + shift/ctrl + 1-7: select a major/minor seventh chord</li>
          </ul>
        </ul>
        "  data-html="true">
          Help
        </a><br>
      </li>
    </ul>
  </div>
</nav>


<div class="container-fluid pt-3 pb-5" id="main_app">
  <!-- Original -->
  <!-- Time steps: Original -->
  <table id=time_steps class="table table-fixed prog_table">
    <thead class="thead-light">
    <tr>
      <th class="prog_head table_cell"></th>
      <div>
        <th class="time_cell" v-for="i in 16" v-bind:key="i" v-bind:id="'time'+(i-1)"> {{ (i+3-(i-1)%4)/4 + "." + ((i-1)%4+1)}} </th>
        <th class="time_cell"></th><th class="time_cell"></th>
      </div>
    </tr>
    </thead>
  </table> 

  <midi-visualizer type="piano-roll" class="right" id="original_vis" v-bind:noteSequence="this.original_noteseq" v-bind:config="this.cfg"></midi-visualizer>
  <div class="up">
  <midi-visualizer type="piano-roll" class="right" id="original_vis_overlay" v-bind:noteSequence="this.original_noteseq_overlay" v-bind:config="this.cfg_mel"></midi-visualizer>
  <svg class="original_svg svg right" height="0px"></svg>
  
  
  <div class="up">

  <!-- Original Progression -->
  <table id="original_prog" class="table table-fixed table-striped prog_table">
    <tbody>
    <tr>
        <th id=play_prog_original class="prog_head" v-on:click="play_prog_original">Original</th>
        <div>
        <td v-for="i in 16" v-bind:key="i" v-bind:id="'original_prog'+(i-1)" class="table_cell" style="font-weight:normal;" v-on:click="play_chord('original', i-1)" > {{ original_chd_str[i-1] }} </td>
        <th></th><th></th>
        </div>
    </tr>
    </tbody>  
  </table>

  <!-- Altered -->
  <!-- Time steps -->
  <table id=altered_time_steps class="table table-fixed prog_table">
    <thead class="thead-light">
    <tr>
        <div>
          <th class = "prog_head table_cell"></th>
          <th class="time_cell" v-for="i in 16" v-bind:key="i" v-bind:id="'time_altered'+(i-1)"> {{ (i+3-(i-1)%4)/4 + "." + ((i-1)%4+1)}} </th>
          <th class="time_cell"></th><th class="time_cell"></th>
        </div>
    </tr>
    </thead>
  </table> 

  <canvas id="altered_canvas" class="right"></canvas>
  <svg class="swapped_svg svg right" id="swapped_svg" height="0px"></svg>
  <div class="up">
  <div class="up">
  <midi-visualizer type="piano-roll" class="right" id="altered_altered_overlay" v-bind:noteSequence="this.altered_noteseq_overlay" v-bind:config="this.cfg_mel"></midi-visualizer>
  <svg class="original_svg svg right" height="0px"></svg>

  <div class="up">
  <!-- Altered Progression -->
  <table id=saved_prog class="table table-fixed table-striped prog_table">
    <tbody>
      <tr>
        <div>
        <th id=play_prog_original class="prog_head" v-on:click="play_prog_altered">Altered</th>
        <td v-for="i in 16" v-bind:key="i" v-bind:id="'altered'+(i-1)" class="table_cell" style="font-weight:normal;" v-on:click="play_chord('altered',i-1)">{{altered_chd_str[i-1]}}</td>
        </div>
        <th></th>
    </tr>
    </tbody>
  </table> 

  <!-- Interfacing -->
  <div class="row">
    <div class="col-4">
    <button id="altered_reset" class="btn btn-light" v-on:click="player_reset">Reset</button><br>
    Bpm: <span id=bpm_text>{{this.bpm}}</span><div id=slider_container><input type="range" class="form-control-range" id=bpm_slider min=30 max=200 v-model="bpm"></div>
    <div class="input-group-prepend">
    <div class="input-group-text" style="width:160px">
      <input type="checkbox" id="root_overlay" v-bind:checked="root_overlay" v-on:click="this.root_on_click()"> <span> &nbsp; Root overlay</span>
    </div>
    </div>
    <div class="input-group-prepend">
      <div class="input-group-text" style="width:160px">
        <input type="checkbox" id="chord_overlay" v-bind:checked="chord_overlay" v-on:click="this.chord_on_click()"> <span> &nbsp; Chord overlay</span>
      </div>
    </div>
  </div>

  <div class="col-3">
    <div class="btn-group">
      <button class="btn btn-light dropdown-toggle" type="button" data-toggle="dropdown">{{"Input type: "+this.input_type}}
      <span class="caret"></span></button>
      <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#" v-on:click="change_input_type('movable')">Movable</a></li>
        <li><a class="dropdown-item" href="#" v-on:click="change_input_type('fixed')">Fixed</a></li>
      </ul>

    <div class="dropdown" v-if="this.input_type == 'movable'">
      <button class="btn btn-light dropdown-toggle" type="button" data-toggle="dropdown">{{"Key: "+this.key+" major"}}
      <span class="caret"></span></button>
      <ul class="dropdown-menu">
        <li><a v-for="key in this.scales_major" 
        v-bind:key="key" class="dropdown-item" href="#" v-on:click="change_key(key)">{{key + " major"}}</a></li>
      </ul>
    </div>
    </div>

    <!-- Interface UIs -->  
    <div v-if="this.loaded">
    <InterfaceFixed v-if="input_type == 'fixed'" v-on:update_current_chord="update_current_chord"/>
    <InterfaceMovable ref="dial" v-if="input_type == 'movable'" v-bind:interface_key="this.key" v-bind:roots="scales_major" v-on:update_current_chord="update_current_chord"/>
    </div>

  </div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>

<!-- Barlines -->
<svg id=original_barline class="barline_svg"></svg><br>
<svg id=altered_barline class="barline_svg"></svg>

<!-- Player -->
<midi-player v-bind:noteSequence="this.original_noteseq" sound-font visualizer="#original_vis" id="original_player"></midi-player>

<!-- Mel/Acc Toggle -->
<div id="melacc_toggle">
<div class="input-group-prepend">
  <div class="input-group-text" style="width:160px">
    <input type="checkbox" id="root_overlay" v-bind:checked="mel" v-on:click="this.mel_on_click()"> <span> &nbsp; Melody</span>
  </div>
</div>
<div class="input-group-prepend">
  <div class="input-group-text" style="width:160px">
    <input type="checkbox" id="chord_overlay" v-bind:checked="acc" v-on:click="this.acc_on_click()"> <span> &nbsp; Accompaniment</span>
  </div>
</div>
</div>

</div>
</template>

<script>
import InterfaceFixed from './components/InterfaceFixed.vue'
import InterfaceMovable from './components/InterfaceMovable.vue'
const axios = require('axios').default
const d3 = require("d3")
const mm = require("@magenta/music")
const _ = require("html-midi-player")
console.log(_)
var player = new mm.SoundFontPlayer('https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus')
var rnn_worker = new Worker('rnn_worker.js')

export default {
  name: 'App',
  components: {
    InterfaceFixed,
    InterfaceMovable
  },
  data: function(){
    return{
      // Constants (not really)
      BACKEND_PATH: "http://127.0.0.1:5000", //""
      STEP_SIZE: 4,
      scales_major: ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'],
      // Chord playback
      prog_step_duration: 0.5,
      octave_center: 48,
      // Velocities
      acc_velocity: 55,
      mel_velocity: 100,

      // Song data (original)
      songID: "000",
      songname: '',
      songkey: '',
      songData: {},

      original_noteseq: 0,
      original_noteseq_mixed: 0,
      original_noteseq_mel: 0,
      original_noteseq_acc: 0,
      original_noteseq_overlay: {notes:[{pitch:30, start:0, end:16}], totalTime: 16},
      empty_noteseq: {notes:[{pitch:30, start:0, end:16}], totalTime: 16},

      original_chd_str: 0,
      original_chd_mat: 0,

      notedic: 0,
      notedic_mixed: 0,
      notedic_mel: 0,
      notedic_acc: 0,

      sustain: [],

      // Song data (altered)
      altered_noteseq: {notes:[], totalTime: 16},
      altered_chd_str: Array(16).fill(""),
      altered_chd_mat: Array(16).fill(Array(36).fill(0)),

      // Interfacing (outside)
      bpm: 60,
      playing: false,
      loaded: false,
      input_type: "fixed",
      key: "C",
      
      mel: false,
      acc: true,

      // Interfacing (inside)
      t: 0,
      chord_seq: [], // Entered chords for the current window
      current_chd: '', // Queued chord for the next time step
      current_chd_text: '',

      // Altered visualiser
      altered_vis: 0,

      // Visualiser config
      cfg: {
        noteHeight: 4,
        pixelsPerTimeStep: 100,
        minPitch: 20,
        maxPitch: 90,
        noteSpacing: 1
      },
      cfg_mel: {
        noteHeight: 4,
        pixelsPerTimeStep: 100,
        minPitch: 20,
        maxPitch: 90,
        noteSpacing: 1,
        noteRGB: "255,0,0"
      },

      // Overlays
      root_overlay: true,
      chord_overlay: false,

      // Improv RNN
      mel_seq:{
        notes: [],
        quantizationInfo: {stepsPerQuarter: 4},
        tempos: [{time: 0, qpm: 60}],
        totalQuantizedSteps: 64
      },
      cur_mel_seq:{
        notes: [],
        quantizationInfo: {stepsPerQuarter: 4},
        tempos: [{time: 0, qpm: 60}],
        totalQuantizedSteps: 16
      },
      rnn_prog: [],
      altered_noteseq_overlay: {notes:[{pitch:50, start:0, end:16}], totalTime: 16},
    }
  },
  computed: {
  },
  methods: {
    // Helpers
    list_to_noteseq(notes_in, filter_start=0, filter_end=16){
      let notes_out = []
      for (let i=0; i<notes_in.length; i++){
          let start = notes_in[i][0]
          let end = notes_in[i][1]
          let pit = notes_in[i][2]
          let velo = notes_in[i][3]
          if (filter_start >= 8){
              start += 8
              end += 8
          }
              if (start>=filter_start && start<filter_end){
                  notes_out.push({pitch:pit, startTime:start, endTime:end, velocity:velo})
              }
      }
      return notes_out
    },

    chords_to_noteseq(chords, relative=true){ 
      
      let mod_chords = []
      for (let i=0; i<chords.length; i++){
        let chord = chords[i]
        let chroma = []
        for (let j=0; j<12; j++){
          if (chord[12+j] == 1){
            chroma.push(j)
          }
        }
        if (chord.slice(0,13).indexOf(1) == -1){
          break
        }
        if (relative){
          mod_chords.push([chord.slice(0,13).indexOf(1),chroma,0])
        }
        else{
          mod_chords.push([chord.slice(0,13).indexOf(1),chroma,chord.slice(24,36).indexOf(1)])
        }
      }
      chords = mod_chords
      

      let prog_notes = [];

      if (chords.length > 0){
        let cur_chord = chords[0];
        let cur_dur = this.prog_step_duration;
        
        for (let i=1; i<chords.length; i++){
            if (JSON.stringify(chords[i])==JSON.stringify(cur_chord)){
                cur_dur += this.prog_step_duration;
            }
            else {
                let root = parseInt(cur_chord[0]);
                let chroma = cur_chord[1];
                let bass = parseInt(cur_chord[2]);
                for (let j=0; j<chroma.length; j++){
                  if (relative){
                    prog_notes.push({pitch: parseInt(chroma[j])+root+this.octave_center, startTime: this.prog_step_duration*i-cur_dur, endTime: this.prog_step_duration*i});
                  }
                  else{
                    prog_notes.push({pitch: parseInt(chroma[j])+this.octave_center, startTime: this.prog_step_duration*i-cur_dur, endTime: this.prog_step_duration*i});
                  }
                }
                prog_notes.push({pitch:bass+root+this.octave_center-12, startTime: this.prog_step_duration*i-cur_dur, endTime: this.prog_step_duration*i});
                cur_chord = chords[i];
                cur_dur = this.prog_step_duration;
            }
        }
        let root = parseInt(cur_chord[0]);
        let chroma = cur_chord[1];
        let bass = parseInt(cur_chord[2]);
        for (let j=0; j<chroma.length; j++){
          if (relative){
            prog_notes.push({pitch: parseInt(chroma[j])+root+this.octave_center, startTime: this.prog_step_duration*chords.length-cur_dur, endTime: this.prog_step_duration*chords.length});
          }
          else{
            prog_notes.push({pitch: parseInt(chroma[j])+this.octave_center, startTime: this.prog_step_duration*chords.length-cur_dur, endTime: this.prog_step_duration*chords.length});
          }
        }
        prog_notes.push({pitch:bass+root+this.octave_center-12, startTime: this.prog_step_duration*chords.length-cur_dur, endTime: this.prog_step_duration*chords.length});

        return {notes: prog_notes, totalTime: this.prog_step_duration*chords.length};
      }
    },

    // Fetch data from the backend
    get_songdata(){
      axios.get(this.BACKEND_PATH + '/get_songdata')
        .then(response => {
              let data = response.data
              if (! data.songData){
                data = JSON.parse(response.data)
              }
              this.songData = data.songData
        })
    },
    
    get_data(id="000", reset=true){
      if(typeof(id) != "string"){
        if (id.target.dataset.song != undefined){
          id = id.target.dataset.song.slice(0,3) + "_" + id.target.dataset.segment
        }
        else{
          id = "000"
        }
      }
      axios.get(this.BACKEND_PATH + '/get_data?song=' + id)
        .then(response => {
              let data = response.data
              if (! data.songID){
                data = JSON.parse(response.data)
              }
              this.songID = data.songID
              this.original_noteseq_mixed = data.original_noteseq_mixed
              this.original_noteseq_mel = data.original_noteseq_mel
              this.original_noteseq_acc = data.original_noteseq_acc
              this.original_chd_str = data.original_chd_str
              this.original_chd_mat = data.original_chd_mat
              this.notedic_mixed = data.notedic_mixed
              this.notedic_mel = data.notedic_mel
              this.notedic_acc = data.notedic_acc
              this.sustain = data.sustain
              this.songname = data.name
              this.songkey = data.key

              this.update_melacc_toggle()
              // Modify the sustain status to include the onset of every measure
              for (let bar=1; bar<4; bar++){
                for (let i=0; i<this.sustain.length; i++){
                  let start = this.sustain[i][0]
                  let end = this.sustain[i][1]
                  if (start < bar*4 && end > bar*4){
                    break
                  }
                  if (start > bar*4){
                    if (i > 0){
                      this.sustain[i-1][1] = bar*4 + 1
                    }
                    else{
                    this.sustain.push([bar*4 - 1, bar*4 + 1])
                    }
                    break
                  }
                }
              }

              // Fetch a placeholder notesequence
              // this.altered_vis = new mm.PianoRollCanvasVisualizer({notes: this.list_to_noteseq(this.notedic[0]["0M3,0M3"]), totalTime:16}, document.getElementById('altered_canvas'), this.cfg)
              if (reset){
                this.altered_vis = new mm.PianoRollCanvasVisualizer({notes: [{pitch: 30, start:0, end:8}], totalTime:16}, document.getElementById('altered_canvas'), this.cfg)
                this.update_overlay()

                this.player_reset()
                this.place_barlines_and_player()
              }
              
              setTimeout(() => {  this.place_barlines_and_player(); }, 1000)
              setTimeout(() => {  this.place_barlines_and_player(); }, 3000)
        })
    },

    // Interfacing (player)
    player_play(){
      
      if (this.loaded){
        if (this.playing){
          if (this.t % this.STEP_SIZE == 0){
            // Reset at t = 0
            if (this.t == 0){
              this.altered_noteseq.notes = []
            }
            this.player_query_step()
          }
          if (!this.playing){
            return
          }

          // Next time step
          this.t += 4;
          if (this.t == 16){
              this.t = 0
          }
        }
      }
      
    },

    player_reset(){
      this.playing = false
      this.t = 0
      this.altered_noteseq.notes = []
      this.chord_seq = []
      this.altered_chd_str = Array(16).fill("")
      this.altered_chd_mat =  Array(16).fill(Array(36).fill(0))
      this.altered_vis.redraw()
      this.update_overlay()
    },

    player_query_step(){
      if (this.current_chd == ''){
        this.playing = false
        return
      }
      
      setTimeout(() => {  this.player_play(); }, 16*250*60/this.bpm)
      // Update cell highlighting
      for (let i=this.t; i<this.t+4; i++){
        this.highlight_cell("altered"+i, 16*250*60/this.bpm/1000)
      }
      const high_light_step = (time) => {
        this.highlight_cell("time_altered"+time, 4*250*60/this.bpm/1000)
        if (time % 4 == 3){
          return
        }
        setTimeout(() => {
          high_light_step(time+1)
        }, 4*250*60/this.bpm);
      }
      high_light_step(this.t)

      // Clean up at song start
      if (this.t == 0){
        this.altered_chd_str = Array(16).fill("")
        this.altered_chd_mat =  Array(16).fill(Array(36).fill(0))
      }

      // Clean up at window start
      if (this.t % this.STEP_SIZE == 0){
        this.chord_seq = []
      }

      this.chord_seq.push(this.current_chd)
      let root = parseInt(this.current_chd.slice(0,-2))
      let chroma = this.current_chd.slice(-2)
      this.current_chd = ''

      // Update string
      this.altered_chd_str[this.t] = this.current_chd_text
      this.current_chd_text = ''
      
      // Query and update noteseq
      let chord_seq_maxlen = 8 / this.STEP_SIZE
      let query = []
      for (let i=0; i<this.chord_seq.length; i++){
        query.push(this.chord_seq[i])
      }
      while (query.length < chord_seq_maxlen){
        query.push(query[query.length-1])
      }
      query = query.join(',')
      let note_list = this.notedic[(this.t - this.t%8)/8][query]
      let new_notes = this.list_to_noteseq(note_list, this.t, this.t+this.STEP_SIZE, true)
      this.altered_noteseq.notes = this.altered_noteseq.notes.concat(new_notes)  
      let quant_note_seq = this.notes_to_quant_noteseq(new_notes)

      // Add the improvised melody
      let t = this.t
      // update the melody noteseq
      let new_mel_notes = []
      this.altered_noteseq_overlay.notes = []
      for (let i=0; i<this.mel_seq.notes.length; i++){
        this.mel_seq.notes[i].quantizedStartStep -= 64
        this.mel_seq.notes[i].quantizedEndStep -= 64
        if (this.mel_seq.notes[i].quantizedStartStep > 0){
          new_mel_notes.push(this.mel_seq.notes[i])
        } 
      }
      
      for (let i=0; i<this.cur_mel_seq.notes.length; i++){
        quant_note_seq.notes.push({
          pitch: this.cur_mel_seq.notes[i].pitch, 
          quantizedStartStep: this.cur_mel_seq.notes[i].quantizedStartStep, 
          quantizedEndStep: this.cur_mel_seq.notes[i].quantizedEndStep,
          velocity: this.mel_velocity  
        })
      
        this.altered_noteseq.notes.push({
          pitch: this.cur_mel_seq.notes[i].pitch, 
          startTime: this.cur_mel_seq.notes[i].quantizedStartStep/4 + t, 
          endTime: this.cur_mel_seq.notes[i].quantizedEndStep/4+t,
          velocity: this.mel_velocity  
        })

        this.cur_mel_seq.notes[i].quantizedStartStep += 64 * 3
        this.cur_mel_seq.notes[i].quantizedEndStep += 64 * 3
        new_mel_notes.push(this.cur_mel_seq.notes[i])
      }
      this.mel_seq.notes = new_mel_notes

      for (let i=0; i<this.altered_noteseq.notes.length; i++){
        let note = this.altered_noteseq.notes[i]
        if (note.velocity == this.mel_velocity){
          this.altered_noteseq_overlay.notes.push(note)
        }
      }
      console.log(this.altered_noteseq_overlay)
      console.log(this.original_noteseq_overlay)
      this.altered_noteseq_overlay = this.mel_seq

      // Restart the player
      if (player.isPlaying()){
        player.stop()
      }
      player.start(quant_note_seq, this.bpm)


      // Canvas and noteseq
      this.altered_vis.noteSequence = this.altered_noteseq
      this.altered_vis.redraw()

      // Overlay and notemat
      let new_chd_mat = Array(36).fill(0)
      new_chd_mat[root] = 1
      new_chd_mat[24] = 1

      let M3 = [0,4,7]
      let m3 = [0,3,7]
      let M7 = [0,4,7,11]
      let m7 = [0,3,7,10]
      let D7 = [0,4,7,10]
      let chm = 0

      if (chroma == 'M3'){
        chm = M3
      }
      if (chroma == 'm3'){
        chm = m3
      }
      if (chroma == 'M7'){
        chm = M7
      }
      if (chroma == 'm7'){
        chm = m7
      }
      if (chroma == 'D7'){
        chm = D7
      }

      for (let i=0; i<chm.length; i++){
        new_chd_mat[(root+chm[i])%12 + 12] = 1
      }
      for (let i=t; i<t+this.STEP_SIZE; i++)[
        this.altered_chd_mat[i] = new_chd_mat
      ]
      this.update_overlay()
    },

    notes_to_quant_noteseq(notes){
      let out = {notes: [], quantizationInfo: {stepsPerQuarter: 4}, tempos: [{time: 0, qpm: 60}],totalQuantizedSteps: 64}
      for (let i=0; i<notes.length; i++){
        let note = notes[i]
        let note_start = note.startTime
        let note_end = note.endTime
        for (let j=0; j<this.sustain.length; j++){
          let sus_start = this.sustain[j][0]
          let sus_end = this.sustain[j][1]
          if (note.endTime > sus_start && note.endTime < sus_end){
            note_end = sus_end
            break
          }
          if (note.endTime < sus_start){
            break
          }
        }
        out.notes.push({pitch:note.pitch, quantizedStartStep:(note_start-this.t)*4, quantizedEndStep:Math.round((note_end-this.t)*4), velocity: this.acc_velocity})
      }
      return out
    },

    canvas_update_note(note){
      let t = this.t
      if (t == 0){
        t = 16
      }
      let canvas_note = {pitch: note.pitch, startTime: note.startTime+t-4, endTime: note.endTime+t-4}
      this.altered_vis.redraw(canvas_note)
    },

    // Interfacing (input type)
    change_input_type(type){
      this.input_type = type
    },
    change_key(key){
      this.key = key
      this.$refs.dial.draw_dial(this.$refs.dial.outer_text(key))
    },
    update_current_chord(chd, text){
      this.current_chd = chd
      this.current_chd_text = text
      if (!this.playing){
        this.playing = true
        this.player_play()
      }
      else{
        // Pre-update overlays and chord texts
        // Overlay and notemat
        let root = parseInt(this.current_chd.slice(0,-2))
        let chroma = this.current_chd.slice(-2)
        let new_chd_mat = Array(36).fill(0)
        let t = this.t
        new_chd_mat[root] = 1
        new_chd_mat[root+24] = 1

        let M3 = [0,4,7]
        let m3 = [0,3,7]
        let M7 = [0,4,7,11]
        let m7 = [0,3,7,10]
        let D7 = [0,4,7,10]
        let chm = 0

        if (chroma == 'M3'){
          chm = M3
        }
        if (chroma == 'm3'){
          chm = m3
        }
        if (chroma == 'M7'){
          chm = M7
        }
        if (chroma == 'm7'){
          chm = m7
        }
        if (chroma == 'D7'){
          chm = D7
        }

        for (let i=0; i<chm.length; i++){
          new_chd_mat[(root+chm[i])%12 + 12] = 1
        }
        for (let i=t; i<t+this.STEP_SIZE; i++)[
          this.altered_chd_mat[i] = new_chd_mat
        ]
        this.update_overlay()

        // Text
        this.altered_chd_str[t] = this.current_chd_text
        }

        // Impovise 
        this.improvise(text)
    },

    // Overlays
    draw_overlay_bar(svg, x, pitch, color){
      x *= 100;
      while (pitch <= 90){
          if (pitch >= 30){
              svg.append('rect')
              .attr('fill', color)
              .attr('opacity', 0.3)
              .attr('x', x)
              .attr('y', this.cfg.noteHeight * (this.cfg.maxPitch - pitch))
              .attr('width', 100)
              .attr('height', 4)
              .attr('class', 'overlay');
          }
          pitch += 12;
      }
    },
    clear_overlay(){
      d3.selectAll(".overlay").remove().exit()
    },
    get_color(pitch){
      return d3.interpolateSinebow((pitch/12+0.6)%1)
    },
    draw_root_overlay(){
      for (let i=0; i<this.original_chd_mat.length; i++){
        let chd = this.original_chd_mat[i];
        let root = chd.slice(0,12).indexOf(1);
        this.draw_overlay_bar(d3.select(".original_svg"), i, root, this.get_color(0));
        if (this.altered_chd_mat[i].slice(0,12).indexOf(1) >= 0){
            this.draw_overlay_bar(d3.select(".swapped_svg"), i, this.altered_chd_mat[i].slice(0,12).indexOf(1), this.get_color(0));
        }
      }
    },
    draw_chord_overlay(){
      for (let i=0; i<this.original_chd_mat.length; i++){
        let chd = this.original_chd_mat[i];
        let root = chd.slice(0,12).indexOf(1);
        for (let j=0; j<12; j++){
          if (chd[12+j] == 1){
              this.draw_overlay_bar(d3.select(".original_svg"), i, j, this.get_color((j-root)%12));
          }
          if (this.altered_chd_mat[i][12+j] == 1){
              this.draw_overlay_bar(d3.select(".swapped_svg"), i, j, this.get_color((j-this.altered_chd_mat[i].slice(0,12).indexOf(1))%12));
          }
        }
      }
    },
    update_overlay(){
      this.clear_overlay()
      if (this.chord_overlay){
        this.draw_chord_overlay()
      }
      else if (this.root_overlay){
        this.draw_root_overlay()
      }
    },
    root_on_click(){
      if (this.root_overlay){
        this.root_overlay = false
      }
      else {
        this.root_overlay = true
      }
      this.update_overlay()
    },
    chord_on_click(){
      if (this.chord_overlay){
        this.chord_overlay = false
      }
      else {
        this.chord_overlay = true
      }
      this.update_overlay()
    },

    // Place barlines / original player
    draw_barlines_original(){
      d3.selectAll(".barline_original").remove().exit()
      let top_rect = document.getElementById("time0").getBoundingClientRect();
      let bottom_rect = document.getElementById("original_prog0").getBoundingClientRect();

      let l1 = top_rect.left + window.pageXOffset || document.documentElement.scrollLeft
      let l2 = top_rect.right + window.pageXOffset || document.documentElement.scrollLeft
      let t = top_rect.top + window.pageYOffset || document.documentElement.scrollTop
      let b = bottom_rect.bottom + window.pageYOffset || document.documentElement.scrollTop

      for (let i=1; i<4; i++){
          d3.selectAll("#original_barline")
          .append('rect')
          .attr('x', l1 + i*4*(l2-l1))
          .attr('y', t)
          .attr('width', 3)
          .attr('height', b-t)
          .attr('class', 'barline barline_original')
      }
    },
    draw_barlines_altered(){
      d3.selectAll(".barline_altered").remove().exit()

      let top_rect = document.getElementById("time_altered0").getBoundingClientRect();
      let bottom_rect = document.getElementById("altered10").getBoundingClientRect();

      let l1 = top_rect.left + window.pageXOffset || document.documentElement.scrollLeft
      let l2 = top_rect.right + window.pageXOffset || document.documentElement.scrollLeft
      let t = top_rect.top + window.pageYOffset || document.documentElement.scrollTop
      let b = bottom_rect.bottom + window.pageYOffset || document.documentElement.scrollTop

      for (let i=1; i<4; i++){
          d3.selectAll("#altered_barline")
          .append('rect')
          .attr('x', l1 + i*4*(l2-l1))
          .attr('y', t)
          .attr('width', 3)
          .attr('height', b-t)
          .attr('class', 'barline barline_altered')
        }
    },
    place_player_original(){
      let top_rect = document.getElementById("time15").getBoundingClientRect();
      let bottom_rect = document.getElementById("original_prog15").getBoundingClientRect();

      let l2 = top_rect.right + window.pageXOffset || document.documentElement.scrollLeft
      let t = top_rect.top + window.pageYOffset || document.documentElement.scrollTop
      let b = bottom_rect.top + window.pageYOffset || document.documentElement.scrollTop

      d3.select("#original_player")
      .style("position","absolute")
      .style("left",l2+"px")
      .style("top", (t+2.5*b)/3.5+"px")
      .style("-webkit-transform","scale(0.75)")
      .raise()
    },
    place_barlines_and_player(){
      this.draw_barlines_original()
      this.draw_barlines_altered()
      this.place_player_original()
      this.place_melacc_toggle()
    },

    // Mel/Acc toggle
    mel_on_click(){
      this.mel = ! this.mel
      if (! this.mel && ! this.acc){
        this.acc = true
      }
      this.update_melacc_toggle()
    },
    acc_on_click(){
      this.acc = ! this.acc
      if (! this.acc && ! this.mel){
        this.mel = true
      }
      this.update_melacc_toggle()
    },
    update_melacc_toggle(){
      if (this.mel && this.acc){
        this.notedic = this.notedic_mixed
        this.original_noteseq = this.original_noteseq_mixed
        this.original_noteseq_overlay = this.original_noteseq_mel
      }
      else if (this.mel){
        this.notedic = this.notedic_mel
        this.original_noteseq = this.original_noteseq_mel
        this.original_noteseq_overlay = this.empty_noteseq
      }
      else{
        this.notedic = this.notedic_acc
        this.original_noteseq = this.original_noteseq_acc
        this.original_noteseq_overlay = this.empty_noteseq
      }
    },
    place_melacc_toggle(){
      let top_rect = document.getElementById("time15").getBoundingClientRect();
      let bottom_rect = document.getElementById("original_prog15").getBoundingClientRect();

      let l1 = top_rect.left + window.pageXOffset || document.documentElement.scrollLeft
      let l2 = top_rect.right + window.pageXOffset || document.documentElement.scrollLeft
      let t = top_rect.top + window.pageYOffset || document.documentElement.scrollTop
      let b = bottom_rect.top + window.pageYOffset || document.documentElement.scrollTop

      d3.select("#melacc_toggle")
      .style("position","absolute")
      .style("left",l2+(l2-l1)/4+"px")
      .style("top", (1.15*t+b)/2.15+"px")
      .style("-webkit-transform","scale(0.6)")
      .raise()
    },

    // Chord playback
    play_chord(track, i){
      player.stop()
      let highlight_start = 0
      let highlight_end = 16
      if (track == 'original'){
        player.start(this.chords_to_noteseq([this.original_chd_mat[i]], false))
        for (let j=0; j<16; j++){
          if (document.getElementById("original_prog"+j).innerHTML.replace(/\s/g,"") != '' && j > i){
            highlight_end = j
            break
          }
          if (document.getElementById("original_prog"+j).innerHTML.replace(/\s/g,"") != ''){
            highlight_start = j
          }
        }
        for (let j=highlight_start; j<highlight_end; j++){
          this.highlight_cell("original_prog"+j, 0.5)
        }
      }
      if (track == 'altered'){
        for (let j=0; j<16; j++){
          if (document.getElementById("altered"+j).innerHTML.replace(/\s/g,"") != '' && j > i){
            break
          }
          if (document.getElementById("altered"+j).innerHTML.replace(/\s/g,"") != ''){
            highlight_start = j
          }
        }
        if (highlight_start < i - 3){return}
        for (let j=highlight_start; j<highlight_start+4; j++){
          this.highlight_cell("altered"+j, 0.5)
        }
        player.start(this.chords_to_noteseq([this.altered_chd_mat[i]], false))
      }

      
    },

    play_prog_original(){
      player.stop()
      player.start(this.chords_to_noteseq(this.original_chd_mat, false))
      let i = 0
      const high_light_step = () => {
        if (i < 16){
          this.highlight_cell("time"+i, this.prog_step_duration)
          if (document.getElementById("original_prog"+i).innerHTML.replace(/\s/g,"") != ''){
            let t = 1
            for (let j=i+1; j<16; j++){
              if (document.getElementById("original_prog"+j).innerHTML.replace(/\s/g,"") == ''){
                t++
              }
              else{
                break
              }
            }
            for (let j=i; j<i+t; j++){
              this.highlight_cell("original_prog"+j, t*this.prog_step_duration)
            }
          }
          i++
          setTimeout(() => {
            high_light_step()
          }, this.prog_step_duration*1000);
        }
      }
      high_light_step()
      
    },

    play_prog_altered(){
      player.stop()
      player.start(this.chords_to_noteseq(this.altered_chd_mat, false))
      let i = 0
      const high_light_step = () => {
        if (i < 16){
          if (i%4 == 0 && document.getElementById("altered"+i).innerHTML.replace(/\s/g,"") == ''){return}
          this.highlight_cell("time_altered"+i, this.prog_step_duration)
          if (document.getElementById("altered"+i).innerHTML.replace(/\s/g,"") != ''){
            for (let j=i; j<i+4; j++){
              this.highlight_cell("altered"+j, 4*this.prog_step_duration)
            }
          }
          i++
          setTimeout(() => {
            high_light_step()
          }, this.prog_step_duration*1000);
        }
      }
      high_light_step()
    },

    // Chord/Time cell highlighting
    highlight_cell(id, t){
      document.getElementById(id).classList.add("cell_active")
      setTimeout(() => {
        document.getElementById(id).classList.remove("cell_active")
      }, t*1000);
    },

    // Improv RNN
    improvise(chd){
      // Continue the melody
      
      let new_notes = []
      for (let i=0; i<this.cur_mel_seq.notes.length; i++){
        new_notes.push({
          pitch: this.cur_mel_seq.notes[i].pitch, 
          quantizedStartStep: this.cur_mel_seq.notes[i].quantizedStartStep, 
          quantizedEndStep: this.cur_mel_seq.notes[i].quantizedEndStep,
          velocity: this.mel_velocity  
        })
      }
      let sequence = {
        notes: new_notes,
        quantizationInfo: {stepsPerQuarter: this.mel_seq.quantizationInfo.stepsPerQuarter},
        totalQuantizedSteps: this.mel_seq.totalQuantizedSteps
      }
      
      this.rnn_prog.push(chd)
      if (this.rnn_prog.length > 4){
        this.rnn_prog = this.rnn_prog.splice(1,5)
      }
      rnn_worker.postMessage({sequence: sequence, prog: [chd]});

      rnn_worker.onmessage = (event) => {
        this.cur_mel_seq = event.data.cont_out
      }

    }
  },

  mounted(){
    this.get_songdata()
    this.get_data()
    player.loadAllSamples().then(()=>{ 
        this.loaded = true
        this.altered_noteseq.notes = []
    })
    
    let This = this
    player.callbackObject = {
        run: (note) => {This.canvas_update_note(note)},
          stop: () => {return}
        };

    // Barlines and player positioning
    window.onresize = this.place_barlines_and_player
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (event) => {
      let key = event.key
      if (['r','R'].includes(key)){
        this.player_reset()
      }
      if (['n','N'].includes(key)){
        this.get_data()
      }
      if (['z','Z'].includes(key)){
        this.get_data("038_B", false)
      }
      if (['x','X'].includes(key)){
        this.get_data("891_A", false)
      }
      if (['c','C'].includes(key)){
        this.get_data("050_B", false)
      }
      if (['v','V'].includes(key)){
        console.log(1)
        this.get_data("358_A", false)
      }
      if (['b','B'].includes(key)){
        this.get_data("476_X", false)
      }
    })

    // Cell highlighting - original (copied form educational)
    const mutationObserver_config = { childList: true, subtree: true, attributes:true };
    let original_timer = document.getElementById("original_player").shadowRoot.querySelector(".current-time")
    let original_controls = document.getElementById("original_player").shadowRoot.querySelector(".controls")

    function original_cell_highlight(time_cell, prog_cell, step=1){
        if (time_cell){
            time_cell.classList.add("time_cell_active")
            setTimeout(() => {
                if (time_cell.classList.contains("time_cell_active")){
                    time_cell.classList.remove("time_cell_active")
                }
            }, step*1000);
            if (! prog_cell.classList.contains("table_cell_active")){
                prog_cell.classList.add("table_cell_active")
                let lighted_cells = [prog_cell]
                let timeout = step
                let temp_cell = document.getElementById("original_prog"+(lighted_cells[lighted_cells.length-1].id.slice(13,15)*1+1))
                
                while (temp_cell && temp_cell.innerHTML.replace(/\s/g, '')==""){
                    temp_cell.classList.add("table_cell_active")
                    lighted_cells.push(temp_cell)
                    temp_cell = document.getElementById("original_prog"+(lighted_cells[lighted_cells.length-1].id.slice(13,15)*1+1))
                    timeout += step
                }
                setTimeout(() => {
                    while (lighted_cells.length > 0){
                        let cell = lighted_cells.pop()
                        if (cell.classList.contains("table_cell_active")){
                            cell.classList.remove("table_cell_active")
                        }
                    }
                }, timeout*1000);
            }
        }
    }

    let original_callback = function(mutationsList, observer) {
        observer == observer
        for(var mutation of mutationsList) {
          mutation == mutation
            if (original_controls.classList.contains("playing")){
                let time_cell = document.getElementById("time"+(original_timer.innerHTML.slice(2,4)*1))
                let prog_cell = document.getElementById("original_prog"+(original_timer.innerHTML.slice(2,4)*1))
                original_cell_highlight(time_cell, prog_cell)
            }
        }
    };

    let original_observer = new MutationObserver(original_callback);
    original_observer.observe(original_controls, mutationObserver_config);

  }


}


</script>

<style>
/* General / Misc */
#main_app{
  transform-origin: top left;
  -webkit-transform: scale(0.6);
  position: relative;
  left: 100px;
}

.right{
    position: relative;
    left: 100px;
}

.popover{
  max-width: 100% !important;
}

/* Prog Table */
.prog_table{
    width: 1900px !important;
}

.prog_head{
    text-align: center;
    vertical-align: text-top;
    width:100px;
    font-weight: bold;
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
}

.prog_repos{
    position: relative;
    top: 5px;}

.time_cell{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
    text-align: left;
    width: 100px;
}

.time_cell_active{
    background-color: #80b8f5 !important
}

.table_cell{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
    text-align: left;
    width: 100px;
}

.table_cell_active{
    background-color: #80b8f5 !important;
    animation-name: table_cell_active_ani;
    animation-duration: 1s;
}

/* Barlines //////////////////////////////////////////////////////////////////////////////// */
.barline_svg{
    position: absolute;
    top: 0px;
    left: 0px;
    width: 1600px;
    height: 1000px;
    pointer-events: none;
}

.barline{
    fill: black;
    opacity: 0.1;
}

/* Piano Roll Overlay //////////////////////////////////////////////////////////////////// */
canvas{
    display: block;
}

.svg{
    position: relative;
    top: -280px;
    width: 1600px;
    height: 280px;
}

.up{
    position:relative;
    top: -280px
}

#original_vis_overlay{
  opacity: 0.85;
}

/* Bpm slider ////////////////////////////////////////////////////////////////////////////////// */
#bpm_slider{
    position: relative;
    top: 15px;
    -webkit-appearance: none;
    width: 300px;
    height: 10px;
    background: #d3d3d3;
    outline: none;
    opacity: 0.7;
    -webkit-transition: .2s;
    transition: opacity .2s;
}

#bpm_slider:hover {
    opacity: 1;
  }
  
#bpm_slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 25px;
    height: 25px;
    background: #80b8f5;
    cursor: pointer;
    stroke-width: 0px;
}
  
#bpm_slider::-moz-range-thumb {
    width: 25px;
    height: 25px;
    background: #80b8f5;
    cursor: pointer;
    stroke-width: 0px;
}

#slider_container{
    height: 50px;
}

/* hover dropdown menus //////////////////////////////////////////////////////////////////////////////////////*/
@media only screen and (max-width: 991px) {
    .navbar-hover .show > .dropdown-toggle::after{
        transform: rotate(-90deg);
    }
}
@media only screen and (min-width: 992px) {
    .navbar-hover .collapse ul li{position:relative;}
    .navbar-hover .collapse ul li:hover> ul{display:block}
    .navbar-hover .collapse ul ul{position:absolute;top:100%;left:0;min-width:250px;display:none}
    .navbar-hover .collapse ul ul ul{position:absolute;top:0;left:100%;min-width:250px;display:none}
}

#resample{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
    padding-left: 10%;
}

#browse_samples{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
}

.dropdown{
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
}

/* Cell highlighting //////////////////////////////////////////////////////////////// */
.cell_active{
  background-color: #80b8f5 !important
}

</style>
